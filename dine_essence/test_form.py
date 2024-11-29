from django.test import TestCase
from .forms import ReservationForm
from django.utils import timezone


# Create your tests here.
class ReservationFormTest(TestCase):
    def setUp(self):
        # Set up some valid data for testing
        self.valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
            "email": "john.doe@example.com",
            "reservation_date": timezone.now().date(),
            "reservation_time": "12:00",
            "guests": 4
        }

    def test_valid_form_submission(self):
        """
        Test that the form is valid with correct data.
        """
        form = ReservationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_submission(self):
        """
        Test that the form is invalid with incorrect data.
        """
        invalid_data = self.valid_data.copy()
        invalid_data['first_name'] = ''
        form = ReservationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
