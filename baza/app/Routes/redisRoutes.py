import datetime
import json
from sqlalchemy import or_
import pickle
from flask import Blueprint, jsonify, request
from app.Models.modelsKatalog import Proizvod
from app.Models.modelsRedis import RedisService
from flasgger import swag_from
from sqlalchemy.orm import class_mapper
from database import redis_client,db_session
from datetime import datetime



redis_routes = Blueprint('redis_routes', __name__)

# @redis_routes.route('/dodavanjeProizvodaUKorpu/<int:product_id>', methods=['GET'])
# def dodavanjeProizvodaUKorpu(product_id):
#    
@redis_routes.route('/dodaj_u_korpu', methods=['POST'])
def dodaj_u_korpu():
    """
    Dodaje proizvode u korpu korisnika.

    ---
    parameters:
      - in: formData
        name: korisnik_id
        type: integer
        required: true
        description: ID korisnika
      - in: formData
        name: proizvodi_id
        type: string
        required: true
        description: String koji sadrži ID-jeve proizvoda razdvojene zarezom
      
      

    responses:
      200:
        description: Proizvodi uspešno dodati u korpu
      500:
        description: Greška prilikom dodavanja proizvoda u korpu
    """
    
    korisnik_id = int(request.form['korisnik_id'])
    proizvodi_id_str = request.form['proizvodi_id']
        
    # Razdvajanje stringa proizvodi_id po zarezu i konvertovanje u listu integera
    proizvodi_id = [int(id) for id in proizvodi_id_str.split(',')]
    print(proizvodi_id)
    #trenutna_stranica = int(request.form['trenutna_stranica'])

    # try:
    kljuc_korpe = f'korpa_{korisnik_id}'

    # Dohvatanje svih atributa proizvoda iz Redis hash-a
    atributi_proizvoda = [redis_client.hget(f'pocetni_proizvodi1', proizvod_id) for proizvod_id in proizvodi_id]
    #return atributi_proizvoda
    # Dodavanje proizvoda u korpu
    for atributi_json in atributi_proizvoda:
        if atributi_json:
            atributi = json.loads(atributi_json.encode('utf-8'))

            # Prilagodite ovo prema atributima koje želite dodati u korpu
            proizvod_u_korpi = {
                'id': atributi['id'],
                'productDescription': atributi['productDescription'],
                'producerName': atributi['producerName'],
                'price': atributi['price'],
                'picture': atributi['picture'],
            }

            # Dodaj proizvod u korpu
            if not redis_client.sismember(kljuc_korpe, atributi['id']):
                    # Dodaj proizvod u korpu ako već nije u njoj
                    redis_client.sadd(kljuc_korpe, json.dumps(proizvod_u_korpi))

        return jsonify({'message': 'Proizvodi uspešno dodati u korpu'}), 200
    
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
    cached_data = redis_client.hgetall(redis_key)

    if cached_data:
        # Ako postoje, koristi keširane podatke
        proizvodi = [json.loads(atributi.encode('utf-8')) for atributi in cached_data.values()]
        return jsonify({'proizvodi': [(proizvod['id'], proizvod) for proizvod in proizvodi]})

    pocetni_proizvodi = Proizvod.query.limit(10).all()

    # Keširanje podataka u Redis hash koristeći JSON
    for proizvod in pocetni_proizvodi:
        atributi_proizvoda = proizvod.toDict()
        redis_client.hset(redis_key, proizvod.id, json.dumps(atributi_proizvoda, default=str))

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
        required: true
        
    responses:
      200:
        description: Lista sledećih 10 proizvoda.
    """
    # Dohvatanje informacija o trenutnoj stranici i broju proizvoda po stranici
    #stranica = request.args.get('stranica', type=int)
    stranica = request.args.get('stranica', type=int)

    #stranica+=stranica+1
    broj_proizvoda_po_stranici = 10
    redis_key=f'pocetni_proizvodi{stranica}'
    # Pokušaj prvo dohvatiti iz Redis hash-a
    cached_data=redis_client.get(f'pocetni_proizvodi{stranica}')
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


@redis_routes.route('/prikazi_akcijske_proizvode', methods=['GET'])
def prikazi_akcijske_proizvode():
    """
    Prikazuje akcijske proizvode na osnovu dana u nedelji.
    ---

    responses:
      200:
        description: Akcijski proizvodi za dati dan.
        schema:
          type: array
          items:
            type: object
            properties:
              proizvodjac:
                type: string
              popust:
                type: integer
              cena:
                type: integer
    """
    danas_je = datetime.now().strftime('%A')  # 'Monday', 'Tuesday', ...
    print(danas_je)
    #danas_je='Monday'
    akcijski_proizvodi = redis_client.get(danas_je)

    if not akcijski_proizvodi:
        # Ako podaci nisu u kešu, dohvatite proizvode iz baze podataka
        if danas_je == 'Monday' or danas_je == 'Wednesday':
            proizvodi_za_popust = db_session.query(Proizvod).filter(or_(Proizvod.category == 'Voce' )).all()
            if proizvodi_za_popust:
                for proizvod in proizvodi_za_popust:
                    proizvod.oldPrice = proizvod.price
                    proizvod.price = proizvod.price - (proizvod.price * proizvod.discount) / 100
            # Konvertujte proizvode u format koji ćete vratiti kao odgovor
                akcijski_proizvodi = [
                    {"proizvodjac": proizvod.producerName,"opis":proizvod.productDescription, "popust": proizvod.discount, "novacena": proizvod.price,"staracena":proizvod.oldPrice}
                    for proizvod in proizvodi_za_popust
                ]
        # Sačuvaj podatke u Redis keš
                redis_client.set(danas_je, json.dumps(akcijski_proizvodi))
        # Ažuriraj cene sa popustom za mleko i povrće ako je danas utorak
        elif danas_je == 'Tuesday' or danas_je == 'Thursday':
            proizvodi_za_popust = db_session.query(Proizvod).filter(or_(Proizvod.category == 'Mlecni proizvodi', Proizvod.category == 'Povrce')).all()
            if proizvodi_za_popust:

                for proizvod in proizvodi_za_popust:
                    proizvod.oldPrice = proizvod.price
                    proizvod.price = proizvod.price - (proizvod.price * proizvod.discount) / 100
        # Konvertujte proizvode u format koji ćete vratiti kao odgovor
                akcijski_proizvodi = [
                    {"proizvodjac": proizvod.producerName,"opis":proizvod.productDescription, "popust": proizvod.discount, "novacena": proizvod.price,"staracena":proizvod.oldPrice}
                    for proizvod in proizvodi_za_popust
                ]

        # Sačuvaj podatke u Redis keš
                redis_client.set(danas_je, json.dumps(akcijski_proizvodi))
        elif danas_je == 'Friday':
            proizvodi_za_popust = db_session.query(Proizvod).filter(or_(Proizvod.category == 'Riba')).all()
            if proizvodi_za_popust:

                for proizvod in proizvodi_za_popust:
                    proizvod.oldPrice = proizvod.price
                    proizvod.price = proizvod.price - (proizvod.price * proizvod.discount) / 100
        # Konvertujte proizvode u format koji ćete vratiti kao odgovor
                akcijski_proizvodi = [
                    {"proizvodjac": proizvod.producerName,"opis":proizvod.productDescription, "popust": proizvod.discount, "novacena": proizvod.price,"staracena":proizvod.oldPrice}
                    for proizvod in proizvodi_za_popust
                ]

        # Sačuvaj podatke u Redis keš
                redis_client.set(danas_je, json.dumps(akcijski_proizvodi))
    else:
        akcijski_proizvodi = json.loads(akcijski_proizvodi)
    return jsonify(akcijski_proizvodi)