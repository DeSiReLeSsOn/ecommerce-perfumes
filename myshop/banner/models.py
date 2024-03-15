from django.db import models

class Banner(models.Model):
    image = models.ImageField(upload_to='banners/', blank=False)  # Поле для изображения
    link = models.CharField(max_length=200)  # Поле для ссылки
    advertisement_text = models.TextField(blank=True)  # Поле для текста рекламы
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.advertisement_text

