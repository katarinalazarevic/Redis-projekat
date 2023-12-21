from flask import Flask
#from app.models import Probas
from database import init_db, db_session, redis_client
app1 = Flask(__name__)
init_db()

@app1.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def main():
   # u = Probas('admin2', 'admin@localhost2')
   # db_session.add(u)
   # db_session.commit()

    redis_client.set('kljuc1', 'vrednost1')
    value1 = redis_client.get('kljuc1')
    print(value1)
if __name__ == '__main__':
    main()