
from django.urls import path
from . import views


urlpatterns = [
    path('product/',views.product,name='product'),
    path('addproducts/',views.addproducts,name='addproducts'),
    path('updateproduct/<int:product_id>/',views.updateproduct ,name='updateproduct'),
    path('deleteproduct/<int:product_id>/',views.deleteproduct ,name='deleteproduct'),
    path('add_product_images/<int:product_id>/',views.add_product_images ,name='add_product_images'),
    # path('filter/', views.filter_products, name='filter_products'),
    
    path('product/<int:product_id>/add_offer/',views.add_product_offer, name='add_product_offer'),
    path('offer/<int:offer_id>/delete/', views.delete_product_offer, name='delete_product_offer'),
]