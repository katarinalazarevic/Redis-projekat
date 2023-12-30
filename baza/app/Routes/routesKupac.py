
import json
from flask import app, jsonify, request
from app.Models.modelsKupac import Kupac
from flask import Blueprint
from database import db_session,redis_client
from flasgger import swag_from
from flask_restful import Resource, Api, reqparse
#from run import api
from flask_bcrypt import bcrypt

kupac_routes = Blueprint('kupac_routes', __name__)




@kupac_routes.route('/dodajKupca', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'name': {'type': 'string'},
                    'email': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Kupac created successfully',
            'schema': {
                'properties': {
                    'message': {'type': 'string'},
                    'kupac_id': {'type': 'integer'}
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'schema': {
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def create_kupac():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({'message': 'Name and email are required'}), 400

    new_kupac = Kupac.create(name=name, email=email)
    return jsonify({'message': 'Kupac created successfully', 'kupac_id': new_kupac.id}),200


@kupac_routes.route('/vratiKupca/<int:kupac_id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'kupac_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID kupca'
        }
    ],
    'responses': {
        200: {
            'description': 'Success',
            'schema': {
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'email': {'type': 'string'}
                }
            }
        },
        404:{
            'description': 'Kupac not found'
  }
}
})
def get_kupac(kupac_id):

    kupac = Kupac.get_by_id(kupac_id)
    if not kupac:
        return jsonify({'message': 'Kupac not found'}), 404

    return jsonify({'id': kupac.id, 'name': kupac.ime, 'email':kupac.email})



@kupac_routes.route('/obrisiKupca/<int:kupacID>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'kupacID',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID kupca koji se briše'
        }
    ],
    'responses': {
        200: {
            'description': 'Kupac deleted successfully',
            'schema': {
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Not Found',
            'schema': {
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def obrisi_kupca_route(kupacID):
    try:
        if kupacID:
            kupac_za_brisanje = Kupac.get_by_id(kupacID)

            if kupac_za_brisanje:
                kupac_za_brisanje.delete()
                return jsonify({'message': f'Kupac {kupac_za_brisanje.name} is successfully deleted.'}), 200
            else:
                return jsonify({'message': 'Kupac not found!'}), 404
        else:
            return jsonify({'message': 'Invalid data! Kupac ID is required for deletion.'}), 400
    except Exception as e:
        return jsonify({'message': f'Internal Server Error: {str(e)}'}),500
    


    
@kupac_routes.route('/izmeniKupca/<int:kupacID>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'kupacID',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID kupca koji se ažurira'
        },
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'name': {'type': 'string'},
                    'email': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Kupac updated successfully',
            'schema': {
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'schema': {
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Not Found',
            'schema': {
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def izmeniKupca(kupacID):
    data = request.json
    novoIme = data.get('name')
    noviEmail = data.get('email')

    if novoIme is None or noviEmail is None:
        return jsonify({'message': 'Data is required for update!'}), 400

    kupac = Kupac.get_by_id(kupacID)
    
    if kupac:
        staroIme = kupac.name 
        kupac.name = novoIme
        kupac.email = noviEmail
        db_session.commit()
        return jsonify({'message': f'Kupac {staroIme} has a new name {kupac.name}.'}), 200
    else:
        return jsonify({'message': 'Kupac not found!'}),404



@kupac_routes.route('/register', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'ime': {'type': 'string'},
                    'prezime': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'},
                    'ulica': {'type': 'string'},
                    'grad': {'type': 'string'},
                    'broj': {'type': 'string'},
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Registracija uspešna',
            'schema': {
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'schema': {
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def register():
    data = request.get_json()
    ime = data.get('ime')
    prezime = data.get('prezime')
    email = data.get('email')
    password = data.get('password')
    ulica = data.get('ulica')
    grad = data.get('grad')
    broj = data.get('broj')
    existing_user = Kupac.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Korisnik sa datim emailom već postoji'}), 400
    # Kreiranje novog korisnika
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = Kupac(ime=ime, prezime=prezime, email=email, password_hash=password_hash, ulica=ulica, grad=grad, broj=broj)
    db_session.add(new_user)
    db_session.commit()
    return jsonify({'message': 'SUCCESS'}), 201

@kupac_routes.route('/login', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'},
                },
                'required': ['email', 'password']  # Obavezna polja
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Uspešna prijava',
            'schema': {
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        401: {
            'description': 'Pogrešan email ili šifra',
            'schema': {
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email i šifra su obavezni'}), 401

    # Provera korisnika
    user = Kupac.query.filter_by(email=email).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        redis_key = f"user"
        user_data_json = json.dumps({'email': user.email, 'id': user.id})

        redis_client.hset(redis_key,user.id, user_data_json)
        #redis_client.expire(redis_key, 900)  # Ističe nakon 15 minuta (900 sekundi)
        return jsonify({'message': 'SUCCESS'}), 200
    else:
        return jsonify({'message': 'FALSE'}), 401
