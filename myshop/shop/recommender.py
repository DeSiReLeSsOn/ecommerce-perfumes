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
                # увеличить балл товара, который принадлежит одному заказу
                r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_product_for(self, products, max_result=6):
        product_ids = [p.id for p in products] 
        if len(products) == 1:
            suggestions = r.zrange(self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_result] 
        else:
            # сгенерировать временный ключ
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # несколько товаров, объединить баллы всех товаров
            # сохранить полученное сортированное множество
            # во временном ключе
            keys = [self.get_product_key(id) for id in product_ids] 
            # удалить идентификаторы товаров,
            # для которых дается рекомендация
            r.zrem(tmp_key, *product_ids) 
            # получить идентификаторы товаров по их количеству,
            #сортировка по убыванию
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_result] 
            r.delete(tmp_key)
        suggested_product_ids = [int(id) for id in suggestions]
        # получить предлагаемые товары и
        # отсортировать их по порядку их появления
        suggested_products = list(Product.objects.filter(
            id__in=suggested_product_ids)) 
        suggested_products.sort(key=lambda x: suggested_product_ids.index(x.id))
        return suggested_products
