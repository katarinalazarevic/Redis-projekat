import json
from flask import Blueprint, request
from app.Models.modelsKatalog import Proizvod
from database import db_session,redis_client
from sqlalchemy.orm import class_mapper
from flasgger import swag_from


redis_routes1 = Blueprint('redis_routes1', __name__)
# class Redis:
#     @staticmethod
def as_dict(obj):
    return {column.key: getattr(obj, column.key) for column in class_mapper(obj.__class__).mapped_table.c}

    
    #@redis_routes.route('/products_by_category', methods=['GET'])
@redis_routes1.route('/products_by_category', methods=['GET'])
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