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
        name: korisnik_email
        type: string
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
    
    korisnik_id = None
    korisnik_email = request.form.get('korisnik_email')    
    proizvodi_id_str = request.form['proizvodi_id']
    redis_key="user"
    if not korisnik_email or not proizvodi_id_str:
        return jsonify({'error': 'Nedostaju potrebni parametri.'}), 400
    
    user_ids = redis_client.hkeys(redis_key)
    
    for user_id in user_ids:
        user_data_json = redis_client.hget(redis_key, user_id)
        if user_data_json:
            user_data = json.loads(user_data_json.encode('utf-8'))
            print(f"Proveravam korisnika sa email-om: {user_data.get('email')}")
            if user_data.get('email') == korisnik_email:
                korisnik_id = user_id
                break
    #return (korisnik_id)
    # Razdvajanje stringa proizvodi_id po zarezu i konvertovanje u listu integera
    proizvodi_id = [int(id) for id in proizvodi_id_str.split(',')]
    
    #trenutna_stranica = int(request.form['trenutna_stranica'])
    if korisnik_id is None:
        return jsonify({'error': 'Korisnik nije pronađen.'}), 404
    # try:
    kljuc_korpe = f'korpa_{korisnik_id}'

    # Dohvatanje svih atributa proizvoda iz Redis hash-a
    atributi_proizvoda = [redis_client.hget(f'pocetni_proizvodi1', proizvod_id) for proizvod_id in proizvodi_id]
    #return atributi_proizvoda
    if not atributi_proizvoda:
        return jsonify({'message': 'Nema proizvoda u kesu'}), 400

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
            redis_client.sadd(kljuc_korpe, json.dumps(proizvod_u_korpi))

    return jsonify({'message': 'Proizvodi uspešno dodati u korpu'}), 200

@redis_routes.route('/kupi_proizvode', methods=['POST'])
def kupi_proizvode():
    """
    Kupuje proizvode iz korpe.
    ---
    parameters:
      - name: korisnik_email
        in: formData
        type: string
        description: E-mail korisnika
        required: true
    responses:
      200:
        description: Poruka o uspešnoj kupovini.
    """
    korisnik_id = None
    korisnik_email = request.args.get('korisnik_email') 
    print(korisnik_email)
    redis_key="user"
    
    user_ids = redis_client.hkeys(redis_key)
    for user_id in user_ids:
        user_data_json = redis_client.hget(redis_key, user_id)
        if user_data_json:
            user_data = json.loads(user_data_json)
            print(f"Proveravam korisnika sa ID-om {user_id}: {user_data.get('email')}")
            if user_data.get('email') == korisnik_email:
                korisnik_id = user_id
                break
    else:
        print(f"Korisnik sa email-om '{korisnik_email}' nije pronađen.")
    # Čitanje proizvoda iz korpe u Redisu
    korpa_key = f'korpa_{korisnik_id}'
    print(korisnik_id)
    proizvodi_u_korpi = redis_client.smembers(korpa_key)

    if proizvodi_u_korpi:
        print(proizvodi_u_korpi)
        # Iteriranje kroz proizvode u korpi
        for proizvod_id_str in proizvodi_u_korpi:
            proizvod_id = json.loads(proizvod_id_str)
            print(proizvod_id)
            json_proizvod = redis_client.hget('proizvodi', str(proizvod_id['id']))

            #proizvod_dict=json.loads(json_proizvod)
            print(json_proizvod)
            if json_proizvod:
                print("opet")
                proizvod_dict = json.loads(json_proizvod)
                print(proizvod_dict)
                trenutna_kolicina = proizvod_dict.get('quantity', 0)
                print("ja",trenutna_kolicina)
                nova_kolicina = max(0, trenutna_kolicina - 1)  # Smanjite količinu za 1 (ili drugi odgovarajući broj)

                proizvod_dict['quantity'] = nova_kolicina

                            # Ažurirajte vrednost direktno u Redis hash mapi
                redis_client.hset('proizvodi', str(proizvod_id['id']), json.dumps(proizvod_dict))
        # Pražnjenje korpe u Redisu
        redis_client.delete(korpa_key)

        return jsonify({'message': 'Uspešna kupovina!'})

    return jsonify({'message': 'Korpa je prazna.'}), 404
                    
    
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
    
