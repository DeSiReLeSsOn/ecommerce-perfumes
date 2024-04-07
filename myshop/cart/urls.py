from django.urls import path
from . import views


app_name = 'cart'


urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('ajax/add/<int:product_id>/', views.cart_add_ajax, name='cart_add_ajax'),
    path('ajax/remove/<int:product_id>/', views.cart_remove_ajax, name='cart_remove_ajax'),
    path('count/', views.cart_count, name='cart_count'),
    path('is-product-in-cart/<int:product_id>/', views.is_product_in_cart, name='is_product_in_cart'),
    
]