from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Category, Product 
from cart.forms import CartAddProductForm 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q, Max, Min
from banner.models import Banner
from .models import FavoriteProduct
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from cart.views import is_product_in_cart
from cart.cart import Cart
import json




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



# def product_list(request, category_slug=None, template_name='shop/product/list.html'):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)

#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)

#     # Pagination
#     paginator = Paginator(products, 9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     inCart = []
#     for product in products:
#         response = is_product_in_cart(request, product.id)
#         response_content = json.loads(response.content.decode('utf-8'))
#         if response_content.get('inCart', False):
#             inCart.append(product.id)

#     if request.user.is_authenticated:
#         favorite_products = FavoriteProduct.objects.filter(user=request.user).values_list('product_id', flat=True)
#         return render(request, template_name,
#                     {'category': category,
#                     'categories': categories,
#                     'page_obj': page_obj,
#                     'favorite_products': favorite_products,
#                     'inCart': inCart
#                     })
#     return render(request, 'shop/product/list.html',
#                     {'category': category,
#                     'categories': categories,
#                     'page_obj': page_obj,
#                     'inCart': inCart
#                     })







# def product_list(request, category_slug=None, template_name='shop/product/list.html'):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)

#     is_favorites = request.GET.get('is_favorites', False) == 'True'

#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)

#     # Фильтрация продуктов по избранным товарам пользователя
#     if request.user.is_authenticated and is_favorites:
#         favorite_products = FavoriteProduct.objects.filter(user=request.user).values_list('product_id', flat=True)
#         products = products.filter(id__in=favorite_products)

#     # Pagination
#     paginator = Paginator(products, 9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Создаем список товаров, которые находятся в корзине пользователя
#     inCart = []
#     for product in products:
#         response = is_product_in_cart(request, product.id)
#         response_content = json.loads(response.content.decode('utf-8'))
#         if response_content.get('inCart', False):
#             inCart.append(product.id)

#     if request.user.is_authenticated:
#         favorite_products = FavoriteProduct.objects.filter(user=request.user).values_list('product_id', flat=True)

#     context = {
#         'category': category,
#         'categories': categories,
#         'page_obj': page_obj,
#         'inCart': inCart,
#     }

#     if request.user.is_authenticated:
#         context['favorite_products'] = favorite_products

#     return render(request, template_name, context)










# def product_list(request, category_slug=None, template_name='shop/product/list.html'):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)

#     is_favorites = request.GET.get('is_favorites', False) == 'True'

#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)

#     # Фильтрация продуктов по избранным товарам пользователя
#     if request.user.is_authenticated and is_favorites:
#         favorite_products = FavoriteProduct.objects.filter(user=request.user).values_list('product_id', flat=True)
#         products = products.filter(id__in=favorite_products)

#     # Сортировка товаров
#     sort_by = request.GET.get('sort_by', 'name')  # Use 'name' as the default sort order
#     if sort_by == 'price-asc':
#         products = products.order_by('price')
#     elif sort_by == 'price-desc':
#         products = products.order_by('-price')
#     elif sort_by == 'views-desc':
#         products = products.order_by('-views_count')
#     elif sort_by == 'search-desc':
#         products = products.order_by('-search_count')
#     else:
#         products = products.order_by(sort_by)

#     # Pagination
#     paginator = Paginator(products, 9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Создаем список товаров, которые находятся в корзине пользователя
#     inCart = []
#     for product in products:
#         response = is_product_in_cart(request, product.id)
#         response_content = json.loads(response.content.decode('utf-8'))
#         if response_content.get('inCart', False):
#             inCart.append(product.id)

#     if request.user.is_authenticated:
#         favorite_products = FavoriteProduct.objects.filter(user=request.user).values_list('product_id', flat=True)

#     context = {
#         'category': category,
#         'categories': categories,
#         'page_obj': page_obj,
#         'inCart': inCart,
#         'sort_by': sort_by,
#     }

#     if request.user.is_authenticated:
#         context['favorite_products'] = favorite_products

#     return render(request, template_name, context)





