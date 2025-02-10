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
    path('update_customer_info/',views.update_customer_info,name='update_customer_info'),
    path('update_customer_image/',views.update_customer_image,name='update_customer_image'),
    path('update_pet_image/',views.update_pet_image,name='update_pet_image'),
    path('pet_registration/',views.pet_registration,name='pet_registration'),
    path('pet_registration_image/',views.pet_registration_image,name='pet_registration_image'),
    path('booking/<int:pet_id>/', views.booking, name='booking'),

    

]