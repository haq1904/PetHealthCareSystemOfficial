from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from .models import Pet,Booking, FormBooking,Schedule,Review
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

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'morning', 'afternoon', 'night']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}), 
        }

    class Meta:
        model = Schedule
        fields = [ 'date']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pet', 'cancel_date', 'refund_fee', 'store_pet']
        widgets = {
            'cancel_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'refund_fee': forms.NumberInput(attrs={'step': '0.01'}) 
        }

class AppointmentDateForm(forms.ModelForm):
    class Meta:
        model = AppointmentDate
        fields = [ 'date', 'morning', 'afternoon', 'night']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class FormBookingForm(forms.ModelForm):
    class Meta:
        model = FormBooking
        fields = ['examine', 'hospitalization', 'vaccination']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['form_customer', 'score']  
        widgets = {
            'form_customer': forms.Textarea(attrs={'style':' width: 200px; height: 30px; resize: none;','class': 'form-control', 'placeholder': 'Nhập đánh giá của bạn...'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 5}),
        }
        labels = {
            'form_customer': 'Đánh giá của bạn',
            'score': 'Điểm số (0-5)',
        }


class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = UpdateStatus
        fields = ['date', 'image', 'description']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        hospitalization = self.cleaned_data.get('hospitalization')

        if hospitalization:
            start_date = hospitalization.start_date
            end_date = hospitalization.end_date

            if start_date and end_date and not (start_date <= date <= end_date):
                raise forms.ValidationError("📅 Ngày cập nhật phải nằm trong khoảng thời gian nhập viện.")

        return date