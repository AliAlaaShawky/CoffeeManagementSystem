from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.
class UserProfile(models.Model):
    #to cocnect the model with his name in another table
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    product_favorites=models.ManyToManyField(Product)
    address=models.CharField(max_length=80)
    address2=models.CharField(max_length=80)
    city=models.CharField(max_length=80)
    state=models.CharField(max_length=80)
    zip_number=models.CharField(max_length=80)
    def __str__(self):
        return self.user.username
