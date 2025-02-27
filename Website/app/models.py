from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models import Count
from decimal import Decimal

class UserRole(models.TextChoices):
    USER = 'user', 'User'
    STAFF = 'staff', 'Staff'
    ADMIN = 'admin', 'Admin'
    VETERINARIAN = 'veterinarian','Veterinarian'

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, phone_number=None, address=None, role=UserRole.USER, **extra_fields):
        if not email:
            raise ValueError("Email is required")
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
        extra_fields.setdefault('is_staff', True)
        return self.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
            address=address,
            role=UserRole.STAFF,
            **extra_fields
        )

    def create_vet(self, username, email, password=None, phone_number=None, address=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
            address=address,
            role=UserRole.VETERINARIAN,
            **extra_fields
        )

    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)     
        extra_fields.setdefault('is_superuser', True)   
        extra_fields.setdefault('role', UserRole.ADMIN)
        
        return self.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=None,   
            address=None,        
            **extra_fields
        )

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(max_length=100,blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER
    )

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"
    

class Staff(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name_staff = models.CharField(max_length=100)
    real_name_Staff=models.CharField(max_length=100,blank=False,null=True)
    phone_number_staff = models.CharField(max_length=15,null=True,blank=False)
    email_staff = models.EmailField(null=True,blank=True)
    images = models.ImageField(upload_to='images/staff/', null=True, blank=True)

    def __str__(self):
        return self.name_staff

class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name_customer = models.CharField(max_length=100)
    phone_number_customer = models.CharField(max_length=15,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    images = models.ImageField(upload_to='images/customer/', null=True, blank=True)
    email_customer = models.EmailField(null=True,blank=True)

    def __str__(self):
        return self.name_customer

class Veterinarian(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name_veterinarian = models.CharField(max_length=100)
    real_name_veterinarian=models.CharField(max_length=100,blank=True,null=True)
    phone_number_veterinarian = models.CharField(max_length=15,null=True,blank=True)
    specialization = models.CharField(max_length=100,null=True,blank=True)
    email_vet = models.EmailField(null=True,blank=True)
    images = models.ImageField(upload_to='images/veterinarian/', null=True, blank=True)

    def __str__(self):
        return self.name_veterinarian
    
class Pet(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    species = models.CharField(max_length=50, blank=True, null=True)   
    age = models.PositiveIntegerField(blank=True, null=True)  
    name_pet = models.CharField(max_length=100, blank=False, null=True) 
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=True)  
    pet_status = models.CharField(max_length=50, blank=False, null=True) 
    pet_type = models.CharField(max_length=50, blank=True, null=True) 
    images = models.ImageField(upload_to='images/pet/', null=True, blank=True) 
    is_male = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.name_pet} ({self.species})"



class MedicalHistory(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    date = models.DateField(null=True,blank=True)
    disease = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return f"Medical History for Pet {self.pet.name_pet} on {self.date}"



class VaccinationHistory(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="vaccination_histories")
    date = models.DateField(null=True,blank=True)
    vaccine_type = models.CharField(max_length=255,null=True,blank=True)
    dosage = models.CharField(max_length=50,null=True,blank=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Vaccination for {self.pet.name_pet} on {self.date}"
    
class Cage(models.Model):
    capacity = models.IntegerField(null=True,blank=True,validators=[MinValueValidator(1), MaxValueValidator(5)])

    
    def __str__(self):
            return f"Cage {self.id} with capacity {self.capacity}"
    

    

    
class Schedule(models.Model):
    veterinarian = models.ForeignKey(Veterinarian, on_delete=models.CASCADE)
    date = models.DateField(blank=False,null=True)
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    night = models.BooleanField(default=False)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['veterinarian', 'date'], name='unique_schedule_per_vet_per_day')
        ]


    def __str__(self):
        return f"Schedule for Veterinarian {self.veterinarian.name_veterinarian} on {self.date}"


class Booking(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True,blank=True)
    veterinarian = models.ForeignKey(Veterinarian, on_delete=models.SET_NULL, null=True,blank=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True,blank=True)
    cancel_date = models.DateTimeField(null=True, blank=True)
    refund_fee = models.DecimalField(max_digits=10, decimal_places=2,default=0, null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    store_pet = models.BooleanField(default=False)

    def calculate_refund(self):
        """Tính số tiền hoàn lại dựa trên thời gian hủy."""
        appointment_date = AppointmentDate.objects.get(hospitalization=self)
        if not self.cancel_date or not appointment_date :
            return 0
        
        days_before_booking = (appointment_date - self.cancel_date).days

        if days_before_booking >= 7:
            return self.prepayment_amount  
        elif 3 <= days_before_booking <= 6:
            return self.prepayment_amount * 0.75  
        else:
            return 0  

    def process_refund(self):
        """Cập nhật phí hoàn tiền khi hủy."""
        self.refund_fee = self.calculate_refund()
        self.save()
    
    def __str__(self):
        return f"Booking {self.id}"
    

    
    
class Examine(models.Model):
    pet=models.ForeignKey(Pet,on_delete=models.CASCADE)
    diagnosis = models.TextField(null=True,blank=True)
    symptom = models.TextField(null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True, blank=True)
    treatment_process = models.TextField(null=True,blank=True)
    result = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"Examine for Pet {self.pet.name_pet}"
    
class Hospitalization(models.Model):
    pet=models.ForeignKey(Pet,on_delete=models.CASCADE)
    cage=models.ForeignKey(Cage,on_delete=models.SET_NULL,null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True, blank=True)
    symptom = models.TextField(null=True,blank=True)
    def __str__(self):
        return f"Hospitalization for Pet {self.pet.name_pet} "
    
class UpdateStatus(models.Model):
    hospitalization=models.ForeignKey(Hospitalization,on_delete=models.CASCADE)
    date=models.DateField(null=True,blank=False)
    image = models.ImageField(upload_to='images/hospitalization/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"Update status for pet {self.hospitalization.pet.name_pet}"


class AppointmentDate(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True)  
    date = models.DateField(blank=True,null=True)
    morning = models.BooleanField(default=False)  
    afternoon = models.BooleanField(default=False)  
    night = models.BooleanField(default=False)  

    def __str__(self):
        return f"Booking {self.booking} - {self.date}"


class Cost(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True) 
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    extra_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    extra_service = models.TextField(blank=True,null=False)
    @property
    def calculate_service_fee(self):
        fee = 0
        try:
            form_booking = FormBooking.objects.get(booking=self.booking)
        except FormBooking.DoesNotExist:
            return fee

        if form_booking.examine:
            fee += 200000
        if form_booking.hospitalization:
            fee += 300000
        if form_booking.vaccination:
            fee += 500000

        return fee 

    def save(self, *args, **kwargs):
        self.service_fee = self.calculate_service_fee 
        super().save(*args, **kwargs)

    @property
    def total_fee(self):
        refund_fee = self.booking.refund_fee if self.booking.refund_fee is not None else Decimal('0.00')
        return self.service_fee + self.extra_fee - refund_fee

    
    def __str__(self):
        return f"Cost for Booking {self.booking.id}"


class FormBooking(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True)
    examine = models.BooleanField(default=False)
    hospitalization = models.BooleanField(default=False)
    vaccination = models.BooleanField(default=False)

    def __str__(self):
        return f"Form for Booking {self.booking.id}"

class BookingStatus(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True)
    cancelled = models.BooleanField(default=False)
    awaiting = models.BooleanField(default=True)
    confirm = models.BooleanField(default=False)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"Status for Booking {self.booking.id}"

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True) 
    form_customer = models.TextField(null=True,blank=True)
    time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True,blank=True,validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
       local_time = timezone.localtime(self.time)  
       return f"Review for Booking {self.booking.id} Time:{self.time}"
    




    


