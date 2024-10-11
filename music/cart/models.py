from django.db import models

from accounts.models import Customer
from admin_products.models import Product
from admin_variant.models import Coupon


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_items')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    razorpay_order_id = models.CharField(max_length=100 ,null=True, blank=True,unique=True)
    razorpay_payment_id = models.CharField(max_length=100 ,null=True, blank=True,unique=True)
    
    def get_cart_total(self):
        cart_items = CartItem.objects.filter(cart=self.id)
        price = []
        for cart_item in cart_items:
            quantity = cart_item.quantity
            price.append(cart_item.product.price * quantity)
        
        if self.coupon:
            return sum(price) - self.coupon.discount_price

        return sum(price)
    
    


    

class CartItem(models.Model):
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    quantity = models.PositiveIntegerField()
    
    def get_product_price(self):
        return self.product.price
    
    def get_item_total(self):
        total = self.product.price * self.quantity
        return total
    
    
    def __str__(self):
        return self.product.product_name
