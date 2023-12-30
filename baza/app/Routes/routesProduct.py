import json
from flask import app, jsonify, request
from app.Models.modelsKatalog import Proizvod
from app.Models.modelsKupac import Kupac
from flask import Blueprint
from database import db_session,redis_client
from flasgger import swag_from

product_routes = Blueprint('product_routes', __name__)

@product_routes.route('/vratiProizvode', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Success',
            'schema': {
                'properties': {
                    'proizvodi': {
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
                                'discount': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        },
        404: {
            'description': 'Proizvodi not found',
            'schema': {
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def get_products():
    proizvodi=Proizvod.getAll()
    if not proizvodi:
        return jsonify({'message': 'Proizvodi not found'}), 404

    proizvodi_lista = []
    for proizvod in proizvodi:
        proizvodi_lista.append({
            'id': proizvod.id,
            'producerName': proizvod.producerName,
            'productDescription': proizvod.productDescription,
            'category': proizvod.category,
            'price': proizvod.price,
            'numOfCliks': proizvod.numOfCliks,
            'picture': proizvod.picture,
            'discount': proizvod.discount,
            'quantity':proizvod.quantity
        })

    return jsonify({'proizvodi': proizvodi_lista})

def ucitajProizvode():
    proizvodi_iz_baze = db_session.query(Proizvod).all()
    for proizvod in proizvodi_iz_baze:
        redis_key = f'proizvodi'
        proizvod_data = {
            'producerName': proizvod.producerName,
            'productDescription': proizvod.productDescription,
            'category': proizvod.category,
            'price': proizvod.price,
            'discount': proizvod.discount,
            'quantity': proizvod.quantity
        }
        atributi_proizvoda = proizvod.toDict()
        redis_client.hset(redis_key, proizvod.id, json.dumps(atributi_proizvoda, default=str))
        

@product_routes.route('/dodajProizvod', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'producerName': {'type': 'string'},
                    'productDescription': {'type': 'string'},
                    'category': {'type': 'string'},
                    'price': {'type': 'integer'},
                    'picture': {'type': 'string'},
                    'discount': {'type': 'integer', 'description': 'Popust na proizvod'},
                    'quantity': {'type': 'integer'},
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Uspešno dodat proizvod',
            'schema': {
                'properties': {
                    'message': {'type': 'string', 'description': 'Poruka o uspehu'},
                    'proizvod_id': {'type': 'integer', 'description': 'ID dodatog proizvoda'}
                }
            }
        },
        '400': {
            'description': 'Neuspešan zahtev',
            'schema': {
                'properties': {
                    'message': {'type': 'string', 'description': 'Poruka o grešci'}
                }
            }
        }
    },
    'request_body': {
        'required': True,
        'content': {
            'application/json': {
                'example': {
                    'producerName': 'Proizvođač',
                    'productDescription': 'Opis proizvoda',
                    'category': 'Kategorija',
                    'price': 100,
                    'picture': 'slika.jpg',
                    'discount': 10,
                    'quantity': 100
                }
            }
        }
    }
})
def dodaj_proizvod():
    data = request.get_json()

    producer_name = data.get('producerName')
    product_description = data.get('productDescription')
    category = data.get('category')
    price = data.get('price')
    picture = data.get('picture')
    discount = data.get('discount', 0)
    quantity = data.get('quantity', 0)

    if not producer_name or not price:
        return jsonify({'message': 'Nedostaju neophodni podaci!'}), 400

    novi_proizvod = Proizvod.create(
        producerName=producer_name,
        productDescription=product_description,
        category=category,
        price=price,
        picture=picture,
        discount=discount,
        quantity=quantity
    )

    return jsonify({'message': 'Proizvod uspešno dodat', 'proizvod_id': novi_proizvod.id}), 201

@product_routes.route('/izmeniProizvod/<int:proizvodID>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'proizvodID',
            'in': 'path',
            'description': 'ID proizvoda koji se izmenjuje',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'quantity': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Uspešno izmenjen proizvod',
            'schema': {
                'properties': {
                    'message': {'type': 'string', 'description': 'Poruka o uspehu'}
                }
            }
        },
        '404': {
            'description': 'Proizvod nije pronađen',
            'schema': {
                'properties': {
                    'message': {'type': 'string', 'description': 'Poruka o grešci'}
                }
            }
        }
    },
    'request_body': {
        'required': True,
        'content': {
            'application/json': {
                'example': {
                    'quantity': 50
                }
            }
        }
    }
})
def izmeni_proizvod(proizvodID):
    data = request.get_json()
    quantity = data.get('quantity')

    if quantity is None:
        return jsonify({'message': 'Nedostaje količina za izmenu!'}), 400

    proizvod = Proizvod.get_by_id(proizvodID)
    if proizvod:
        proizvod.quantity = quantity
        db_session.commit()
        return jsonify({'message': 'Proizvod uspešno izmenjen'}), 200
    else:
        return jsonify({'message': 'Proizvod nije pronađen!'}), 404
    
@product_routes.route('/obrisiProizvod/<int:proizvodID>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'proizvodID',
            'in': 'path',
            'description': 'ID proizvoda koji se briše',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        '200': {
            'description': 'Uspešno obrisan proizvod',
            'schema': {
                'properties': {
                    'message': {'type': 'string', 'description': 'Poruka o uspehu'}
                }
            }
        },
        '404': {
            'description': 'Proizvod nije pronađen',
            'schema': {
                'properties': {
                    'message': {'type': 'string', 'description': 'Poruka o grešci'}
                }
            }
        }
    }
})
def obrisi_proizvod(proizvodID):
    """
    Endpoint za brisanje proizvoda.

    ---
    tags:
      - Proizvodi
    parameters:
      - name: proizvodID
        in: path
        description: ID proizvoda koji se briše
        required: true
        type: integer
    responses:
      200:
        description: Proizvod uspešno obrisan
      404:
        description: Proizvod nije pronađen
    """
    proizvod = Proizvod.get_by_id(proizvodID)
    if proizvod:
        proizvod.delete()
        return jsonify({'message': f'Proizvod {proizvod.productDescription} uspešno obrisan'}), 200
    else:
        return jsonify({'message': 'Proizvod nije pronađen!'}), 404