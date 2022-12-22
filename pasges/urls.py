from django.urls import path 
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('about',views.second,name='about'),
    path('coffee',views.coffee,name='coffee')



]