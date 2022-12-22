from django.shortcuts import get_object_or_404 , render
from .models import Product

# Create your views here.
def products(request):
    cs=None
    pro=Product.objects.all()
    if'cs' in request.GET:
        cs=request.GET['cs']
        if not cs:
            cs='off'
    if 'sename' in request.GET:
        name=request.GET['sename']
        if name:
            if cs=='on':
                pro=pro.filter(name__contains=name)
            else:
                pro=pro.filter(name__icontains=name)

    if 'sedes' in request.GET:
        desc=request.GET['sedes']
        if desc:
            if cs=='on':
                pro=pro.filter(describtion__contains=desc)
            else:  
                pro=pro.filter(describtion__icontains=desc)
  
    if 'seprfo' in request.GET and 'seprto' in request.GET:
        seprfo=request.GET['seprfo']
        seprto=request.GET['seprto']
        if seprfo and seprto :
            if seprfo.isdigit() and seprto.isdigit() :
                pro=pro.filter(price__gte=seprfo,price__lte=seprto)

    context={
        'x':pro
    }
    return render(request,'products/products.html',context)
def product(request,pro_id):
    context={
        'pro':get_object_or_404(Product,pk=pro_id)
    }
    return render(request,'products/product.html',context) 
def search(request):
    return render(request,'products/search.html')       
 