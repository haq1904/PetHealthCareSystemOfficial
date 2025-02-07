from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.register,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('home_customer/',views.home_customer,name='home_customer'),


]