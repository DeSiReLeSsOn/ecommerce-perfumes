from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import OrderItem, Order
from .forms import OrderCreateForm
#from .tasks import order_created
from cart.cart import Cart
from django.contrib.auth.decorators import login_required 




def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            #order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process')) 
    else:
        form = OrderCreateForm() 
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
             
                 
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})



@login_required
def get_user_orders(request):
    orders = Order.objects.filter(user=request.user)
    order_items = OrderItem.objects.filter(order__user=request.user)
    return render(request, 'orders/order/order_list.html', {'orders': orders, 'order_items': order_items})

#@staff_member_required
"""def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order_id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')])
    return response"""