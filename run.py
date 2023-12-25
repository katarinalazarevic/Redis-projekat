from flask import Flask,jsonify
from flasgger import Swagger
from flask_restful import Api
from app.CRUDKupci import azuriraj_kupca, obrisi_kupca
#from  import kupac_routes
from app.Routes.routesKupac import Kupac
#from app.models import Probas
from database import init_db, db_session, redis_client
from app.Routes.routesKupac import kupac_routes
from app.Routes.routesProduct import product_routes
from app.Routes.redisRoutes import redis_routes

app1 = Flask(__name__)
api=Api(app1)
swagger= Swagger(app1)
app1.register_blueprint(kupac_routes)
app1.register_blueprint(product_routes)
app1.register_blueprint(redis_routes)
init_db()

@app1.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
#def main():

    #redis_client.set('kljuc', 'vrednost')

# Čitanje podatka iz Redis
 #   procitana_vrednost = redis_client.get('kljuc')

   # print(f'Pročitana vrednost: {procitana_vrednost}')

if __name__ == '__main__':
    #main()
    #main()
    app1.run(debug=True)