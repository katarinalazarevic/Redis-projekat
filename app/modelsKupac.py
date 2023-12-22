from sqlalchemy import Column, Integer, String
from database import Base, db_session

class Kupac(Base):
    __tablename__ = 'Kupac'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50), unique=False)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'
    
    @staticmethod
    def create(name, email):
     new_kupac = Kupac(name=name, email=email)
     db_session.add(new_kupac)
     db_session.commit()
     return new_kupac


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

    # def delete(self):
    #     db_session.delete(self)
    #     db_session.commit()