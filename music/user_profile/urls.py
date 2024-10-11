
from django.urls import path
from . import views

urlpatterns = [
    path('add_address/', views.add_address, name='add_address'),
    path('manageaddress/',views.manageaddress,name='manageaddress'),
    path('deleteaddress/<int:id>/',views.deleteaddress,name='deleteaddress'),
    path('edit_address/<int:id>/', views.edit_address, name='editaddress'),
    path('Address/', views.Address, name='Address'),
]