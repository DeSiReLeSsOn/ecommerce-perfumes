from django.db import models
from django.contrib.auth import get_user_model




User = get_user_model()

class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField("Отзыв")
    created = models.DateTimeField("Создан",auto_now_add=True)
    updated = models.DateTimeField("Обновлен",auto_now=True)
