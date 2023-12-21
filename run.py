from flask import Flask
from app.models import Probas
from database import init_db, db_session

app1 = Flask(__name__)
init_db()

@app1.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def main():
    u = Probas('admin2', 'admin@localhost2')
    db_session.add(u)
    db_session.commit()
if __name__ == '__main__':
    main()