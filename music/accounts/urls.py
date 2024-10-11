from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('change-password/',views. change_password, name='change_password'),
    path('forgetpassword/',views.forgetpassword,name='forgetpassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword/',views.resetpassword,name='resetpassword'),


    path('login/', views.login, name="login"),
    path('users/',views.users,name='users'),
    

    # path('orders/',views.orders,name='orders'),
    path('blockuser/<int:id>/',views.blockuser,name='blockuser'),
  
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),

    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),


    path('extraimg/',views.extraimg,name='extraimg'),
    
    path('about/',views.about,name='about'),
    path('accounts/login/',views.login ,name='login'),
    path('register/',views.register ,name='register'),
    path('logout/',views.logout ,name='logout'),
    # path('otp/',views.otp ,name='otp'),
    path('profile/',views.profile ,name='profile'),
   
    # path('product_details/<int:category_slug,product_slug>/',views.product_details ,name='product_details'),

   

    
]