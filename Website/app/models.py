from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserRole(models.TextChoices):
    USER = 'user', 'User'
    STAFF = 'staff', 'Staff'
    ADMIN = 'admin', 'Admin'

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, phone_number=None, address=None, role=UserRole.USER, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        # Chỉ yêu cầu phone_number nếu role không phải ADMIN
        if role != UserRole.ADMIN and not phone_number:
            raise ValueError("Phone number is required")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            phone_number=phone_number,
            address=address,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, username, email, password=None, phone_number=None, address=None, **extra_fields):
        return self.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
            address=address,
            role=UserRole.STAFF,
            **extra_fields
        )
    
    def create_superuser(self, username, email, password, **extra_fields):
        # Đối với superuser, không bắt buộc phải có phone_number và address
        extra_fields.setdefault('is_staff', True)      # Cho phép truy cập admin site
        extra_fields.setdefault('is_superuser', True)    # Toàn quyền
        extra_fields.setdefault('role', UserRole.ADMIN)
        
        return self.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=None,   # Không bắt buộc đối với admin
            address=None,        # Không bắt buộc đối với admin
            **extra_fields
        )

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.USER
    )

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"
    



