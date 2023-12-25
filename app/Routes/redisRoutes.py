from flask import Blueprint
from app.Models.modelsKatalog import Proizvod
from app.Models.modelsRedis import RedisService

redis_routes = Blueprint('redis_routes', __name__)

@redis_routes.route('/dodavanjeProizvodaUKorpu/<int:product_id>', methods=['GET'])
def dodavanjeProizvodaUKorpu(product_id):
    """
    Upisuje proizvod u Redis na temelju proslijeđenog ID-a.

    ---
    parameters:
      - in: path
        name: produc_id
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
        redis_service = RedisService()
        redis_service.UpisiProizvodUKorpu(product_id)
        redis_service.close_connection()
        return "Proizvod uspješno upisan u Redis.", 200
    except Exception as e:
        return f"Greška prilikom upisa proizvoda u Redis: {str(e)}", 500

@redis_routes.route('/provjera_proizvoda_u_redisu/<int:produc_id>', methods=['GET'])
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
