
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from payment import webhooks
from django_email_verification import urls as email_urls 




urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('email/', include(email_urls), name='email-verification'),
    path('banner/', include('banner.urls', namespace='banner')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('api/', include('api.urls', namespace='api')),
    path('', include('shop.urls', namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)