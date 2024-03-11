from django.shortcuts import render
from .models import Banner
from .forms import BannerForm

def create_banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = BannerForm()
    
    return render(request, 'create_banner.html', {'form': form})
