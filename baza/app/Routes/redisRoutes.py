import datetime
import json
from sqlalchemy import desc, or_
import pickle
from flask import Blueprint, jsonify, request
from app.Models.modelsKatalog import Proizvod
from app.Models.modelsKupac import Kupac
from app.Models.modelsRedis import RedisService
from flasgger import swag_from
from sqlalchemy.orm import class_mapper
from database import redis_client,db_session
from datetime import datetime, timedelta



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
    
    print(request.form)
    korisnik_id = None
    korisnik_email = request.json.get('korisnik_email')    
    proizvodi_id = request.json['proizvodi_id']

    print(f"Korisnik email: {korisnik_email}")
    print(f"Proizvodi ID: {proizvodi_id}")


    redis_key="user"
    if not korisnik_email or not proizvodi_id:
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
    #proizvodi_id = [int(id) for id in proizvodi_id_str.split(',')]
    
    #trenutna_stranica = int(request.form['trenutna_stranica'])
    if korisnik_id is None:
        return jsonify({'error': 'Korisnik nije pronađen.'}), 404
    # try:
    kljuc_korpe = f'korpa_{korisnik_id}'

    # Dohvatanje svih atributa proizvoda iz Redis hash-a
    atributi_proizvoda = [redis_client.hget(f'proizvodi', proizvodi_id)]
    #return atributi_proizvoda
    if not atributi_proizvoda:
        return jsonify({'message': 'Nema proizvoda u kesu'}), 400
    print(atributi_proizvoda)
    # Dodavanje proizvoda u korpu
    
    for atributi_json in atributi_proizvoda:
        if atributi_json:
            atributi = json.loads(atributi_json.encode('utf-8'))
            print("Usao sam")
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
    korisnik_email = request.json.get('korisnik_email') 
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
        ukupna_cena_proizvoda = 0
        # Iteriranje kroz proizvode u korpi
        for proizvod_id_str in proizvodi_u_korpi:
            proizvod_id = json.loads(proizvod_id_str)
            print(proizvod_id)
            json_proizvod = redis_client.hget('proizvodi', str(proizvod_id['id']))

            #proizvod_dict=json.loads(json_proizvod)
            print(json_proizvod)
            if json_proizvod:
                proizvod_dict = json.loads(json_proizvod)
                ukupna_cena_proizvoda += proizvod_dict.get('price', 0)
                print("opet")
                print(proizvod_dict)
                trenutna_kolicina = proizvod_dict.get('quantity', 0)
                trenutni_numofClic=proizvod_dict.get('numOfCliks', 0)
                nova=trenutni_numofClic+1
                print("ja",trenutna_kolicina)
                nova_kolicina = max(0, trenutna_kolicina - 1)  # Smanjite količinu za 1 (ili drugi odgovarajući broj)

                proizvod_dict['quantity'] = nova_kolicina
                proizvod_dict['numOfCliks'] = nova

                            # Ažurirajte vrednost direktno u Redis hash mapi
                redis_client.hset('proizvodi', str(proizvod_id['id']), json.dumps(proizvod_dict))
                proizvod=Proizvod.query.filter_by(id=proizvod_id["id"]).first()
                if(proizvod):
                    proizvod.numOfCliks+=nova 
                    db_session.commit()
        # Pražnjenje korpe u Redisu
            korisnik = Kupac.query.filter_by(email=korisnik_email).first()

            if korisnik:
                # Ažuriranje vrednosti bodova korisnika u PostgreSQL bazi
                korisnik.bodovi += ukupna_cena_proizvoda
                db_session.commit()
        redis_client.delete(korpa_key)

        return jsonify({'message': 'Uspešna kupovina!'})

    return jsonify({'message': 'Korpa je prazna.'}),404
                    
    
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
@redis_routes.route('/products_by_category', methods=['POST'])
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
    data= request.get_json()
    category=data.get('category')
   # print(kategorija)
    #category = request.json.get('category')
    #category = data.get('category')
    # Provera da li postoji hash za datu kategoriju u Redisu
    print(category)
    hash_key = f'category:{category}' #po kategoriji
    kljuc='proizvodi'
    if redis_client.exists(hash_key):
        # Ako postoji hash, čitamo vrednosti i vraćamo ih kao listu
        products_json = redis_client.hvals(hash_key)
        return [json.loads(product) for product in products_json]
    else:
        all_products_json = redis_client.hgetall(kljuc)
        matching_products = [json.loads(product) for product in all_products_json.values() if json.loads(product).get('category') == category]
        for product in matching_products:
            redis_client.hset(hash_key, product['id'], json.dumps(product))
        return matching_products
    
