
from django.urls import path
from . import views



urlpatterns = [
    path('shop/',views.shop ,name='shop'),
    path('shopdetails/<int:id>/',views.shopdetails ,name='shopdetails'),
    path('search/',views.shop,name='search'),
]