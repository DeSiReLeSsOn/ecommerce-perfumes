from django import forms
from .models import Banner

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['image', 'link', 'advertisement_text', 'is_active']