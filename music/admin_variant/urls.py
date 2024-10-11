from django.urls import path

from admin_products.views import add_product_offer, delete_product_offer
from .views import *
from .coupon_view import *

urlpatterns = [
    path('',product_variants,name= 'product_variants'),
    path('add_color',add_color,name= 'add_color'),
    path('add_variant',add_variant,name= 'add_variant'),
    path('edit_variant/<int:variant_id>',edit_variant,name= 'edit_variant'),
    path('delete_variant',delete_variant,name= 'delete_variant'),
    path('upload_images',upload_images,name='upload_images'),   
    path('coupons/', coupon_list, name='coupon_list'),
    path('coupons/add/', add_coupon, name='add_coupon'),
    path('coupons/edit/<int:pk>/',edit_coupon, name='edit_coupon'),
    path('coupons/delete/<int:pk>/', delete_coupon, name='delete_coupon'),

    
 
]