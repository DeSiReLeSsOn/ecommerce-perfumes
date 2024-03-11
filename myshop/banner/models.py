from django.db import models

class Banner(models.Model):
    image = models.ImageField(upload_to='banners/', blank=True)  # Поле для изображения
    link = models.CharField(max_length=200)  # Поле для ссылки
    advertisement_text = models.TextField(blank=True)
    is_active = models.BooleanField(default=True) # Поле для текста рекламы

    def __str__(self):
        return self.advertisement_text

