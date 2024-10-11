from django.urls import path
from . import views


urlpatterns = [
              
    path('view/', views.view, name='view'),
    path('order_list/', views.order_list, name='order_list'),
    path('change_order_status/<int:order_id>/', views.change_order_status, name='change_order_status'),
    path('admin_sales',views.admin_sales,name='admin_sales'),
    path('cancelOrder/', views.cancelOrder, name='cancelOrder'),
    path('order_items/<int:id>/', views.order_items, name='ordered_items'),
]