@redis_routes.route('/ucitavajPo10Proizvoda/<int:brojStranice>', methods=['GET'])
def prvih_deset_proizvoda(brojStranice):
    """
    Prikazuje prvih 10 proizvoda.
    ---
    parameters:
        name: stranica1
        in: query
        type: integer
        description: Trenutna stranica
        required: true
    responses:
      200:
        description: Lista prvih 10 proizvoda.
    """
    
    redis_key = 'proizvodi'
    redis_key_akcija =datetime.now().strftime('%A')  # Ključ za akcijske proizvode (npr. 'Monday')


    # Dohvati podatke iz Redis keša
    cached_data_proizvodi = redis_client.hvals(redis_key)
    cached_data_akcija = redis_client.get(redis_key_akcija)
    #cached_data = redis_client.hvals(redis_key)
    #stranica = request.args.get('stranica', type=int)
    stranica=brojStranice
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
                        "producerName": proizvod[1]['producerName'],
                        "productDescription": proizvod[1]['productDescription'],
                        "discount": proizvod[1]['discount'],
                        "novacena": proizvod[1]['price'],
                        "price": proizvod[1]['oldPrice'],
                        "picture":proizvod[1]['picture']
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
                        "producerName": proizvod[1]['producerName'],
                        "productDescription": proizvod[1]['productDescription'],
                        "discount": proizvod[1]['discount'],
                        "novacena": proizvod[1]['price'],
                        "price": proizvod[1]['oldPrice']
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
                        "producerName": proizvod[1]['producerName'],
                        "productDescription": proizvod[1]['productDescription'],
                        "discount": proizvod[1]['discount'],
                        "novacena": proizvod[1]['price'],
                        "price": proizvod[1]['oldPrice']
                    }
                    for proizvod in proizvodi_za_popust
                ]

                redis_client.set(danas_je, json.dumps(akcijski_proizvodi))
    else:
        akcijski_proizvodi = json.loads(akcijski_proizvodi)
    return jsonify(akcijski_proizvodi)



@redis_routes.route('/prikaziProizvodeUKorpi',methods=['POST'])
def prikaziProizvodeUKorpi():
    """
    Prikazuje proizvode u korpi korisnika.

    ---
    parameters:
      - in: query
        name: korisnik_email
        type: string
        required: true
        description: Email korisnika

    responses:
      200:
        description: Proizvodi u korpi
      400:
        description: Greška: Email korisnika nije prosleđen
      500:
        description: Interna server greška
    """
    try:
        # Dobijanje emaila korisnika iz zahteva
        data = request.get_json()
        korisnik_id = None
        #korisnik_email = request.args.get('korisnik_email')
        korisnik_email = data.get('korisnik_email')    
        #korisnik_email=emailKorisnika
       
        redis_key="user"
        if not korisnik_email :
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

        if not korisnik_id:
            return jsonify({"error": "ID korisnika nije prosleđen."}), 400

        # Formirajte ključ za Redis skup korpe korisnika
        kljuc_korpe = f'korpa_{korisnik_id}'

        # Dobijanje svih proizvoda u korpi iz Redis skupa
        proizvodi_u_korpi = redis_client.smembers(kljuc_korpe)

        # Konvertujte proizvode u listu radi lakše manipulacije
        proizvodi_lista = list(proizvodi_u_korpi)

        return [json.loads(product) for product in proizvodi_lista], 200

    except Exception as e:
        return jsonify({"error":str(e)}), 500
                        


@redis_routes.route('/obrisiProizvodIzKorpe', methods=['DELETE'])
def obrisiProizvodIzKorpe():
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
        name: proizvod_id
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
    redis_key="user"
    korisnik_email = request.json.get('korisnik_email')   
    proizvodId= request.json.get('proizvod_id')

    print(korisnik_email, proizvodId)

    if not korisnik_email or not proizvodId:
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
    if korisnik_id is None:
        return jsonify({'error': 'Korisnik nije pronađen.'}), 404
    # try:
    kljuc_korpe = f'korpa_{korisnik_id}'
    proizvodId_str = str(proizvodId)
    print(proizvodId_str)
    if redis_client.exists(kljuc_korpe):
    # Čitamo članove hash mape kao rečnik
        set_members = redis_client.smembers(kljuc_korpe)
        print(set_members)

        # Provera da li proizvod postoji u korpi
        for member in set_members:
        # Parsiramo JSON string u rečnik
            product = json.loads(member.encode('utf-8'))
            print(product.get('id'),proizvodId_str,proizvodId)
            # Provera da li proizvod ima traženi ID
            if str(product.get('id')) == proizvodId_str:                # Ako ima, uklanjamo proizvod iz korpe
                print("usao")
                redis_client.srem(kljuc_korpe, member)
                return jsonify({'message': 'Proizvod uspešno obrisan iz korpe.'}), 200

        # Ako ne pronađemo proizvod, vraćamo odgovarajuću grešku
        return jsonify({'error': 'Proizvod nije pronađen u korpi.'}), 404
    else:
        return jsonify({'error': 'Korpa nije pronađena.'}),404
    



