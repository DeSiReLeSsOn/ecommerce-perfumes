from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product 
from cart.forms import CartAddProductForm 
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q, Max, Min
from banner.models import Banner
from .models import FavoriteProduct
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from cart.context_processors import *





"""def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    product = Product.objects.filter(available=True)
    paginator = Paginator(product, 3) 
    page_number = request.GET.get('page', 1)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = product.filter(category=category)
    return render(request, 
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories, 
                   'products': products})"""


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)  
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)


    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})



def product_detail(request, id, slug):
    product = get_object_or_404(Product, 
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


"""def search(request):
	query = request.POST.get('q')
	products = Product.objects.filter(name__icontains=query).all()
	return render(request, 'shop/product/list.html', {'products': products}) """

def search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'shop/product/list.html', {'products': products})

def index(request):
    #banners = Banner.objects.filter(is_active=True)
    banners = Banner.objects.all()
    return render(request, 'shop/banner.html', {'banners': banners})



@login_required
def add_to_favorite_ajax(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite_product, created = FavoriteProduct.objects.get_or_create(user=request.user, product=product)
    if created:
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
def remove_from_favorite_ajax(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    removed = FavoriteProduct.objects.filter(user=request.user, product=product).delete()
    
    if removed:
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})



