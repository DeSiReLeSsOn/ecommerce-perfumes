from django.contrib import admin
from .models import HomeBanner



@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ['maintitle','title','small_description','is_active']
    
    