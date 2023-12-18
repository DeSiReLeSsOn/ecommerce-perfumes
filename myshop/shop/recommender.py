import redis
from django.conf import settings
from .models import Product 


#соединить с редис 
r = redis.Redis(host=settings.REDIS_HOST, port=set.REDIS_PORT, db=settings.REDIS_DB) 

class Recommender:
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'


    def product_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            # получить другие товары, купленные
            # вместе с каждым товаром
            if product_id != with_id:
                # увеличить балл товара,купленного вместе
                r.zincrby(self.get_product_key(product_id), 1, with_id)
