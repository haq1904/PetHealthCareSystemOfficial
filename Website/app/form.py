from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from .models import Pet

class CreateUserForm (UserCreationForm) :
    class Meta():
        model=CustomUser
        fields = ('username' , 'email', 'password1', 'password2')


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name_pet','pet_type','species','age','weight','pet_status','is_male']
        widgets = {
            'name_pet': forms.TextInput(attrs={'class': 'form-control'}),
            'pet_type': forms.TextInput(attrs={'class': 'form-control'}),
            'species': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'pet_status': forms.TextInput(attrs={'class': 'form-control'}),
            'is_male': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }