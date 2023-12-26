import json
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
        redis_client.set(product_key, product_name)

        redis_client.expire(product_key, 30)

        return jsonify({'message': 'Proizvod uspešno upisan u Redis.'}), 200
    except Exception as e:
        return jsonify({'message': f'Greška prilikom upisa proizvoda u Redis: {str(e)}'}), 500
@redis_routes.route('/citanjeProzivodaIzKorpe/<int:produc_id>', methods=['GET'])
def citanjeProzivodaIzKorpe(produc_id):
    """
    Provjera postojanja proizvoda u Redisu na temelju ID-a.

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
    hash_key = f'category:{category}'
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
# Pimer korišćenja: