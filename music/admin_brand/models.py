import uuid
from django.db import models

# Create your models here.
class Brand(models.Model):
    brand_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    brand_img = models.ImageField(upload_to='brand', null=True, blank=True)
    brand_name = models.CharField(unique=True, max_length=50)
    brand_description = models.TextField()


    def __str__(self):
        return self.brand_name