from django.db import models
from accounts.models import Customer
# Create your models here.
class AddressDetails(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    order_address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def full_address(self):
        return f"{self.order_address},{self.city}, {self.state}, {self.country}, PIN: {self.zip_code}"
    
    def str(self):
        return self.user.username