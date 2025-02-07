from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .form import *

# Create your views here.
def register(request):
    if(request.user.is_authenticated):
        logout(request)
        redirect('login')
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
    return render(request,'app/cutomer/login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

def home_customer(request):
    return render(request,'app/home_customer.html')