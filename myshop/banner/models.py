from django.db import models

class Banner(models.Model):
    image = models.ImageField("Изображение", upload_to='banners/', blank=False)  
    link = models.CharField("Ссылка", max_length=200)  
    advertisement_text = models.TextField("Текст рекламы", blank=True)  
    is_active = models.BooleanField("Активна/Неактивна", default=True) 

    def __str__(self):
        return self.advertisement_text

