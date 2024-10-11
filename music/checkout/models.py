from django.db import models

from accounts.models import Customer
from admin_products.models import Product
from user_profile.models import AddressDetails

# Create your models here.

class Payment(models.Model):

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)

    transaction_id = models.CharField(max_length=100)

    cart_total = models.PositiveIntegerField()

   

  

    payment_method = models.CharField(max_length=30, default='RazorPay')

    is_paid = models.BooleanField(default=True)

    paid_date = models.DateTimeField(auto_now_add=True)



    def _str_(self) -> str:

        return self.transaction_id
    

class Order(models.Model):

    order_id = models.CharField(max_length=100, unique=True)

    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

   

    delivery_address = models.ForeignKey(AddressDetails, on_delete=models.SET_NULL, null=True)

    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)

    ordered_date = models.DateTimeField(auto_now_add=True, editable=False)



    def _str_(self) -> str:

        return f'{self.id} of {self.user}'    
    



class OrderItem(models.Model):
    STATUS = (
        ('Ordered', 'Ordered'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded')
    )
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    order_status = models.CharField(max_length=20, choices=STATUS, default='Ordered')
    item_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    item_total = models.PositiveIntegerField()

    def __str__(self):
        return self.product.product_name  