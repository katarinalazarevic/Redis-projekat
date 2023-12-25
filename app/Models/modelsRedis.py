import redis
from app.Models.modelsKatalog import Proizvod

class RedisService:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    @staticmethod
    def UpisiProizvodUKorpu(ID):
        proizvod = Proizvod.get_by_id(ID)  

        if proizvod:
            product_id = proizvod.id
            product_name = proizvod.producerName

            
            RedisService().r.set(f'product:{product_id}', product_name)
        else:
            print("Proizvod s traženim ID-om nije pronađen.")


    @staticmethod
    def procitajProizvodIzKorpe(product_id):
        product_name = RedisService().r.get(f'product:{product_id}')
        if product_name:
            return f"Proizvod s ID-om {product_id} pronađen u Redisu: {product_name.decode('utf-8')}"
        else:
            return f"Proizvod s ID-om {product_id} nije pronađen u Redisu."

    def close_connection(self):
        self.r.close()