@redis_routes.route('/vratiKategorije',methods=['GET'])
def vratiKategorije():
    """
    Prikazuje proizvode u korpi korisnika.

    ---
    parameters:
      - in: formData
        name: korisnik_email
        type: string
        required: false
        description: Email korisnika

    responses:
      200:
        description: Proizvodi uspešno dodati u korpu
      500:
        description: Greška prilikom dodavanja proizvoda u korpu
    """
    kljuc_proizvodi = 'proizvodi'  # Ključ za hash sa svim proizvodima u Redisu
    kljuc_kategorije = 'kategorije'  # Ključ za set sa kategorijama u Redisu

    # Provera da li postoji set za kategorije u Redisu
    if redis_client.exists(kljuc_kategorije):
        # Ako postoji set, čitamo vrednosti i vraćamo ih kao listu
        categories = list(redis_client.smembers(kljuc_kategorije))
        return categories
    else:
        # Ako ne postoji set, prolazimo kroz proizvode i dodajemo kategorije direktno u set
        if redis_client.exists(kljuc_proizvodi):
            all_products_json = redis_client.hgetall(kljuc_proizvodi)
            
            # Dodajemo kategorije direktno u set
            redis_client.sadd(kljuc_kategorije, *[json.loads(product)['category'] for product in all_products_json.values()])
            # Čitamo vrednosti seta i vraćamo ih kao listu
            categories = list(redis_client.smembers(kljuc_kategorije))
            return categories, 200
        else:
            return jsonify({"error": "Nema proizvoda u Redisu."}),404
        

def syncredisandgres():
    datafromredis=redis_client.hgetall('proizvodi')
    Proizvod.updateMainDB(datafromredis)


@redis_routes.route('/vratiNajpopularnijeproizvode', methods=['GET'])
def vratiNajpopularnijeproizvode():
    proizvodi_raw = redis_client.hgetall('proizvodi')

    # Pretvaranje JSON stringova u Python objekte
    proizvodi = {int(k): json.loads(v) for k, v in proizvodi_raw.items()}

    # Sortiranje proizvoda na osnovu numOfCliks u opadajućem redosledu
    sortirani_proizvodi = sorted(proizvodi.values(), key=lambda x: x['numOfCliks'], reverse=True)

    # Vraćanje prvih 5 proizvoda
    prvih_5_proizvoda = sortirani_proizvodi[:5]

    return jsonify(prvih_5_proizvoda)


@redis_routes.route('/ucitajNajaktivnijeKorisnike', methods=['GET'])
def ucitajNajaktivnijeKorisnike():
    try:
        #  prvo čitanje iz keša
        najaktivniji_korisnici = redis_client.get("najaktivniji_korisnici")

        if najaktivniji_korisnici:
          
            najaktivniji_korisnici = json.loads(najaktivniji_korisnici)
            return jsonify(najaktivniji_korisnici)
        else:
            
            korisnici = Kupac.query.order_by(desc(Kupac.bodovi)).all()

            # Prikazujemo najviše 10 korisnika, ali možete prilagoditi prema potrebi
            broj_korisnika = 10
            najaktivniji_korisnici = [
                {
                    'ime': korisnik.ime,  
                    'prezime': korisnik.prezime,
                    'bodovi': korisnik.bodovi
                }
                for korisnik in korisnici[:broj_korisnika]
            ]

            # Konvertujemo listu u JSON format
            json_najaktivniji_korisnici = json.dumps(najaktivniji_korisnici)

            
            redis_client.setex("najaktivniji_korisnici", timedelta(minutes=30).seconds, json_najaktivniji_korisnici)

            return jsonify(najaktivniji_korisnici)

    except Exception as e:
        return jsonify({"error":str(e)})