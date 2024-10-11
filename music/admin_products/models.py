from django.db import models

from admin_brand.models import Brand
from admin_category.models import Category

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    # slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    # size = models.ForeignKey(Prodectsize, on_delete=models.CASCADE,null=True)
    images1 = models.ImageField(upload_to='uploads')

    stock = models.IntegerField(null=True)

    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)

    def __str__(self):

        return self.product_name


class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    offer_price = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return f'{self.product.product_name} Image'
