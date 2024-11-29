from django import forms
from .models import Reservation


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

   