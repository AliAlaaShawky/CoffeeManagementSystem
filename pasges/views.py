from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product
# Create your views here.
def index(request):
    context={
        'x':Product.objects.all()
     }
    return render(request,'pages/index.html',context)
def second(request):
    return render(request,'pages/about.html')
def coffee(request):
    return render(request,'pages/coffee.html')    
