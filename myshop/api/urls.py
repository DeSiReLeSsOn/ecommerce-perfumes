from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet

router = routers.SimpleRouter()
router.register(r'product', ProductViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]