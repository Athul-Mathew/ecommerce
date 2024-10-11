from django.urls import path, include
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
               path('brand/',views.brand,name='brand'),
               path('addbrand/',views.addbrand,name='addbrand'),
               path('brand/<uuid:brand_id>/update/', views.update_brand, name='update_brand'),
               path('deletebrand/<int:brand_id>/',views.deletebrand,name='deletebrand'),
            
]