from django.db import models
from django.conf import settings
from store.models import product


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.PositiveIntegerField(help_text="Enter discount percentage",default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"

    @property
    def total_price(self):
        return sum(item.sub_total for item in self.items.all())

    @property
    def discount_amount(self):
        if self.coupon:
            return (self.total_price * self.coupon.discount) / 100
        return 0

    @property
    def final_price(self):
        return self.total_price - self.discount_amount


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.product_name

    @property
    def sub_total(self):
        return self.product.price * self.quantity