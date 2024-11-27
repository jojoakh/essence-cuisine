from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "reservation_date",
            "reservation_time",
            "guests",
        ]
        widgets = {
            "reservation_date": forms.DateInput(attrs={"type": "date"}),
            "reservation_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        reservation_date = cleaned_data.get("reservation_date")
        reservation_time = cleaned_data.get("reservation_time")

        # Check for double booking
        if Reservation.objects.filter(
            reservation_date=reservation_date, 
            reservation_time=reservation_time
        ).exists():
            raise ValidationError(
                "This time slot is already booked. Please choose another."
            )

        return cleaned_data
