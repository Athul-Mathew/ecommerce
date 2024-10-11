
from django.urls import path, include
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('adminpanel/',views.adminpanel,name="adminpanel"),
    path('dashboard/',views.dashboard,name='dashboard'),
    # path('apply-coupon/', views.show_cart, name="apply_coupon"),
    # path('remove-coupon/', views.remove_coupon, name="remove_coupon"),

]
