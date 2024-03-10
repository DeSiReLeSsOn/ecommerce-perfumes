from django.db import models
from shop.models import Product


# Create your models here.
class HomeBanner(models.Model):
    maintitle = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    shop_link = models.URLField(null=True,blank=True,max_length=300)
    small_description = models.CharField(max_length=300)
    background_image = models.ImageField(upload_to="home_banner", help_text="1920x801 px image for fit background")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    
    