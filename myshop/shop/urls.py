from django.urls import path
from . import views


app_name = 'shop'


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('add-to-favorite/<int:product_id>/', views.add_to_favorite_ajax, name='add-to-favorite'),
    path('remove-from-favorite/<int:product_id>/', views.remove_from_favorite_ajax, name='remove-to-favorite'),

]