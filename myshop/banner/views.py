from django.shortcuts import render
from banner.models import Banner


def index(request):
    #banners = Banner.objects.filter(is_active=True).first()
    banners = Banner.objects.all()
    return render(request, 'banner.html', {'banners': banners})