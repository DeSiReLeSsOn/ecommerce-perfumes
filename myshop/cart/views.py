from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from django.http.response import JsonResponse




@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')
@require_POST
def cart_add_ajax(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1, override_quantity=False)
    return JsonResponse({'success': True})


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@require_POST
def cart_remove_ajax(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    data = JsonResponse({'success': True})
    return data








    


def cart_detail(request, json=False, product_id=None):
    cart = Cart(request)
    cart_products = [item['product'] for item in cart]
    if json:
        total_items = len(cart)
        return JsonResponse({'total_items': total_items})
    elif product_id:
        product = get_object_or_404(Product, id=product_id)
        if product in cart_products:
            return JsonResponse({'inCart': True})
        else:
            return JsonResponse({'inCart': False})
    else:
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={
                                'quantity': item['quantity'],
                                'override': True})
        coupon_apply_form = CouponApplyForm()
        return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})


    
