from django import forms
from .models import Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, time, date


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

        # Set the min date for the reservation_date field to prevent selecting past dates
        self.fields['reservation_date'].widget = forms.DateInput(attrs={
            'type': 'date',
            'min': date.today().strftime('%Y-%m-%d')  # Prevent past dates
        })

        # Dynamically adjust available times based on reservation_date
        if 'reservation_date' in self.initial:
            selected_date = self.initial['reservation_date']

            # Get current time and date
            now = datetime.now()

            if selected_date == now.date():
                # Filter times for today: only allow future times
                self.fields['reservation_time'].widget = forms.Select(choices=[
                    (self._time_to_str(time_obj), self._time_to_str(time_obj, "%I:%M %p"))
                    for time_obj in self._get_available_times(selected_date)
                    if datetime.combine(selected_date, time_obj) > now
                ])
            else:
                # Show all available times for future dates
                self.fields['reservation_time'].widget = forms.Select(choices=[
                    (self._time_to_str(time_obj), self._time_to_str(time_obj, "%I:%M %p"))
                    for time_obj in self._get_available_times(selected_date)
                ])

    def _get_available_times(self, selected_date):
        """
        Fetch available times as a list of `datetime.time` objects from 11:00 AM to 9:00 PM,
        with slots every 30 minutes. Removes times that are already booked.
        """
        # Create time slots from 11:00 AM to 9:00 PM, every 30 minutes
        time_slots = []
        start_hour = 11  # Start at 11:00 AM
        end_hour = 21  # End at 9:00 PM

        for hour in range(start_hour, end_hour + 1):
            # Create both 00 and 30 minute intervals for each hour
            time_slots.append(time(hour, 0))  # 00 minute (e.g., 11:00, 12:00)
            time_slots.append(time(hour, 30))  # 30 minute (e.g., 11:30, 12:30)

        # Retrieve existing reservations for the selected date
        booked_slots = Reservation.objects.filter(reservation_date=selected_date)

        # Remove the booked slots from the available time slots
        available_slots = [
            time_obj for time_obj in time_slots
            if not booked_slots.filter(reservation_time=time_obj.strftime("%H:%M")).exists()
        ]

        return available_slots

    def _time_to_str(self, time_obj, format_str="%H:%M"):
        """
        Convert time object to string format.
        Default format: "%H:%M" (24-hour format).
        """
        return time_obj.strftime(format_str)