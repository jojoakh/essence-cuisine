from django.db import models
from django.contrib.auth.models import User
from datetime import time

# Create your models here.
# Reservation model
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    guest_count = models.PositiveIntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=15, default="")

    def __str__(self):
        return (f"{self.reservation_date} "
                f"at {self.reservation_time} "
                f"for {self.guest_count} guests")

# Menu model
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('starter', 'Starter'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')],
        default='USD'
    )

    def __str__(self):
        return self.name
