from flask import jsonify
from sqlalchemy import Column, Integer, String
from database import Base, db_session

class Proizvod(Base):
    __tablename__= 'KatalogProizvoda'
    id = Column(Integer, primary_key=True,autoincrement=True)
    producerName=Column(String(50), unique=False)
    productDescription = Column(String(50), unique=False) #mleko 300ml
    category=Column(String(50), unique=False)
    price = Column(Integer, unique=False)
    numOfCliks = Column(Integer, default=0, nullable=True)
    picture=Column(String(50), unique=False)# jaje.jpg "imeProizvida".jpg
    discount=Column(Integer, unique=False)
    quantity=Column(Integer, unique=False)

    def toDict(self):
        return {
            'id': self.id,
            'producerName': self.producerName,
            'productDescription': self.productDescription,
            'category': self.category,
            'price': self.price,
            'numOfCliks': self.numOfCliks,
            'picture': self.picture,
            'discount': self.discount,
            'quantity': self.quantity
        }
    @classmethod
    def fromDict(cls, data):
        return cls(**data)
    def __init__(self, producerName,productDescription=None, category=None,
                 price=0,picture=None, discount=0,quantity=None):
        self.producerName=producerName
        self.productDescription=productDescription
        self.category=category
        self.price=price
        self.numOfCliks=0
        self.picture=picture
        self.discount=discount
        self.quantity=quantity

    @staticmethod
    def create(producerName,productDescription,category,price,picture,discount,quantity):
        newProduct=Proizvod(producerName,productDescription=productDescription,category=category,price=price,picture=picture,discount=discount,quantity=quantity)
        db_session.add(newProduct)
        db_session.commit()
        return newProduct
    
    @staticmethod
    def getAll():
       return Proizvod.query.all()
    
    @staticmethod
    def get_by_id(produc_id):
        proizvod = Proizvod.query.filter_by(id=produc_id).first()
        return proizvod
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()


    
    
    