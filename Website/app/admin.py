from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
import logging

logger = logging.getLogger('django')


class CustomUserAdmin(UserAdmin):

    # 🏷 **1. list_display** - Hiển thị các trường trong danh sách user
    list_display = ('username', 'email', 'phone_number', 'address', 'role', 'is_staff', 'is_active')

    # 🔍 **2. search_fields** - Thêm chức năng tìm kiếm theo các trường
    search_fields = ('username', 'email', 'phone_number')

    # ✏ **3. list_editable** - Cho phép chỉnh sửa trực tiếp từ danh sách user
    list_editable = ('phone_number', 'address', 'role')

    #  **4. fieldsets** - Cấu hình trang chỉnh sửa User
    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin bổ sung', {'fields': ('phone_number', 'address', 'role')}),
    )

    # **5. add_fieldsets** - Cấu hình trang tạo User mới
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

        logger.debug(f"User role: {obj.role}")
        if obj.role == 'user':
            try:
                customer = Customer.objects.get(user=obj)
                customer.name_customer = obj.username  
                customer.phone_number_customer = obj.phone_number  
                customer.address = obj.address  
                customer.save()
                print(f"Updated customer: {customer}")
                logger.debug(f"Updated customer: {customer}")
            except Customer.DoesNotExist:
                Customer.objects.create(user=obj, name_customer=obj.username) 
                print("Created new customer")
                logger.debug("Created new customer")

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
    list_display = ('name_pet', 'customer', 'species', 'age', 'weight', 'pet_status', 'pet_type', 'is_male')  # Hiển thị các cột trong danh sách
    list_filter = ('species', 'pet_status', 'pet_type', 'is_male')  # Bộ lọc ở sidebar
    search_fields = ('name_pet', 'customer__name')  # Cho phép tìm kiếm theo tên thú cưng và tên khách hàng
    list_editable = ('pet_status', 'weight')  # Cho phép chỉnh sửa trực tiếp trên danh sách
    ordering = ('-age',)  # Sắp xếp mặc định theo tuổi giảm dần
    readonly_fields = ('images',)  # Chỉ đọc cho ảnh
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
admin.site.register(PetStatus)
admin.site.register(Schedule)
admin.site.register(Booking)
admin.site.register(Cost)
admin.site.register(Form)
admin.site.register(BookingStatus)
admin.site.register(Review)
admin.site.register(CageType)
admin.site.register(CageStatus)

