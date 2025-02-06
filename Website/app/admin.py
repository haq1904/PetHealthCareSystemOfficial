from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Import model CustomUser của bạn

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

    def save_model(self, request, obj, form, change):
        """Đảm bảo `is_staff` được cập nhật đúng khi admin thay đổi role"""
        if obj.role in ['staff', 'veterinarian', 'admin']:
            obj.is_staff = True
        else:
            obj.is_staff = False
        super().save_model(request, obj, form, change)

#  **Đăng ký CustomUserAdmin vào Django Admin**
admin.site.register(CustomUser, CustomUserAdmin)

