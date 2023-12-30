from flask import Flask,jsonify,render_template
from flasgger import Swagger
from flask_cors import CORS
from flask_restful import Api
from app.CRUDKupci import azuriraj_kupca, obrisi_kupca
from app.Routes.routesKupac import Kupac
from database import init_db, db_session, redis_client
from app.Routes.routesKupac import kupac_routes
from app.Routes.routesProduct import product_routes
from app.Routes.redisRoutes import redis_routes

app1 = Flask(__name__)
api=Api(app1)
CORS(app1, resources={r"/*": {"origins": "http://localhost:3000"}})
swagger= Swagger(app1)
app1.register_blueprint(kupac_routes)
app1.register_blueprint(product_routes)
app1.register_blueprint(redis_routes)
# app1.register_blueprint(redis_routes1)
init_db()
@app1.route("/")
def home():
    return ('proba.html')
@app1.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
# def main():
#     

if __name__ == '__main__':
    #main()
    app1.run(debug=True)