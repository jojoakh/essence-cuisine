from django import forms
from .models import Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date

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
        fields = ['reservation_date', 'reservation_time', 'guest_count']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Limit guest count to 1-10
        self.fields['guest_count'].widget = forms.NumberInput(attrs={
            'type': 'number', 
            'min': 1, 
            'max': 10
        })

        # Filter reservation_time based on availability
        if 'reservation_date' in self.initial:
            selected_date = self.initial['reservation_date']
            now = datetime.now()

            if selected_date == now.date():
                # Only allow future times for today
                available_times = [
                    time for time in Reservation.TIME_CHOICES 
                    if datetime.combine(selected_date, time[0]) > now
                ]
            else:
                # Show all times for future dates
                available_times = Reservation.TIME_CHOICES

            self.fields['reservation_time'].choices = available_times
        
