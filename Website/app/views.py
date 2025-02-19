from django.shortcuts import get_object_or_404, render,redirect
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
from django.conf import settings

# Create your views here.


#for customer
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
        email = data.get('email')
        customer = Customer.objects.get(user=request.user)
        customer.address = address
        request.user.address = address
        customer.phone_number_customer = phone
        request.user.phone_number = phone
        customer.email_customer=email
        print( customer.email_customer)
        request.user.email=email
        customer.save()
        request.user.save()
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
            
            if request.user.role == "user":
                
                currentUser = Customer.objects.get(user=request.user)
                
            elif request.user.role == "staff":
                currentUser = Staff.objects.get(user=request.user)
                

            elif request.user.role == "veterinarian":
                currentUser = Veterinarian.objects.get(user=request.user)
            
            

            if currentUser.images:
                old_image_path = currentUser.images.path
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            new_filename = f"{request.user.name}_{currentUser.id}_{slugify(image.name)}"

            currentUser.images.save(new_filename, image, save=True)

            return JsonResponse({'success': True,
                "message": "Tải ảnh lên thành công!",
                "image_url": currentUser.images.url,
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
        formBooking = formBookingForm.save(commit=False)  
        flag=True
        #kiểm tra có hồ sơ nào cùng dịch vụ trong trạng thái đợi không.
        if formBooking.examine : 
            if Booking.objects.filter(formbooking__examine=True,bookingstatus__awaiting=True,pet=pet) :
                flag=False
        if formBooking.hospitalization : 
            if Booking.objects.filter(formbooking__hospitalization=True,bookingstatus__awaiting=True,pet=pet) :
                flag=False
        if formBooking.vaccination :
            if Booking.objects.filter(formbooking__vaccination=True,bookingstatus__awaiting=True,pet=pet) :
                flag=False
        if not flag :
            messages.warning(request,f"Hồ sơ của pet {pet.name_pet} đã tồn tại những dịch vụ bạn đã chọn. Vui lòng chọn dịch khác!")
            return redirect('home_customer')
        booking=Booking.objects.create(pet=pet,veterinarian=vet)
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
        
        cost=Cost.objects.create(booking=booking)
        cost.save()

        if formBooking.examine :
            Examine.objects.create(pet=pet)
        if formBooking.hospitalization :
            Hospitalization.objects.create(pet=pet)
            booking.store_pet=True
        if formBooking.vaccination :
            VaccinationHistory.objects.create(pet=pet)
        booking.save()
        BookingStatus.objects.create(booking=booking)
        
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
    booking=Booking.objects.filter(pet=pet)
    
    if request.method=="POST":
        messages.success(request, f"Để xóa hồ sơ thú cưng, vui lòng liên hệ nhân viên để được hỗ trợ.!") 
        return redirect('home_customer')
        
    return render(request,"customer/petInf_customer.html",{"pet":pet})

def  vaccine_his(request,pet_id):
    vaccines=VaccinationHistory.objects.filter(pet=Pet.objects.get(id=pet_id))
    return render(request,"customer/vaccine_his.html",{'vaccines':vaccines})

def  medical_his(request,pet_id):
    medicals=MedicalHistory.objects.filter(pet=Pet.objects.get(id=pet_id))
    return render(request,"customer/medical_his.html",{'medicals':medicals})

def store_pet(request):
    pets=Pet.objects.filter(customer=Customer.objects.get(user=request.user))
    bookings = Booking.objects.filter(store_pet=True)
    return render(request,'customer/store_pet.html',{'bookings':bookings,'pets':pets})

def store_petInf_customer(request,pet_id):
    pet = Pet.objects.get(id=pet_id)
    return render(request,"customer/store_petInf_customer.html",{"pet":pet})

def list_hos(request,pet_id):
    pet=Pet.objects.get(id=pet_id)
    hos=Hospitalization.objects.filter(pet=pet)
    return render(request,"customer/list_hos.html",{'hoss':hos})

def update_status_pet(request,hos_id):
    hos=Hospitalization.objects.get(id=hos_id)
    updateStatus = UpdateStatus.objects.filter(hospitalization=hos)
    return render(request,"customer/update_status_pet.html",{"updateStatus": updateStatus})





#for staff

def home_staff(request):
    reviews= Review.objects.all()
    return render(request,"staff/home_staff.html",{'reviews':reviews})

def profile_staff(request):
    staff=Staff.objects.get(user=request.user)
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            staff.real_name_Staff = form.cleaned_data.get('real_name_Staff')
            staff.email_staff = form.cleaned_data.get('email_staff')
            staff.phone_number_staff = form.cleaned_data.get('phone_number_staff')
            staff.save()
    else:
        form=StaffForm(instance=staff)
            
    return render(request,"staff/profile_staff.html",{'staff': staff,'form':form})


def in_use_cage(request):
    cages = Cage.objects.annotate(hos_count=Count('hospitalization')).filter(hos_count__gt=0)
    if(request.method=="POST"):
        form=Cageform(request.POST)
        if(form.is_valid()):
            newCage=Cage.objects.create()
            newCage.capacity=form.cleaned_data.get('capacity')
            newCage.save()
            messages.success(request,'Đã thêm chuồng thành công.')
    else :
        form=Cageform()
    return render(request,"staff/in_use_cage.html",{'cages':cages,'form':form})

def vacant_cage(request):
    cages = Cage.objects.annotate(hos_count=Count('hospitalization')).filter(hos_count=0)
    return render(request,"staff/vacant_cage.html",{'cages':cages})

def delete_cage(request):
    cages = Cage.objects.annotate(hos_count=Count('hospitalization')).filter(hos_count=0)

    if request.method == "POST":
        cage_id = request.POST.get('cage_id')
        cage = Cage.objects.get(id=cage_id)
        cage.delete()
        return redirect('delete_cage') 

    return render(request, "staff/delete_cage.html", {'cages': cages})

def petInf_store(request,cage_id):
    cage = get_object_or_404(Cage.objects.annotate(hos_count=Count('hospitalization')), id=cage_id)
    hoss = Hospitalization.objects.filter(cage=cage)
    return render(request,"staff/petInf_store.html",{'cage':cage,'hoss':hoss})

def deletePet_store(request,cage_id):
    cage = get_object_or_404(Cage.objects.annotate(hos_count=Count('hospitalization')), id=cage_id)
    hoss = Hospitalization.objects.filter(cage=cage)
    if request.method=="POST":
        hos_id =request.POST.get('hos_id')
        hos=Hospitalization.objects.get(id=hos_id)
        hos.cage=None
        hos.save()        
        
    return render(request,"staff/deletePet_store.html",{'cage':cage,'hoss':hoss})

def addPet_store(request,cage_id):
    hoss= Hospitalization.objects.filter(pet__booking__store_pet=True,cage=None).distinct()
    cage = get_object_or_404(Cage.objects.annotate(hos_count=Count('hospitalization')), id=cage_id)
    if request.method =="POST":
        if cage.hos_count<5 :
            hos_id = request.POST.get('hos_id')
            hos=Hospitalization.objects.get(id=hos_id)
            hos.cage=cage
            hos.save()
        else :
            messages.warning("Số lượng thú cưng đã đạt tối ta.")
            return redirect('addPet_store') 
    return render(request,"staff/addPet_store.html",{'hoss':hoss})


def awaiting_booking(request):
    bookings=Booking.objects.filter(bookingstatus__awaiting=True)
    return render(request,'staff/awaiting_booking.html',{'bookings':bookings})

def confirm_booking(request):
    bookings=Booking.objects.filter(bookingstatus__confirm=True)
    return render(request,'staff/confirm_booking.html',{'bookings':bookings})

def success_booking(request):
    bookings=Booking.objects.filter(bookingstatus__success=True)
    return render(request,'staff/success_booking.html',{'bookings':bookings})

def cancel_booking(request):
    bookings=Booking.objects.filter(bookingstatus__cancelled=True)
    return render(request,'staff/cancel_booking.html',{'bookings':bookings})

def bookingInf_staff(request,booking_id):
    booking=Booking.objects.get(id=booking_id)
    appointmentdate=AppointmentDate.objects.get(booking=booking)
    if appointmentdate.morning==True:
        part = "Buổi sáng"
    elif appointmentdate.afternoon==True:
        part = "Buổi chiều"
    else :
        part = "Buổi tối"

    options=[]
    if booking.formbooking.examine:
        options.append("Khám bệnh")
    if booking.formbooking.hospitalization:
        options.append("Gửi để theo dõi")
    if booking.formbooking.vaccination:
        options.append("Tiêm vaccine")

    if booking.bookingstatus.awaiting:
        status="Đang đợi xác nhận"
    elif booking.bookingstatus.confirm:
        status="Đã được xác nhận"
    elif booking.bookingstatus.success:
        status="Thành công"
    elif booking.bookingstatus.cancelled:
        status="Đã hủy"

    if request.method=="POST":
        action = request.POST.get('action')
        form=CostForm(request.POST)
        if action=='changeBtn':
            booking.staff=Staff.objects.get(user=request.user)
            if form.is_valid() :
                #lưu phí phát sinh và nội dung phát sinh
                booking.cost.extra_fee=form.cleaned_data.get('extra_fee')
                booking.cost.extra_service=form.cleaned_data.get('extra_service')
                booking.cost.save()

                #đặt lại trạng thái cho lịch đặt
                booking.bookingstatus.awaiting=False
                booking.bookingstatus.confirm=True
                booking.bookingstatus.save()

                #lưu id của staff vào booking
                booking.save()
        elif action=='deleteBtn' :
            #set lại thời gian rảnh của các bác sĩ
            schedule=Schedule.objects.get(date=booking.appointmentdate.date,veterinarian=booking.veterinarian)
            if booking.appointmentdate.morning:
                schedule.morning=True
            elif booking.appointmentdate.afternoon:
                schedule.afternoon=True
            elif booking.appointmentdate.night:
                schedule.night=True
            schedule.save()
            booking.delete()
            return redirect('awaiting_booking')
    else :
        form=CostForm()
    return render(request,'staff/bookingInf_staff.html',{'booking':booking,'part': part,'options':options,'status':status,'form':form})



def booking_date_staff(request,booking_id):
    booking = Booking.objects.get(id = booking_id)
    date = request.session.get("selected_date")

    if request.method == "POST":
        action=request.POST.get('action')
        dateForm = AppointmentDateForm(request.POST)
        if action=='confirmBtn':
            
            if dateForm.is_valid():
                date = dateForm.cleaned_data['date']
                request.session["selected_date"] = str(date)
        elif action == 'bookBtn' :
            choice = request.POST.get("appointment_choice")
            if choice : 
                schedule_str , part = choice.split(":")
                schedule_id = int(schedule_str)
                schedule = Schedule.objects.get(id=schedule_id) # lấy lịch được chọn
                appointmentdate=AppointmentDate.objects.get(booking=booking) # lấy ngày và buổi của booking hiện tại
                appointmentdate.date=date
                if not booking.veterinarian : # nếu chưa có bác sĩ
                    booking.veterinarian=schedule.veterinarian # gán bác sĩ của ngày được chọn cho booking
                    #thay đổi ngày đặt lịch và cũng như là trạng thái lịch cua bác sĩ
                    if part == 'morning' : 
                        schedule.morning=False
                        appointmentdate.morning=True
                    elif part == 'afternoon':
                        schedule.afternoon=False
                        appointmentdate.afternoon=True
                    elif part == 'night':
                        schedule.night=False
                        appointmentdate.night=True
                    booking.staff=Staff.objects.get(user=request.user)
                    booking.bookingstatus.awaiting=False
                    booking.bookingstatus.confirm=True
                    booking.bookingstatus.save()
                    schedule.save()
                    appointmentdate.save()
                    booking.save()
                    messages.success(request,'Đặt lịch với bác sĩ thành công!')
                    return redirect('bookingInf_staff',booking_id=booking_id)
                else : 
                    messages.warning(request,'Lịch khám đã có bác sĩ phụ trách, vui lòng không đổi!')
                    return redirect('bookingInf_staff',booking_id=booking_id)
                
     
            else :
                messages.warning(request,'Vui lòng chọn ít nhất một ngày!')
                return redirect("booking_date_staff",booking_id=booking_id)


    elif request.method == "GET" and "selected_date" in request.session:
        dateForm = AppointmentDateForm(initial={'date': date})

    else:
        dateForm = AppointmentDateForm()

    schedules = Schedule.objects.filter(date=date) if date else []

    context = {
        'dateForm': dateForm,
        'schedules': schedules,
        'date': date,
    }
    return render(request,'staff/booking_date_staff.html',context)


