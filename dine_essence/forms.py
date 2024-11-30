from django import forms
from .models import Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReservationForm(forms.ModelForm):
    """
    Form for creating and updating reservations.
    """
    class Meta:
        model = Reservation
        fields = ['reservation_date', 'reservation_time', 'guest_count', 'email', 'first_name', 'last_name','phone']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),
            'reservation_time': forms.TimeInput(attrs={'type': 'time'}),
        }

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
