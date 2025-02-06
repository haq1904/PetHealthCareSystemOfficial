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
    address = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER
    )

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Customer(models.Model):
    id_customer = models.AutoField(primary_key=True)
    name_customer = models.CharField(max_length=100)
    phone_number_customer = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    email_customer = models.EmailField()

    def __str__(self):
        return self.name_customer
    

class Pet(models.Model):
    id_pet = models.AutoField(primary_key=True)
    species = models.CharField(max_length=50)  
    age = models.PositiveIntegerField()  
    name_pet = models.CharField(max_length=100) 
    weight = models.DecimalField(max_digits=5, decimal_places=2)  
    pet_status = models.CharField(max_length=50, blank=True, null=True) 
    pet_type = models.CharField(max_length=50, blank=True, null=True)  

    def __str__(self):
        return f"{self.name_pet} ({self.species})"

class Examine(models.Model):
    id_examine = models.AutoField(primary_key=True)
    id_pet = models.ForeignKey('Pet', on_delete=models.CASCADE)
    diagnosis = models.TextField()
    symptom = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    treatment_process = models.TextField()
    result = models.TextField()

    def __str__(self):
        return f"Examine for Pet {self.id_pet.id_pet}"

class MedicalHistory(models.Model):
    id_pet = models.ForeignKey('Pet', on_delete=models.CASCADE)
    date = models.DateField()
    disease = models.CharField(max_length=255)

    def __str__(self):
        return f"Medical History for Pet {self.id_pet.id_pet} on {self.date}"


class Gender(models.Model):
    id_pet = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name="gender")
    is_male = models.BooleanField()

    def __str__(self):
        return f"Gender of {self.id_pet.name_pet}: {'Male' if self.is_male else 'Female'}"


class VaccinationHistory(models.Model):
    id_pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="vaccination_histories")
    date = models.DateField()
    vaccine_type = models.CharField(max_length=255)
    dosage = models.CharField(max_length=50)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Vaccination for {self.id_pet.name_pet} on {self.date}"
    
class Hospitalization(models.Model):
    id_hospitalization = models.AutoField(primary_key=True)
    id_pet = models.ForeignKey('Pet', on_delete=models.CASCADE)
    id_cage = models.ForeignKey('Cage', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    symptom = models.TextField()

    def __str__(self):
        return f"Hospitalization for Pet {self.id_pet.id_pet} in Cage {self.id_cage.id_cage}"

class PetStatus(models.Model):
    id_hospitalization = models.ForeignKey('Hospitalization', on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/',null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Status for Pet in Hospitalization {self.id_hospitalization}"

    


class Staff(models.Model):
    id_staff = models.AutoField(primary_key=True) 
    name_staff = models.CharField(max_length=100)  
    phone_number_staff = models.CharField(max_length=15)  
    email_staff = models.EmailField(max_length=100)  


    def __str__(self):
        return self.name_staff


class Veterinarian(models.Model):
    id_veterinarian = models.AutoField(primary_key=True) 
    name_veterinarian = models.CharField(max_length=100) 
    phone_number_veterinarian = models.CharField(max_length=15) 
    specialization = models.CharField(max_length=100)  
    email_vet = models.EmailField(max_length=100)  

    def __str__(self):
        return self.name_veterinarian
    
class Schedule(models.Model):
    id_schedule = models.AutoField(primary_key=True)
    id_veterinarian = models.ForeignKey('Veterinarian', on_delete=models.CASCADE)
    date = models.DateField()
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    night = models.BooleanField(default=False)

    def __str__(self):
        return f"Schedule for Veterinarian {self.id_veterinarian.name_veterinarian} on {self.date}"


class Booking(models.Model):
    id_booking = models.AutoField(primary_key=True)
    id_customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False,blank=False)
    id_staff = models.ForeignKey('Staff', on_delete=models.SET_NULL, null=True,blank=True)
    id_pet = models.ForeignKey('Pet', on_delete=models.SET_NULL, null=True,blank=True)
    id_veterinarian = models.ForeignKey('Veterinarian', on_delete=models.SET_NULL, null=True,blank=True)
    cancel_date = models.DateTimeField(null=True, blank=True)
    refund_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id_booking}"


class Cost(models.Model):
    id_booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    additional_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Cost for Booking {self.id_booking}"

class Form(models.Model):
    id_booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    examine = models.BooleanField(default=False)
    hospitalization = models.BooleanField(default=False)
    vaccination = models.BooleanField(default=False)

    def __str__(self):
        return f"Form for Booking {self.id_booking}"

class BookingStatus(models.Model):
    id_booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    cancelled = models.BooleanField(default=False)
    awaiting = models.BooleanField(default=False)
    confirm = models.BooleanField(default=False)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"Status for Booking {self.id_booking}"

class Review(models.Model):
    id_review = models.AutoField(primary_key=True)
    id_booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    form_customer = models.ForeignKey('Customer', null=True, on_delete=models.SET_NULL)
    form_veterinarian = models.ForeignKey('Veterinarian', null=True, on_delete=models.SET_NULL)
    time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()

    def __str__(self):
        return f"Review for Booking {self.id_booking}"
    
class Cage(models.Model):
    id_cage = models.AutoField(primary_key=True)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Cage {self.id_cage} with Capacity {self.capacity}"

class CageType(models.Model):
    id_cage = models.ForeignKey('Cage', on_delete=models.CASCADE, primary_key=True)
    isolation = models.BooleanField(default=False)
    recovery = models.BooleanField(default=False)
    long_term = models.BooleanField(default=False)
    short_term = models.BooleanField(default=False)

    def __str__(self):
        return f"Cage Type for Cage {self.id_cage}"

class CageStatus(models.Model):
    id_cage = models.ForeignKey('Cage', on_delete=models.CASCADE, primary_key=True)
    vacant = models.BooleanField(default=True)
    in_use = models.BooleanField(default=False)
    dirty = models.BooleanField(default=False)

    def __str__(self):
        return f"Status for Cage {self.id_cage}"
    


