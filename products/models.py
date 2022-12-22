from pydoc import describe
from django.db import models
from datetime import datetime
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=150)
    describtion=models.TextField()
    price=models.DecimalField(max_digits=6,decimal_places=2)
    photo=models.ImageField(upload_to='photo/%y/%m/%d')
    is_active=models.BooleanField(default=True)
    publish_date=models.DateTimeField(default=datetime.now)
    ### fuction to return name of product replace object
    def __str__(self) :
        return self.name
    class Meta :
        ordering=['-publish_date']      
