from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .form import *
from django.utils.timezone import localtime, now

# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == "POST" :
        form = CreateUserForm(request.POST) 
        if (form.is_valid()):
            form.save()
            return redirect('login')
        else:
            messages.info(request,"The information provided is invalid!")
    context = {'form':form}    
    return render(request,'app/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        last_login = localtime(request.user.last_login).date()
        today = localtime(now()).date()
        
        if last_login != today:
            logout(request)
            return redirect('login')
    
    if(request.user.is_authenticated):
        if(request.user.role == "user"):
            return redirect('home_customer')
    
    if(request.method== "POST"):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if(user is not None):
            login(request,user)
            return redirect('home_customer')
        else:
            messages.info(request,"User name or Password is not correct")
    return render(request,'app/login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

def home_customer(request):
    customer=Customer.objects.get(user=request.user)
    pets= Pet.objects.filter(customer=customer)
    context={'customer': customer,'pets':pets}
    return render(request,'customer/home_customer.html',context)

def profile_customer(request):
    customer=Customer.objects.get(user=request.user)
    context={'customer': customer}
    return render(request,'customer/profile_customer.html',context)

def appointment_registration(request):
    return render(request,'customer/appointment_registration.html')

def rating(request):
    return render(request,'customer/rating.html')