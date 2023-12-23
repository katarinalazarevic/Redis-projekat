from flask import app, jsonify, request
from app.modelsKupac import Kupac
from flask import Blueprint
from database import db_session
from flasgger import swag_from

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



# @kupac_routes.route('/vratiKupca/<int:kupac_id>', methods=['GET'])
# def get_kupac(kupac_id):
#     kupac = Kupac.get_by_id(kupac_id)
#     if not kupac:
#         return jsonify({'message': 'Kupac not found'}), 404

#     return jsonify({'id': kupac.id, 'name': kupac.name, 'email': kupac.email})

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
    """
    Get information about a specific kupac.

    :param kupac_id: ID of the kupac
    :type kupac_id: int
    :return: Information about the kupac
    :rtype: dict
    """
    kupac = Kupac.get_by_id(kupac_id)
    if not kupac:
        return jsonify({'message': 'Kupac not found'}), 404

    return jsonify({'id': kupac.id, 'name': kupac.name, 'email':kupac.email})



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

