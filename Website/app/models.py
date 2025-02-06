from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


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
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
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
    phone_number_staff = models.CharField(max_length=15,null=True,blank=True)
    email_staff = models.EmailField(null=True,blank=True)

    def __str__(self):
        return self.name_staff

class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name_customer = models.CharField(max_length=100)
    phone_number_customer = models.CharField(max_length=15,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    email_customer = models.EmailField(null=True,blank=True)

    def __str__(self):
        return self.name_customer

class Veterinarian(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name_veterinarian = models.CharField(max_length=100)
    phone_number_veterinarian = models.CharField(max_length=15,null=True,blank=True)
    specialization = models.CharField(max_length=100,null=True,blank=True)
    email_vet = models.EmailField(null=True,blank=True)

    def __str__(self):
        return self.name_veterinarian
    
class Pet(models.Model):
    species = models.CharField(max_length=50)  
    age = models.PositiveIntegerField()  
    name_pet = models.CharField(max_length=100) 
    weight = models.DecimalField(max_digits=5, decimal_places=2)  
    pet_status = models.CharField(max_length=50, blank=True, null=True) 
    pet_type = models.CharField(max_length=50, blank=True, null=True)  

    def __str__(self):
        return f"{self.name_pet} ({self.species})"

class Examine(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    diagnosis = models.TextField(null=True,blank=True)
    symptom = models.TextField(null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True, blank=True)
    treatment_process = models.TextField(null=True,blank=True)
    result = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"Examine for Pet {self.pet.name_pet}"

class MedicalHistory(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    date = models.DateField(null=True,blank=True)
    disease = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return f"Medical History for Pet {self.pet.name_pet} on {self.date}"


class Gender(models.Model):
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name="gender")
    is_male = models.BooleanField(null=True,blank=True)

    def __str__(self):
        return f"Gender of {self.pet.name_pet}: {'Male' if self.is_male else 'Female'}"


class VaccinationHistory(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="vaccination_histories")
    date = models.DateField(null=True,blank=True)
    vaccine_type = models.CharField(max_length=255,null=True,blank=True)
    dosage = models.CharField(max_length=50,null=True,blank=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Vaccination for {self.pet.name_pet} on {self.date}"
    
class Cage(models.Model):
    cage = models.AutoField(primary_key=True)
    capacity = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"Cage {self.id} with Capacity {self.capacity}"
    
class Hospitalization(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    cage = models.ForeignKey(Cage, on_delete=models.CASCADE)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True, blank=True)
    symptom = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"Hospitalization for Pet {self.pet.name_pet} in Cage {self.cage.id}"

class PetStatus(models.Model):
    hospitalization = models.ForeignKey(Hospitalization, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/',null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Status for Pet in Hospitalization {self.hospitalization.id}"

    
class Schedule(models.Model):
    veterinarian = models.ForeignKey(Veterinarian, on_delete=models.CASCADE)
    date = models.DateField()
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    night = models.BooleanField(default=False)

    def __str__(self):
        return f"Schedule for Veterinarian {self.id} on {self.date}"


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True,blank=True)
    veterinarian = models.ForeignKey(Veterinarian, on_delete=models.SET_NULL, null=True,blank=True)
    pet = models.ForeignKey(Pet, on_delete=models.SET_NULL, null=True,blank=True)
    cancel_date = models.DateTimeField(null=True, blank=True)
    refund_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id}"


class Cost(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    additional_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Cost for Booking {self.booking.id}"

class Form(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    examine = models.BooleanField(default=False)
    hospitalization = models.BooleanField(default=False)
    vaccination = models.BooleanField(default=False)

    def __str__(self):
        return f"Form for Booking {self.booking.id}"

class BookingStatus(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    cancelled = models.BooleanField(default=False)
    awaiting = models.BooleanField(default=False)
    confirm = models.BooleanField(default=False)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"Status for Booking {self.booking.id}"

class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    form_customer = models.TextField(null=True,blank=True)
    form_veterinarian = models.TextField(null=True,blank=True)
    time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"Review for Booking {self.booking.id}"
    


class CageType(models.Model):
    cage = models.ForeignKey(Cage, on_delete=models.CASCADE)
    isolation = models.BooleanField(default=False)
    recovery = models.BooleanField(default=False)
    long_term = models.BooleanField(default=False)
    short_term = models.BooleanField(default=False)

    def __str__(self):
        return f"Cage Type for Cage {self.cage.id}"

class CageStatus(models.Model):
    cage = models.ForeignKey(Cage, on_delete=models.CASCADE)
    vacant = models.BooleanField(default=True)
    in_use = models.BooleanField(default=False)
    dirty = models.BooleanField(default=False)

    def __str__(self):
        return f"Status for Cage {self.cage.id}"
    


