import json
import pickle
from flask import Blueprint, jsonify, request
from app.Models.modelsKatalog import Proizvod
from app.Models.modelsRedis import RedisService
from flasgger import swag_from
from sqlalchemy.orm import class_mapper
from database import redis_client,db_session



redis_routes = Blueprint('redis_routes', __name__)

@redis_routes.route('/dodavanjeProizvodaUKorpu/<int:product_id>', methods=['GET'])
def dodavanjeProizvodaUKorpu(product_id):
    """
    Upisuje proizvod u Redis na temelju proslijeđenog ID-a.

    ---
    parameters:
      - in: path
        name: product_id
        schema:
          type: integer
        required: true
        description: ID proizvoda koji se upisuje u Redis
    responses:
      200:
        description: Uspješan upis proizvoda u Redis
      500:
        description: Greška prilikom upisa proizvoda u Redis
    """
    try:
        proizvod = Proizvod.get_by_id(product_id)  

        if not proizvod:
            return jsonify({'message': 'Proizvod sa traženim ID-om nije pronađen.'}), 404

        product_key = f'product:{product_id}'

        if redis_client.exists(product_key):
            return jsonify({'message': 'Proizvod već postoji u Redisu.'}), 409

        product_name = proizvod.producerName
        redis_client.set(product_key, product_name) #pretrazujemo redi po product_key

        redis_client.expire(product_key, 30)

        return jsonify({'message': 'Proizvod uspešno upisan u Redis.'}), 200
    except Exception as e:
        return jsonify({'message': f'Greška prilikom upisa proizvoda u Redis: {str(e)}'}), 500
@redis_routes.route('/citanjeProzivodaIzKorpe/<int:produc_id>', methods=['GET'])
def citanjeProzivodaIzKorpe(produc_id):
    """
    Provera postojanja proizvoda u Redisu na temelju ID-a.

    ---
    parameters:
      - in: path
        name: produc_id
        schema:
          type: integer
        required: true
        description: ID proizvoda koji se provjerava u Redisu
    responses:
      200:
        description: Informacija o postojanju proizvoda u Redisu
      404:
        description: Proizvod nije pronađen u Redisu
    """
    result = RedisService.procitajProizvodIzKorpe(produc_id)
    if 'pronađen' in result:
        return result, 200
    else:
        return result, 404

def as_dict(obj):
    return {column.key: getattr(obj, column.key) for column in class_mapper(obj.__class__).mapped_table.c}

    
    #@redis_routes.route('/products_by_category', methods=['GET'])
@redis_routes.route('/products_by_category', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'category',
            'in': 'query',
            'type': 'string',
            'description': 'Category for which to retrieve products'
        }
    ],
    'responses': {
        200: {
            'description': 'List of products in the specified category',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'producerName': {'type': 'string'},
                        'productDescription': {'type': 'string'},
                        'category': {'type': 'string'},
                        'price': {'type': 'integer'},
                        'numOfCliks': {'type': 'integer'},
                        'picture': {'type': 'string'},
                        'discount': {'type': 'integer'},
                        'quantity': {'type': 'integer'}
                    }
                }
            }
        },
        404: {
            'description': 'No products found for the specified category',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def get_products_by_category():
    category = request.args.get('category')
    #category = data.get('category')
    # Provera da li postoji hash za datu kategoriju u Redisu
    hash_key = f'category:{category}' #po kategoriji
    if redis_client.exists(hash_key):
        # Ako postoji hash, čitamo vrednosti i vraćamo ih kao listu
        products_json = redis_client.hvals(hash_key)
        return [json.loads(product) for product in products_json]
    else:
        # Ako ne postoji hash, izvršavamo upit u PostgreSQL bazi
        products = db_session.query(Proizvod).filter(Proizvod.category == category).all()
        # Konvertujemo rezultat u listu JSON objekata
        for product in products:
            product_dict = as_dict(product)
            redis_client.hset(hash_key, product_dict['id'], json.dumps(product_dict))
        # Povratni podaci
        return [json.loads(product) for product in redis_client.hvals(hash_key)]
    
@redis_routes.route('/prvih_deset_proizvoda', methods=['GET'])
def prvih_deset_proizvoda():
    """
    Prikazuje prvih 10 proizvoda.
    ---
    responses:
      200:
        description: Lista prvih 10 proizvoda.
    """
    redis_key = 'pocetni_proizvodi1'
    cached_data=redis_client.get('pocetni_proizvodi1')
    if cached_data:
        # Ako postoje, koristi keširane podatke
        cached_data = json.loads(cached_data.encode('utf-8'))
        # Prikazivanje podataka iz Redis-a, bez kreiranja novih instanci klase Proizvod
        return jsonify({'proizvodi': [(proizvod['id'], proizvod) for proizvod in cached_data['proizvodi']]})

    pocetni_proizvodi = Proizvod.query.limit(10).all()

    # Keširanje podataka u Redis koristeći JSON
    data_to_cache = json.dumps({'proizvodi': [proizvod.toDict() for proizvod in pocetni_proizvodi]}, default=str)
    redis_client.set(redis_key, data_to_cache, ex=15)
    response_data = {'proizvodi': [(proizvod.id, proizvod.toDict()) for proizvod in pocetni_proizvodi]}

    return jsonify(response_data)
@redis_routes.route('/ucitaj_narednih_10', methods=['POST'])
def ucitaj_narednih_10():
    """
    Učitava sledećih 10 proizvoda na osnovu trenutne stranice.
    ---
    parameters:
      - name: stranica
        in: query
        type: integer
        description: Trenutna stranica
        required: false
        default: 2
    responses:
      200:
        description: Lista sledećih 10 proizvoda.
    """
    # Dohvatanje informacija o trenutnoj stranici i broju proizvoda po stranici
    stranica = request.args.get('stranica', default=2, type=int)
    broj_proizvoda_po_stranici = 10
    redis_key=f'proizvodi_stranica_{stranica}'
    # Pokušaj prvo dohvatiti iz Redis hash-a
    cached_data=redis_client.get(f'proizvodi_stranica_{stranica}')
    if cached_data:
        # Ako postoje, koristi keširane podatke
        cached_data = json.loads(cached_data.encode('utf-8'))
        return jsonify({'proizvodi': [(proizvod['id'], proizvod) for proizvod in cached_data['proizvodi']]})
    else:
            # Ako nije u Redis kešu, dohvati iz PostgreSQL-a pomoću SQLAlchemy-ja
            pocetni_indeks = (stranica - 1) * broj_proizvoda_po_stranici
            pocetni_proizvodi = Proizvod.query.offset(pocetni_indeks).limit(broj_proizvoda_po_stranici).all()
            data_to_cache = json.dumps({'proizvodi': [proizvod.toDict() for proizvod in pocetni_proizvodi]}, default=str)
            redis_client.set(redis_key, data_to_cache, ex=15)
            response_data = {'proizvodi': [(proizvod.id, proizvod.toDict()) for proizvod in pocetni_proizvodi]}

            return jsonify(response_data)