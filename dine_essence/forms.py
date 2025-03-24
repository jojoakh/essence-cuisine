from django import forms
from .models import Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
import re


# form for handling reservation
class ReservationForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"readonly": "readonly"})
    )

    class Meta:
        model = Reservation
        fields = ['username', 'reservation_date',
                  'reservation_time', 'guest_count', 'email', 'phone']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),
            'reservation_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        pattern = re.compile(r'^\+?\d{10,15}$')
        if not pattern.match(phone):
            raise ValidationError(
                "Enter a valid phone number (10-15 digits, optional '+').")
        return phone


class CustomUserCreationForm(UserCreationForm):
    """
    Customized user registration form that includes an email field.
    """
    email = forms.EmailField(required=True,
                             help_text="Enter a valid email address.")

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


# form for editting reservation
class EditReservationForm(forms.ModelForm):
    reservation_date = forms.DateField(
        widget=forms.SelectDateWidget(),
        label="Reservation Date"
    )
    reservation_time = forms.ChoiceField(
        choices=[],  # This will be dynamically filled with available slots
        label="Reservation Time"
    )
    guest_count = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.Select(choices=[(i, i) for i in range(1, 11)]),
        label="Number of Guests"
    )

    class Meta:
        model = Reservation
        fields = ['reservation_date', 'reservation_time', 'guest_count']

    def __init__(self, *args, **kwargs):
        # Pop the time_slots list so it can be passed dynamically
        time_slots = kwargs.pop('time_slots', [])
        super().__init__(*args, **kwargs)

        # Update the reservation_time field choices dynamically
        self.fields['reservation_time'].choices = [(slot, slot)
                                                   for slot in time_slots]

    def clean_reservation_date(self):
        # Ensure the selected date is not in the past
        selected_date = self.cleaned_data['reservation_date']
        if selected_date < timezone.now().date():
            raise ValidationError("You cannot select a past date.")
        return selected_date

    def clean_reservation_time(self):
        # Ensure the selected time is one of the available time slots
        selected_time = self.cleaned_data['reservation_time']
        available_slots = dict(self.fields['reservation_time'].choices)
        if selected_time not in available_slots:
            raise ValidationError("Please select a valid available time.")
        return selected_time
