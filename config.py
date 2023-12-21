import os
import psycopg2


class Config:
    # SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/database_name'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # REDIS_URL = 'redis://host.docker.internal:6379/0'
    conn = psycopg2.connect(database = "Projekat1", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "petarbaze",
                        port = 5432)