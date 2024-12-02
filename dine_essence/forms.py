from django import forms
from .models import Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput, NumberInput, Select
from datetime import datetime, date, time, timedelta



class ReservationForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"readonly": "readonly"})
    )

    class Meta:
        model = Reservation
        fields = ['username', 'reservation_date', 'reservation_time', 'guest_count', 'email', 'phone']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),
            'reservation_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username

class CustomUserCreationForm(UserCreationForm):
    """
    Customized user registration form that includes an email field.
    """
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        """
        Save the provided password in hashed format.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EditReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['guest_count', 'reservation_date', 'reservation_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Predefined time slots (example: you can adjust this list as per your needs)
        self.time_slots = [
            "12:00", "12:30", "13:00", "13:30", "14:00", 
            "14:30", "15:00", "15:30", "16:00", "16:30", 
            "17:00", "17:30", "18:00", "18:30", "19:00",
            
        ]
        
        # Ensure guest_count and reservation_time have the right choices and validation
        self.fields['reservation_time'].choices = [(slot, slot) for slot in self.time_slots]

    def clean_reservation_time(self):
        reservation_time = self.cleaned_data['reservation_time']
        
        # Ensure the time is one of the predefined time slots
        if reservation_time not in self.time_slots:
            raise forms.ValidationError("Invalid time slot selected. Please choose a valid time.")
        
        return reservation_time

    def clean_reservation_date(self):
        reservation_date = self.cleaned_data['reservation_date']
        
        # Ensure the reservation date is not in the past
        if reservation_date < datetime.today().date():
            raise forms.ValidationError("The reservation date cannot be in the past.")
        
        return reservation_date