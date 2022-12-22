import re
from urllib import request
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile 
from django.contrib import auth
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from products.models import Product

# Create your views here.
def signin(request):
    if request.method=='POST' and 'btnlog' in request.POST:
        username=request.POST['siname']
        password=request.POST['sipass']
        user=auth.authenticate(password=password,username=username)
        if user is not None:
            if 'rememberme' not in request.POST:
                print('rememberme')
                request.session.set_expiry(0) 
            auth.login(request,user)
            messages.success(request,'login sucessfully')
            return redirect('index')
        else:
            messages.error(request,'username or password is incorrect')

    return render(request,'accounts/signin.html')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')
            
def signup(request):
    if request.method=='POST' and 'submit' in request.POST:
        fname=None
        lname=None
        address=None
        address2=None
        city=None
        state=None
        zip=None
        email=None
        username=None
        password=None
        termes=None
        is_added=None
        if 'sfname' in request.POST: fname=request.POST['sfname']
        else: messages.error(request,'Error in frist name')
        if 'slname' in request.POST: lname=request.POST['slname']
        else: messages.error(request,'Error in last name')
        if 'sad' in request.POST: address=request.POST['sad']
        else: messages.error(request,'Error in  address')
        if 'ssad' in request.POST: address2=request.POST['ssad']
        else: messages.error(request,'Error in  address2')
        if 'scity' in request.POST: city=request.POST['scity']
        else: messages.error(request,'Error in  city')
        if 'state' in request.POST: state=request.POST['state']
        else: messages.error(request,'Error in  state')
        if 'szip' in request.POST: zip=request.POST['szip']
        else: messages.error(request,'Error in  zip numper')
        if 'smail' in request.POST: email=request.POST['smail']
        else: messages.error(request,'Error in  e-mail address')
        if 'suname' in request.POST: username=request.POST['suname']
        else: messages.error(request,'Error in  username')
        if 'supass' in request.POST: password=request.POST['supass']
        else: messages.error(request,'Error in  password')
        if 'termes' in request.POST: termes=request.POST['termes']
        ###check varibales:
        c=0
        if fname and lname and address and address2 and city and zip and state and email  and username and password:
            if termes =='on':
                #check User name is exist or no
                if User.objects.filter(username=username).exists():
                    messages.error(request,'this username is elready exist')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request,'this email is already exist')
                    else:
                       try:
                            c=1
                            validate_email(email)
                       except ValidationError:
                            c=2
                       if (c==1):
                           #add user
                           user=User.objects.create_user(first_name=fname,last_name=lname
                            ,email=email,username=username,password=password)
                           user.save() 
                           userprofile=UserProfile(user=user,address=address
                             ,address2=address2,state=state,city=city,zip_number=zip )
                           userprofile.save()
                           #clear values
                           fname='' 
                           lname=''
                           email=''
                           city=''
                           zip=''
                           state=''
                           address=''
                           address2=''
                           username=''
                           password=''
                           termes=''
                           
                           messages.success(request,'create account sucessfully')
                           is_added=True
                       else: 
                           messages.error(request, 'Invalid Email')   
                        
            else: 
                 print(termes)
                 messages.error(request,'you should agree termes frist')
        else:
            messages.error(request,'please check empty field ')
        return render (request,'accounts/signup.html',{
            'sfname': fname,
            'slname': lname,
            'sad':address,
            'ssad' :address2,
            'scity' :city,
            'state' :state,
            'szip' :zip,
            'smail': email,
            'suname' :username,
            'supass' :password,
            'termes' :termes,
            'is_added':is_added

          })    
    return render (request,'accounts/signup.html')
def profile(request):
        if request.method=='POST' and 'ptnchange' in request.POST:
            userprofile=UserProfile.objects.get(user=request.user)
            if request.POST['pfname']and request.POST['plname'] and request.POST['pad'] and request.POST['ppad'] and request.POST['pcity']and request.POST['pstate'] and request.POST['pmail'] and  request.POST['puname'] and request.POST['ppass'] and request.POST['pzip']:
                request.user.frist_name=request.POST['pfname']
                request.user.last_name=request.POST['plname']
                #request.user.email=request.POST['pmail']
                #request.user.username=request.POST['puname']
                userprofile.address=request.POST['pad']
                userprofile.address2=request.POST['ppad']
                userprofile.zip_number=request.POST['pzip']
                userprofile.city=request.POST['pcity']
                userprofile.state=request.POST['pstate']
                s=request.user.password=request.POST['ppass']
                request.user.set_password(s)   
                request.user.save()
                userprofile.save()
                auth.login(request,request.user)
                messages.success(request,'data changed sucessfully!')
                
            else:
                messages.error(request,"please check empty failed")
            return render (request, 'accounts/profile.html')    
        else:
            print("test")
            if  request.user.is_authenticated:
                userprofile=UserProfile.objects.get(user=request.user)
                context={
                    'pfname': request.user.first_name,
                    'plname' :request.user.last_name,
                    'pmail':request.user.email,
                    'puname' :request.user.username,
                    #'ppass':request.user.password,
                    'pad' : userprofile.address,
                    'ppad': userprofile.address2,
                    'pcity' :userprofile.city,
                    'pstate':userprofile.state,
                    'pzip' :userprofile.zip_number,
                }
                print("ss")
                return render (request, 'accounts/profile.html',context) 
            else:
                 return render (request, 'accounts/profile.html')
   
def product_favorite(request,pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        fav=Product.objects.get(pk=pro_id)
        # start to check the product already in favorite list or not
        if UserProfile.objects.filter(user=request.user,product_favorites=fav).exists():
            messages.info(request,'this product already exist is favorite list')
        else:
            userprofile=UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.add(fav)
            messages.success(request,'added successfully!')
    else:
        messages.error(request,'you must be log in frist!')
    return redirect('/products/'+str(pro_id))      
def show_product_favorite(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
       userinfo=UserProfile.objects.get(user=request.user)
       pro=userinfo.product_favorites.all()

    
    context={
            'x':pro
        }
    messages.info(request,'your favorite products')
    return render(request,'products/products.html',context)
def mss(request):
    if request.GET:
        messages.info(request,'this is signin page')
        messages.warning(request,'this is wrong password')
        messages.success(request,'succefuly sign in')
        messages.error(request,'error')
