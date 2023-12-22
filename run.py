from flask import Flask
from app.CRUDKupci import azuriraj_kupca, obrisi_kupca
#from  import kupac_routes
from app.routesKupac import Kupac
#from app.models import Probas
from database import init_db, db_session, redis_client
from app.routesKupac import kupac_routes



app1 = Flask(__name__)
app1.register_blueprint(kupac_routes)
init_db()

@app1.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':

    #main()
    app1.run(debug=True)