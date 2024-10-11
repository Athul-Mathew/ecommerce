from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission,Group
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

from admin_brand.models import Brand
from admin_products.models import Product



# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Email address is required')

        if not username:
            raise ValueError('Username is required')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Customer(AbstractBaseUser):
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    username = models.CharField(max_length=50, unique=True,null=True)
    email = models.EmailField(max_length=100, unique=True,null=True)
    phone_number = models.CharField(max_length=50,null=True)
    user_image = models.ImageField(upload_to='profile_picture', blank=True, null=True,default='profile_picture/propic.png')


    # Required
    date_joined = models.DateField(auto_now_add=True,null=True)
    last_login = models.DateTimeField(auto_now_add=True,null=True)
    is_admin = models.BooleanField(default=False,null=True)
    is_staff = models.BooleanField(default=False,null=True)
    is_active = models.BooleanField(default=False,null=True)
    is_superadmin = models.BooleanField(default=False,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
 
    objects = MyAccountManager()

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

class UserOTP(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    time_st=models.DateTimeField(auto_now=True)
    otp=models.IntegerField()



    

import uuid


        
    

    



class variations(models.Model):
    colour = models.CharField(max_length=20)    
    

class MultiProduct(models.Model):

    product=models.ForeignKey(Product,on_delete=models.CASCADE)   

    image=models.ImageField(upload_to='uploads')

   

class logo(models.Model)    :

    logo=models.ImageField(upload_to='uploads')






