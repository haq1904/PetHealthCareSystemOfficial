from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .form import *
from django.utils.timezone import localtime, now
import os
from django.utils.text import slugify
from .form import PetForm,BookingForm
from datetime import datetime

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
    pet_count=Pet.objects.filter(customer=customer).count()
    context={'customer': customer,'pet_count':pet_count}
    return render(request,'customer/profile_customer.html',context)

def update_customer_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        address = data.get('address')
        phone = data.get('phone')
        customer = Customer.objects.get(user=request.user)
        customer.address = address
        request.user.address = address
        customer.phone_number_customer = phone
        request.user.phone_number = phone
        customer.save()
        return JsonResponse({'message': 'Cập nhật thành công!'}, status=200)
    return JsonResponse({'message': 'Phương thức không hợp lệ!'}, status=405)

def appointment_registration(request):
    customer=Customer.objects.get(user=request.user)
    pets = Pet.objects.filter(customer=customer)
    context={'pets':pets}
    return render(request,'customer/appointment_registration.html',context)

def rating(request):
    return render(request,'customer/rating.html')

def pet_registration(request):
    customer = Customer.objects.get(user=request.user)
    
    if request.method == "POST":
        form = PetForm(request.POST)
        if form.is_valid():
            pet=form.save(commit=False)
            pet.customer=customer
            pet.save()
            request.session['pet_id'] = pet.id
            print(pet.id)

            return redirect('pet_registration_image')  
    
    else:
        form = PetForm()

    context = {'form': form}
    return render(request, 'customer/pet_registration.html', context)

def pet_registration_image(request):
    return render(request,'customer/pet_registration_image.html')

def update_customer_image(request):
    if request.method == "POST":
        try:
            image = request.FILES.get("image")
            if not image:
                return JsonResponse({"error": "Bạn chưa chọn ảnh!"}, status=400)

            customer = Customer.objects.get(user=request.user)

            if customer.images:
                old_image_path = customer.images.path 
                if os.path.exists(old_image_path):
                    os.remove(old_image_path) 

            new_filename = f"{customer.id}_{slugify(image.name)}"

            customer.images.save(new_filename, image, save=True)

            return JsonResponse({'success': True,
                "message": "Tải ảnh lên thành công!",
                "image_url": customer.images.url,
            })
        except Exception as e:
            return JsonResponse({"error": f"Lỗi: {str(e)}"}, status=500)

    return JsonResponse({"error": "Phương thức không hợp lệ!"}, status=405)

def update_pet_image(request):
    if request.method == "POST":
        try:
            image = request.FILES.get("image")
            if not image:
                return JsonResponse({"error": "Bạn chưa chọn ảnh!"}, status=400)


            pet_id = request.session.get("pet_id")
            pet = Pet.objects.get(id=pet_id)
            del request.session["pet_id"]
            


            if pet.images:
                old_image_path = pet.images.path 
                if os.path.exists(old_image_path):
                    os.remove(old_image_path) 

            name, ext = os.path.splitext(image.name)
            new_filename = f"{pet.id}_{slugify(name)}{ext}"

            pet.images.save(new_filename, image, save=True)

            return JsonResponse({'success': True,
                "message": "Tải ảnh lên thành công!",
                "image_url": pet.images.url,
            })
        except Exception as e:
            return JsonResponse({"error": f"Lỗi: {str(e)}"}, status=500)

    return JsonResponse({"error": "Phương thức không hợp lệ!"}, status=405)

def booking(request,pet_id,date):
    pet=Pet.objects.get(id=pet_id)
    vet_id = request.GET.get('vet_id')
    part=request.GET.get('part')
    if request.method=="POST":
        formBookingForm=FormBookingForm(request.POST)
        bookingForm=BookingForm(request.POST)
        if formBookingForm.is_valid() and bookingForm.is_valid():
            booking=bookingForm.save(commit=False)
            
    context={'pet':pet}
    return render (request,"customer/booking.html",context)

def booking_date(request, pet_id):
    date = request.session.get("selected_date")  

    if request.method == "POST":
        dateForm = AppointmentDateForm(request.POST)
        if dateForm.is_valid():
            date = dateForm.cleaned_data['date']
            request.session["selected_date"] = str(date) 

    elif request.method == "GET" and "selected_date" in request.session:
        dateForm = AppointmentDateForm(initial={'date': date})  

    else:
        dateForm = AppointmentDateForm()

    schedules = Schedule.objects.filter(date=date) if date else []

    context = {
        'dateForm': dateForm,
        'schedules': schedules,
        'pet_id': pet_id,
        'date': date
    }

    return render(request, "customer/booking_date.html", context)



def save_selected_date(request):
    if request.method == "POST":
        data = json.loads(request.body)
        selected_date = data.get("selected_date")
        request.session["selected_date"] = selected_date  # Lưu vào session
        return JsonResponse({"status": "success"})

def get_selected_date(request):
    selected_date = request.session.get("selected_date", "")
    return JsonResponse({"selected_date": selected_date})