import redis
from django.conf import settings
from .models import Product 


#соединить с редис 
r = redis.Redis(host=settings.REDIS_HOST, port=set.REDIS_PORT, db=settings.REDIS_DB) 

class Recommender:
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'


    