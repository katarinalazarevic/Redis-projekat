import bcrypt
from flask import jsonify, request
from sqlalchemy import Column, Integer, String
from database import Base, db_session

class Kupac(Base):
    __tablename__ = 'Kupac'
    id = Column(Integer, primary_key=True,autoincrement=True)
    ime = Column(String(50), nullable=False)
    prezime = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    ulica = Column(String(100))
    grad = Column(String(50))
    broj = Column(String(10))
    bodovi=Column(Integer, default=0,unique=False,nullable=True)
    
    
    def __init__(self, ime, prezime, email, password_hash, ulica, grad, broj):
        self.ime = ime
        self.prezime = prezime
        self.email = email
        self.password_hash =password_hash
        self.ulica = ulica
        self.grad = grad
        self.broj = broj
        self.bodovi=0

    def __repr__(self):
        return f'<User {self.name!r}>'
    
    # @staticmethod
    # def create(name, email):
    #  new_kupac = Kupac(name=name, email=email)
    #  db_session.add(new_kupac)
    #  db_session.commit()
    #  return new_kupac

   
    @staticmethod
    def get_by_id(kupac_id):
        kupac = Kupac.query.filter_by(id=kupac_id).first()
        return kupac

    # @staticmethod
    # def get_all():
    #     return Kupac.query.all()
        

    # def update(self, name=None, email=None):
    #     if name:
    #         self.name = name
    #     if email:
    #         self.email = email
    #     db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()