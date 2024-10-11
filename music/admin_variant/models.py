from datetime import date, datetime
from django.db import models
from django.forms import ValidationError

from admin_products.models import Product

# Create your models here.
class Colors(models.Model):
    color_name = models.CharField(max_length=100)

    def __str__(self):
        return self.color_name
    
    
class Product_Variant(models.Model):
    thumbnail = models.ImageField(upload_to='variant_thumbnail',null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(blank=True)
    price = models.PositiveIntegerField(null=True)
    is_available = models.BooleanField(default=True,blank=True)

    def __str__(self) -> str:
        return str(self.product) + ' with ' + str(self.color) +  ' color'
    

class Variant_images(models.Model):
    variant = models.ForeignKey(Product_Variant,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='variant_images')

    def __str__(self) -> str:
        return 'image of ' + str(self.variant)

global current_date;
current_date = datetime.utcnow()

def validate_expiry_date(value):
    min_date = date.today()
    if value < min_date:
        raise ValidationError(
        (f"Expiry date cannot be earlier than {min_date}.")
        )

class Coupon(models.Model):
    name = models.CharField(max_length=15)
    min_amount = models.PositiveBigIntegerField(default=15000)
    discount_price = models.PositiveBigIntegerField(default = 799)
    is_expired = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.name