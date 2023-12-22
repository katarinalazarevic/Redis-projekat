from flask import app, jsonify, request
from app.modelsKupac import Kupac
from flask import Blueprint
from database import db_session

kupac_routes = Blueprint('kupac_routes', __name__)




@kupac_routes.route('/dodajKupca', methods=['POST'])
def create_kupac():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({'message': 'Name and email are required'}), 400

    new_kupac = Kupac.create(name=name, email=email)
    return jsonify({'message': 'Kupac created successfully', 'kupac_id': new_kupac.id}), 201



@kupac_routes.route('/vratiKupca/<int:kupac_id>', methods=['GET'])
def get_kupac(kupac_id):
    kupac = Kupac.get_by_id(kupac_id)
    if not kupac:
        return jsonify({'message': 'Kupac not found'}), 404

    return jsonify({'id': kupac.id, 'name': kupac.name, 'email': kupac.email})





@kupac_routes.route('/obrisiKupca/<int:kupacID>', methods=['DELETE'])
def obrisi_kupca_route(kupacID):
    data = request.get_json()
    

    if kupacID:
        kupac_za_brisanje = Kupac.get_by_id(kupacID)

        if kupac_za_brisanje:
            kupac_za_brisanje.delete()
            return jsonify({'message': f'Kupac {kupac_za_brisanje.name} je uspešno obrisan.'}), 200
        else:
            return jsonify({'message': 'Kupac nije pronađen!'}), 404
    else:
        return jsonify({'message': 'Neispravni podaci! Potreban je ID kupca za brisanje.'}), 400
    


    
@kupac_routes.route('/izmeniKupca/<int:kupacID>', methods=['PUT'])
def izmeniKupca(kupacID):
    data = request.json
    novoIme = data.get('name')
    noviEmail = data.get('email')

    if novoIme is None or noviEmail is None:
        return jsonify({'message': 'Potrebni su podaci za ažuriranje!'}), 400

    kupac = Kupac.get_by_id(kupacID)
    
    if kupac:
        staroIme = kupac.name
        kupac.name = novoIme
        kupac.email = noviEmail
        db_session.commit()
        return jsonify({'message': f'Kupac {staroIme} je dobio novo ime {kupac.name}.'}), 200
    else:
        return jsonify({'message': 'Kupac nije pronađen!'}), 404

