from django.shortcuts import render, get_object_or_404, redirect
from store.models import product
from .models import Cart, CartItem, Coupon
from django.contrib.auth.decorators import login_required

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def add_to_cart(request, product_id):
    cart = get_cart(request)
    item = get_object_or_404(product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))


def decrease_cart(request, product_id):
    cart = get_cart(request)
    item = get_object_or_404(product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=item)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart_detail')


def remove_from_cart(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect('cart_detail')


def apply_coupon(request):
    cart = get_cart(request)
    if request.method == 'POST':
        code = request.POST.get('coupon')
        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)
            cart.coupon = coupon
        except Coupon.DoesNotExist:
            cart.coupon = None
        cart.save()
    return redirect('cart_detail')


def cart_detail(request):
    cart = get_cart(request)
    items = cart.items.all()
    return render(request, 'shoping-cart.html', {
        'cart': cart,
        'items': items
    })


@login_required(login_url='login')  # 🔥 forces login
def checkout(request):
    if request.method=="POST":
        return redirect('/') 

    cart = get_cart(request)
    items = cart.items.all() if cart else []

    return render(request, 'checkout.html', {
        'cart': cart,
        'items': items
    })