from django.urls import path
from .views import home, about, shop, features,contact,product_details

urlpatterns = [
    path('',home, name='home'),
    path('about/',about, name='about'),
    path('shop/',shop, name='shop'),
    path('contact/',contact,name='contact'),
    path('features/',features, name='features'),
    path('shop/<slug:category_slug>/',shop, name='products_by_category'),
    path('shop/<slug:category_slug>/<slug:product_slug>/',product_details, name='single_product'),

]