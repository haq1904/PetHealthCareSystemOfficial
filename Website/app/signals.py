from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Staff, Customer, Veterinarian

User = get_user_model()

@receiver(user_logged_in)
def create_role_specific_object(sender, request,user, **kwargs):
    print("Signal user_logged_in triggered for user:", user)
    if user.role == 'staff':
        if not Staff.objects.filter(user=user).exists():
            Staff.objects.create(user=user, name_staff=user.username)
    elif user.role == 'veterinarian':
        if not Veterinarian.objects.filter(user=user).exists():
            Veterinarian.objects.create(user=user, name_veterinarian=user.username)
    elif user.role == 'user':
        if not Customer.objects.filter(user=user).exists():
            Customer.objects.create(user=user, name_customer=user.username)