def product_list(request, category_slug=None, template_name='shop/product/list.html'):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    is_favorites = request.GET.get('is_favorites', False) == 'True'

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Фильтрация продуктов по избранным товарам пользователя
    if request.user.is_authenticated and is_favorites:
        favorite_products = FavoriteProduct.objects.filter(user=request.user).values_list('product_id', flat=True)
        products = products.filter(id__in=favorite_products)


    # Сортировка товаров
    sort_by = request.GET.get('sort_by', 'name')  # Use 'name' as the default sort order
    if sort_by == 'price-asc':
        products = products.order_by('price')
    elif sort_by == 'price-desc':
        products = products.order_by('-price')
    elif sort_by == 'views-desc':
        products = products.order_by('-views_count')
    elif sort_by == 'search-desc':
        products = products.order_by('-search_count')
    else:
        products = products.order_by(sort_by)

    



    # Pagination
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Создаем список товаров, которые находятся в корзине пользователя
    inCart = []
    for product in products:
        response = is_product_in_cart(request, product.id)
        response_content = json.loads(response.content.decode('utf-8'))
        if response_content.get('inCart', False):
            inCart.append(product.id)

    if request.user.is_authenticated:
        favorite_products = FavoriteProduct.objects.filter(user=request.user).values_list('product_id', flat=True)

    context = {
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
        'inCart': inCart,
        'sort_by': sort_by,
    }

    if request.user.is_authenticated:
        context['favorite_products'] = favorite_products

    return render(request, template_name, context)









def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)

    # Обновление счетчика просмотров товара
    product.views_count += 1
    product.save()

    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})



"""def search(request):
	query = request.POST.get('q')
	products = Product.objects.filter(name__icontains=query).all()
	return render(request, 'shop/product/list.html', {'products': products}) """

# def search(request):
#     query = request.GET.get('q')
#     if query:
#         products = Product.objects.filter(name__icontains=query)
#     else:
#         products = Product.objects.all()


#     paginator = Paginator(products, 9)  # 9 products per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'shop/product/list.html', {'page_obj': page_obj, 'query': query})


def search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)

        # Обновление счетчика поисковых запросов для товаров
        for product in products:
            product.search_count += 1
            product.save()

        # Сортировка товаров по частоте поиска
        products = products.order_by('-search_count')
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 9)  # 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/product/list.html', {'page_obj': page_obj, 'query': query})


# def brands(request):

#     categories = Category.objects.all()

#     # Pagination
#     paginator = Paginator(categories, 9)  # 9 categories per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'shop/brands.html', {'page_obj': page_obj})

# def index(request):
#     #banners = Banner.objects.filter(is_active=True)
#     banners = Banner.objects.all()
#     return render(request, 'shop/banner.html', {'banners': banners})


def brands(request, category_slug=None):
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        categories = categories.filter(slug=category_slug)

    # Pagination
    paginator = Paginator(categories, 9)  # 9 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'category_slug': category_slug,
    }

    return render(request, 'shop/brands.html', context)



def add_to_favorite_ajax(request, product_id):
    user = request.user

    if user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        favorite_product, created = FavoriteProduct.objects.get_or_create(user=request.user, product=product)

        if created:
            return JsonResponse({'success': True, 'authenticated': True})
        
        return JsonResponse({'success': False, 'authenticated': True})
    
    else:
        login_url = reverse('account:login')
        return JsonResponse({'authenticated': False, 'redirect': login_url})




@login_required
def remove_from_favorite_ajax(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    removed = FavoriteProduct.objects.filter(user=user, product=product).delete()
    
    if removed:
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})



def favorite_products(request, template_name='shop/product/list.html'):
    if not request.user.is_authenticated:
        return redirect('account:login')

    favorite_products_ids = FavoriteProduct.objects.filter(user=request.user).values_list('product_id', flat=True)
    products = Product.objects.filter(id__in=favorite_products_ids, available=True)

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    in_cart = []
    for product in products:
        if product.id in favorite_products_ids:
            in_cart.append(product.id)

    context = {
        'category': None,
        'categories': Category.objects.all(),
        'page_obj': page_obj,
        'in_cart': in_cart,
    }

    if request.user.is_authenticated:
        context['favorite_products'] = favorite_products_ids

    return render(request, template_name, context)