@redis_routes.route('/ucitavajPo10Proizvoda', methods=['POST'])
def prvih_deset_proizvoda():
    """
    Prikazuje prvih 10 proizvoda.
    ---
    parameters:
      - name: stranica
        in: query
        type: integer
        description: Trenutna stranica
        required: true
    responses:
      200:
        description: Lista prvih 10 proizvoda.
    """
    redis_key = 'proizvodi'
    redis_key_akcija = 'Tuesday'#datetime.now().strftime('%A')  # Ključ za akcijske proizvode (npr. 'Monday')

    # Dohvati podatke iz Redis keša
    cached_data_proizvodi = redis_client.hvals(redis_key)
    cached_data_akcija = redis_client.get(redis_key_akcija)
    #cached_data = redis_client.hvals(redis_key)
    stranica = request.args.get('stranica', type=int)
    broj_proizvoda_po_stranici = 10
    x=(stranica-1)*broj_proizvoda_po_stranici
    y=x+broj_proizvoda_po_stranici
    if cached_data_proizvodi:
        # Ako postoje, koristi keširane podatke
        proizvodi = [json.loads(atributi.encode('utf-8')) for atributi in cached_data_proizvodi[x:y]]
        if cached_data_akcija:
            akcijski_proizvodi = json.loads(cached_data_akcija.encode('utf-8'))
            print(akcijski_proizvodi)

            for proizvod in proizvodi:
                if (redis_key_akcija == 'Monday' or redis_key_akcija == 'Wednesday') and proizvod['category'] == 'Voce':
                    akcijski_proizvod = next((p for p in akcijski_proizvodi if p['id'] == proizvod['id']), None)
                    if akcijski_proizvod:
                        proizvod['novacena'] = akcijski_proizvod.get('novacena', None)
                        proizvod['staracena']=akcijski_proizvod.get('staracena',None)
                        print(proizvod['novacena'],proizvod['staracena'])
                elif (redis_key_akcija == 'Tuesday' or redis_key_akcija == 'Thursday') and proizvod['category'] in ['Mlecni proizvodi','Povrce']:
                    akcijski_proizvod = next((p for p in akcijski_proizvodi if p['id'] == proizvod['id']), None)
                    if akcijski_proizvod:
                        proizvod['novacena'] = akcijski_proizvod.get('novacena', None)
                        proizvod['staracena']=akcijski_proizvod.get('staracena',None)
                        print(proizvod['novacena'],proizvod['staracena'])
                elif(redis_key_akcija == 'Friday'  and proizvod['category'] =='Riba'):
                    akcijski_proizvod = next((p for p in akcijski_proizvodi if p['id'] == proizvod['id']), None)
                    if akcijski_proizvod:
                        proizvod['novacena'] = akcijski_proizvod.get('novacena', None)
                        proizvod['staracena']=akcijski_proizvod.get('staracena',None)
                        print(proizvod['novacena'],proizvod['staracena'])
    return jsonify({'proizvodi': [(proizvod['id'], proizvod) for proizvod in proizvodi]})

    
 
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
    #danas_je='Tuesday'
    redis_key='proizvodi'
    akcijski_proizvodi = redis_client.get(danas_je)
    proizvodi_za_popust = []
    # HSCAN vraća iterator koji prolazi kroz sve ključeve i vrednosti u hash-u
    

    #return jsonify({'proizvodi': proizvodi})
    if not akcijski_proizvodi:
        # Ako podaci nisu u kešu, dohvatite proizvode iz baze podataka
        if danas_je == 'Monday' or danas_je == 'Wednesday':
            hash_values = redis_client.hgetall(redis_key)

    # Prolazi kroz svaki ključ i vrednost
            for key, atributi_json in hash_values.items():
                atributi = json.loads(atributi_json)
                
                # Proveri da li proizvod pripada odabranoj kategoriji
                if atributi.get('category') in [ "Voce"]:
                    proizvodi_za_popust.append((atributi['id'], atributi))
            print(proizvodi_za_popust)
            if proizvodi_za_popust:
                for proizvod_tuple in proizvodi_za_popust:
                    proizvod = proizvod_tuple[1]  # Drugi element tuple-a je rečnik sa atributima proizvoda
                    print("LA", proizvod)
                    proizvod['oldPrice'] = proizvod['price']
                    proizvod['price'] = proizvod['price'] - (proizvod['price'] * proizvod['discount']) / 100
            # Konvertujte proizvode u format koji ćete vratiti kao odgovor
                akcijski_proizvodi = [
                    {
                        "id":proizvod[1]['id'],
                        "proizvodjac": proizvod[1]['producerName'],
                        "opis": proizvod[1]['productDescription'],
                        "popust": proizvod[1]['discount'],
                        "novacena": proizvod[1]['price'],
                        "staracena": proizvod[1]['oldPrice']
                    }
                    for proizvod in proizvodi_za_popust
                ]
        # Sačuvaj podatke u Redis keš
                redis_client.set(danas_je, json.dumps(akcijski_proizvodi))
        # Ažuriraj cene sa popustom za mleko i povrće ako je danas utorak
        elif danas_je == 'Tuesday' or danas_je == 'Thursday':
            for _, atributi_json in redis_client.hscan_iter(redis_key):
                atributi = json.loads(atributi_json.encode('utf-8'))
                
                # Proveri da li proizvod pripada odabranoj kategoriji
                if atributi.get('category') in ['Mlecni proizvodi', 'Povrce']:
                    proizvodi_za_popust.append((atributi['id'], atributi))
            
            if proizvodi_za_popust:
                for proizvod in proizvodi_za_popust:
                    proizvod[1]['oldPrice'] = proizvod[1]['price']
                    proizvod[1]['price'] = proizvod[1]['price'] - (proizvod[1]['price'] * proizvod[1]['discount']) / 100
                
                akcijski_proizvodi = [
                    {
                        "id":proizvod[1]['id'],
                        "proizvodjac": proizvod[1]['producerName'],
                        "opis": proizvod[1]['productDescription'],
                        "popust": proizvod[1]['discount'],
                        "novacena": proizvod[1]['price'],
                        "staracena": proizvod[1]['oldPrice']
                    }
                    for proizvod in proizvodi_za_popust
                ]

                redis_client.set(danas_je, json.dumps(akcijski_proizvodi))

        elif danas_je == 'Friday':
            for _, atributi_json in redis_client.hscan_iter(redis_key):
                atributi = json.loads(atributi_json.encode('utf-8'))
                
                # Proveri da li proizvod pripada odabranoj kategoriji
                if atributi.get('category') == 'Riba':
                    proizvodi_za_popust.append((atributi['id'], atributi))
            
            if proizvodi_za_popust:
                for proizvod in proizvodi_za_popust:
                    proizvod[1]['oldPrice'] = proizvod[1]['price']
                    proizvod[1]['price'] = proizvod[1]['price'] - (proizvod[1]['price'] * proizvod[1]['discount']) / 100
                
                akcijski_proizvodi = [
                    {
                        "id":proizvod[1]['id'],
                        "proizvodjac": proizvod[1]['producerName'],
                        "opis": proizvod[1]['productDescription'],
                        "popust": proizvod[1]['discount'],
                        "novacena": proizvod[1]['price'],
                        "staracena": proizvod[1]['oldPrice']
                    }
                    for proizvod in proizvodi_za_popust
                ]

                redis_client.set(danas_je, json.dumps(akcijski_proizvodi))
    else:
        akcijski_proizvodi = json.loads(akcijski_proizvodi)
    return jsonify(akcijski_proizvodi)