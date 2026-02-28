from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,get_object_or_404
from .models import product,category
from cart.models import product, Cart, CartItem

def home(request):
    products = product.objects.filter(is_available=True)
    sort = request.GET.get('sort')
    search_query = request.GET.get('search')  # get search keyword

    if search_query:
        products = products.filter(product_name__icontains=search_query)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_date')

    return render(request, 'index.html', {'products': products, 'sort': sort, 'search': search_query})


def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request,'contact.html')



def shop(request,category_slug=None):
    sort = request.GET.get('sort')
    search_query = request.GET.get('search')  # get search keyword

    if search_query:
        products = products.filter(product_name__icontains=search_query)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_date')

    products=None
    categories=None
    if category_slug!=None:
        categories=get_object_or_404(category,slug=category_slug)
        products=product.objects.filter(category=categories,is_available=True)
        return render(request,'product.html',{'products':products})
    products=product.objects.filter(is_available=True)
    return render(request,'product.html',{'products':products, 'sort': sort, 'search': search_query})


def product_details(request, category_slug, product_slug):
    try:
        single_item = product.objects.get(category__slug=category_slug, slug=product_slug)
    except product.DoesNotExist:
        return render(request, '404.html')  # or redirect somewhere

    # Get current cart
    cart = None
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)

    # Check if this product is already in cart
    in_cart = False
    if cart:
        in_cart = CartItem.objects.filter(cart=cart, product=single_item).exists()

    return render(request, 'product-detail.html', {
        'single_item': single_item,
        'in_cart': in_cart,
    })
# Features page
def features(request):
    return render(request, 'shoping-cart.html')  