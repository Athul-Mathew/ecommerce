from django.urls import path

# from accounts import views
from cart import views

urlpatterns = [
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('',views.show_cart,name='show_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_cartitem/<int:product_id>/', views.remove_cartitem, name='remove_cartitem'),



    path('remove-coupon/', views.remove_coupon, name="remove_coupon"),
    
]
