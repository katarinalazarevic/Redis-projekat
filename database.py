import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import redis
from redis import Redis

engine = create_engine('postgresql://postgres:petarbaze@localhost/Projekat1') #konekcija sa bazom
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

redis_client = Redis(host='localhost', port=6379, decode_responses=True)

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import app.models
    #kreiranje tabela
    Base.metadata.create_all(bind=engine)