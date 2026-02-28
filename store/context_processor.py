from .models import category
from cart.models import Cart, CartItem

def cart_context(request):
    # Get or create cart
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)

    # Get cart items
    cart_items = cart.items.all() if cart else []

    # Calculate total quantity and total price
    cart_count = sum(item.quantity for item in cart_items)
    cart_total = sum(item.sub_total for item in cart_items)

    return {
        'cart': cart,
        'cart_items': cart_items,
        'cart_count': cart_count,
        'cart_total': cart_total,
    }

def menu_links(request):
    links=category.objects.all()
    return dict(links=links)
