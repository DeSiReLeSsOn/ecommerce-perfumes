from django import template
from banner.models import Banner
import random



register = template.Library()

@register.inclusion_tag('shop/banner.html')
def show_banner(is_homepage=False):
    if is_homepage == True:
        banner = Banner.objects.filter(is_active=True)
        random_banner = random.choice(banner)
        return {"random_banner": random_banner}
    else:
        return {}