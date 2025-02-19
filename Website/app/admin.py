from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
import logging
from django.core.exceptions import ValidationError
logger = logging.getLogger('django')


class CustomUserAdmin(UserAdmin):

    list_display = ('username', 'email', 'phone_number', 'address', 'role', 'is_staff', 'is_active')

    
    search_fields = ('username', 'email', 'phone_number')

    
    list_editable = ('phone_number', 'address', 'role')

    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin bổ sung', {'fields': ('phone_number', 'address', 'role')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Thông tin bổ sung', {'fields': ('phone_number', 'address', 'role')}),
    )

    model = CustomUser

    def save_model(self, request, obj, form, change):
        """Cập nhật is_staff và tạo object role tương ứng khi tạo user trong Django Admin"""
        
        
        obj.is_staff = obj.role in ['staff', 'veterinarian', 'admin']

        super().save_model(request, obj, form, change)

        if not change:
            if obj.role == 'staff':
                Staff.objects.create(user=obj, name_staff=obj.username)
            elif obj.role == 'veterinarian':
                Veterinarian.objects.create(user=obj, name_veterinarian=obj.username)
            elif obj.role == 'user':
                Customer.objects.create(user=obj, name_customer=obj.username)

        if obj.role == 'user':
            try:
                customer = Customer.objects.get(user=obj)
                customer.name_customer = obj.username  
                customer.phone_number_customer = obj.phone_number  
                customer.address = obj.address  
                customer.email_customer=obj.email
                customer.save()
            except Customer.DoesNotExist:
                Customer.objects.create(user=obj, name_customer=obj.username) 

        elif obj.role == 'staff':
            try:
                staff = Staff.objects.get(user=obj)
                staff.name_staff = obj.username 
                staff.phone_number_staff = obj.phone_number  
                staff.email_staff = obj.email  
                staff.save()
            except Staff.DoesNotExist:
                pass  

        elif obj.role == 'veterinarian':
            try:
                veterinarian = Veterinarian.objects.get(user=obj)
                veterinarian.name_veterinarian = obj.username  
                veterinarian.phone_number_veterinarian = obj.phone_number  
                veterinarian.email_vet = obj.email  
                veterinarian.save()
            except Veterinarian.DoesNotExist:
                pass  

class PetAdmin(admin.ModelAdmin):
    list_display = ('name_pet', 'customer', 'species', 'age', 'weight', 'pet_status', 'pet_type', 'is_male') 
    list_filter = ('species', 'pet_status', 'pet_type', 'is_male') 
    search_fields = ('name_pet', 'customer__name')  
    list_editable = ('pet_status', 'weight')  
    ordering = ('-age',)  
    readonly_fields = ('images',) 
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name_pet', 'customer', 'species', 'age', 'is_male')
        }),
        ('Thông tin sức khỏe', {
            'fields': ('weight', 'pet_status', 'pet_type')
        }),
        ('Hình ảnh', {
            'fields': ('images',)
        }),
    )



class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('veterinarian', 'date', 'morning', 'afternoon', 'night')




class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'veterinarian', 'pet',  'booking_date')

#  **Đăng ký CustomUserAdmin vào Django Admin**
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(Veterinarian)
admin.site.register(Pet,PetAdmin)
admin.site.register(Examine)
admin.site.register(MedicalHistory)
admin.site.register(VaccinationHistory)
admin.site.register(Cage)
admin.site.register(Hospitalization)
admin.site.register(Schedule,ScheduleAdmin)
admin.site.register(Booking,BookingAdmin)
admin.site.register(Cost)
admin.site.register(FormBooking)
admin.site.register(BookingStatus)
admin.site.register(Review)
admin.site.register(AppointmentDate)
admin.site.register(UpdateStatus)
