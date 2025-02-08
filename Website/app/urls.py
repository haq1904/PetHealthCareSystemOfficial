from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginPage,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logoutPage,name='logout'),
    path('home_customer/',views.home_customer,name='home_customer'),
    path('profile_customer/',views.profile_customer,name='profile_customer'),
    path('appointment_registration/',views.appointment_registration,name='appointment_registration'),
    path('rating/',views.rating,name='rating'),
    


]