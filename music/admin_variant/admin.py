from django.contrib import admin

# Register your models here.
from .models import Variant_images,Product_Variant,Coupon

admin.site.register(Variant_images)
admin.site.register(Coupon)