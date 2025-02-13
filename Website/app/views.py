from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .form import *
from django.utils.timezone import localtime, now
from django.utils import timezone
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
        if(request.user.role == "staff"):
            return redirect('home_staff')
        if(request.user.role == "verterinarian"):
            return redirect('home_customer')

    if(request.method== "POST"):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            # Sau khi login, kiểm tra vai trò của user để redirect đúng trang
            if user.role == "user":
                return redirect('home_customer')
            elif user.role == "staff":
                return redirect('home_staff')
            elif user.role == "veterinarian":
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


def pet_registration(request):
    customer = Customer.objects.get(user=request.user)

    if request.method == "POST":
        form = PetForm(request.POST)
        if form.is_valid():
            pet=form.save(commit=False)
            pet.customer=customer
            pet.save()
            request.session['pet_id'] = pet.id
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

def booking(request, pet_id, date):
    pet =Pet.objects.get(id=pet_id)
    part = request.GET.get('part')
    vet_id = request.GET.get('vet_id')
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    print(date_obj)
    if vet_id :
        vet=Veterinarian.objects.get(id=vet_id)
    else:
        vet =None
    
    if request.method == "POST":
        formBookingForm = FormBookingForm(request.POST)
        booking=Booking.objects.create(pet=pet,veterinarian=vet)
        formBooking = formBookingForm.save(commit=False)  
        formBooking.booking=booking
        formBooking.save()
        
        appointment=AppointmentDate.objects.create(booking=booking,date=date_obj)
        if vet :
            schedule=Schedule.objects.get(veterinarian=vet,date=date_obj)
            if part == 'morning':
                appointment.morning=True
                schedule.morning=False
            elif part =='afternoon':
                appointment.afternoon=True
                schedule.afternoon=False
            else:
                appointment.night=True
                schedule.night=False
            schedule.save()
            appointment.save()
        booking.save()
        cost=Cost.objects.create(booking=booking)
        cost.save()

        if formBooking.examine :
            Examine.objects.create(booking=booking)
        if formBooking.hospitalization :
            Hospitalization.objects.create(booking=booking)
        if formBooking.vaccination :
            VaccinationHistory.objects.create(pet=pet)
        
        messages.success(request, "Bạn đã đặt lịch cho thú cưng thành công! Sẽ có nhân viên liên hệ để bạn thanh toán trực tuyến hoặc bạn có thể thanh toán trực tiếp tại hệ thống của chúng tôi. Xin cảm ơn quý khách!")
        return redirect("home_customer") 
    else:
        formBookingForm = FormBookingForm()
    
    
    days_mapping = {
        "Monday": "Thứ Hai",
        "Tuesday": "Thứ Ba",
        "Wednesday": "Thứ Tư",
        "Thursday": "Thứ Năm",
        "Friday": "Thứ Sáu",
        "Saturday": "Thứ Bảy",
        "Sunday": "Chủ Nhật"
    }

    part_mapping={
        "morning":"Buổi sáng",
        "afternoon":"Buổi Chiều",
        "night":"Buổi tối",
    }
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    day_english = date_obj.strftime("%A")  
    day_vietnamese = days_mapping.get(day_english) 
    part_vietnamese = part_mapping.get(part)
    formatted_date = f"{day_vietnamese}, {date_obj.strftime('%d/%m/%Y')}"
    context = {
        "pet": pet,
        "vet": vet,
        "formBookingForm" : formBookingForm,
        "date":date_obj,
        "formatted_date":formatted_date,
        "part_vietnamese":part_vietnamese
    }
    return render(request, "customer/booking.html", context)

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
        'date': date,
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

def pick_pet_review(request):
    customer=Customer.objects.get(user=request.user)
    pets = Pet.objects.filter(customer=customer)
    context={'pets':pets}
    return render(request,'customer/pick_pet_review.html',context)

def pick_booking_review(request,pet_id):
    bookings=Booking.objects.filter(pet=Pet.objects.get(id=pet_id))
    if bookings :
        booking_options=[]
        for booking in bookings:
            options = []
            if hasattr(booking, 'formbooking'): 
                if booking.formbooking.examine:
                    options.append("Khám bệnh")
                if booking.formbooking.hospitalization:
                    options.append("Gửi để theo dõi")
                if booking.formbooking.vaccination:
                    options.append("Tiêm vaccine")

            booking_options.append({
                "booking": booking,
                "options": options
            })
    else: 
        booking_options=[]

    context={"booking_options":booking_options}
    return render(request,'customer/pick_booking_review.html',context)

def review(request,booking_id):
    booking=Booking.objects.get(id=booking_id)
    date=booking.appointmentdate.date
    if booking.appointmentdate.morning==True:
        part = "Buổi sáng"
    elif booking.appointmentdate.afternoon==True:
        part = "Buổi chiều"
    else :
        part = "Buổi tối"

    days_mapping = {
        "Monday": "Thứ Hai",
        "Tuesday": "Thứ Ba",
        "Wednesday": "Thứ Tư",
        "Thursday": "Thứ Năm",
        "Friday": "Thứ Sáu",
        "Saturday": "Thứ Bảy",
        "Sunday": "Chủ Nhật"
    }

    if request.method=="POST":
        form=ReviewForm(request.POST)
        if(form.is_valid()):
            if Review.objects.filter(booking=booking).exists() :
                booking.review=form.save(commit=False)
                booking.review.time=timezone.now()
                booking.review.save()
                messages.success(request, "Đã cập nhật đánh giá. Xin cảm ơn bạn!")
            else :
                review=form.save(commit=False)
                review.time=timezone.now()
                review.booking=booking
                review.save()
                messages.success(request, "Đã gửi đánh giá đến hệ thống. Xin cảm ơn bạn!") 
            return redirect('home_customer')            
    else:
        form=ReviewForm()



    day_english = date.strftime("%A")  
    day_vietnamese = days_mapping.get(day_english) 
    formatted_date = f"{day_vietnamese}, {date.strftime('%d/%m/%Y')}"

    context={"booking":booking,"formatted_date":formatted_date,"part":part,"form":form}
    return render(request,"customer/review.html",context)

def petInf_customer(request,pet_id):
    pet=Pet.objects.get(id=pet_id)
    return render(request,"customer/petInf_customer.html",{"pet":pet})

def  vaccine_his(request,pet_id):
    vaccines=VaccinationHistory.objects.filter(pet=Pet.objects.get(id=pet_id))
    return render(request,"customer/vaccine_his.html",{'vaccines':vaccines})

def  medical_his(request,pet_id):
    medicals=MedicalHistory.objects.filter(pet=Pet.objects.get(id=pet_id))
    return render(request,"customer/medical_his.html",{'medicals':medicals})


def home_staff(request):
    return render(request,"staff/home_staff.html")