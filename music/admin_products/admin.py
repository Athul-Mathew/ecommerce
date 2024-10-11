from django.contrib import admin

from admin_products.models import Product, ProductImage, ProductOffer

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductOffer)
