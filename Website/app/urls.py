from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.register,name='register'),
    path('login/',views.loginPage,name='login'),
    path('home/',views.home,name='home'),
    path('logout/',views.logoutPage,name='logout')


]