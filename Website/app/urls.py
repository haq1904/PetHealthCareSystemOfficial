from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #For customer
    path('',views.loginPage,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logoutPage,name='logout'),
    path('home_customer/',views.home_customer,name='home_customer'),
    path('store_pet/',views.store_pet,name='store_pet'),
    path('profile_customer/',views.profile_customer,name='profile_customer'),
    path('appointment_registration/',views.appointment_registration,name='appointment_registration'),
    path('update_customer_info/',views.update_customer_info,name='update_customer_info'),
    path('update_customer_image/',views.update_customer_image,name='update_customer_image'),
    path('update_pet_image/',views.update_pet_image,name='update_pet_image'),
    path('pet_registration/',views.pet_registration,name='pet_registration'),
    path('pet_registration_image/',views.pet_registration_image,name='pet_registration_image'),
    path('booking/<int:pet_id>/<str:date>/', views.booking, name='booking'),
    path('booking_date/<int:pet_id>/', views.booking_date, name='booking_date'),
    path("save_selected_date/", views.save_selected_date, name="save_selected_date"),
    path("get_selected_date/", views.get_selected_date, name="get_selected_date"),
    path("pick_pet_review/", views.pick_pet_review, name="pick_pet_review"),
    path('pick_booking_review/<int:pet_id>/', views.pick_booking_review, name='pick_booking_review'),
    path('review/<int:booking_id>/', views.review, name='review'),
    path('petInf_customer/<int:pet_id>/', views.petInf_customer, name='petInf_customer'),
    path('medical_his/<int:pet_id>/', views.medical_his, name='medical_his'),
    path('vaccine_his/<int:pet_id>/', views.vaccine_his, name='vaccine_his'),
    path('store_petInf_customer/<int:pet_id>/',views.store_petInf_customer,name='store_petInf_customer'),
    path('list_hos/<int:pet_id>/',views.list_hos,name='list_hos'),
    path('update_status_pet/<int:hos_id>/',views.update_status_pet,name='update_status_pet'),


    #for staff

    path('home_staff',views.home_staff,name='home_staff'),
    path('home_staff/profile_staff/',views.profile_staff,name='profile_staff'),
    path('home_staff/in_use_cage/',views.in_use_cage,name='in_use_cage'),
    path('home_staff/vacant_cage/',views.vacant_cage,name='vacant_cage'),
    path('home_staff/vacant_cage/delete_cage/',views.delete_cage,name='delete_cage'),
    path('home_staff/in_use_cage/petInf_store/<int:cage_id>/',views.petInf_store,name='petInf_store'),
    path('home_staff/in_use_cage/petInf_store/<int:cage_id>/deletePet_store/',views.deletePet_store,name='deletePet_store'),
    path('home_staff/in_use_cage/petInf_store/<int:cage_id>/addPet_store/',views.addPet_store,name='addPet_store'),
    path('home_staff/awaiting_booking/',views.awaiting_booking,name='awaiting_booking'),
    path('home_staff/confirm_booking/',views.confirm_booking,name='confirm_booking'),
    path('home_staff/success_booking/',views.success_booking,name='success_booking'),
    path('home_staff/cancel_booking/',views.cancel_booking,name='cancel_booking'),
    path('home_staff/bookingInf_staff/<int:booking_id>/',views.bookingInf_staff,name='bookingInf_staff'),



    
    


   

]