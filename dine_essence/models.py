from django.db import models
from django.contrib.auth.models import User
from datetime import time

# Create your models here.
class Table(models.Model):
    number = models.IntegerField(unique=True)
    seats = models.IntegerField()

    def __str__(self):
        return f"Table {self.number} - {self.seats} seats"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate reservation with a user
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100,  default="")
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    guest_count = models.PositiveIntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=15, default="")
   
    def __str__(self):
        return f"{self.reservation_date} at {self.reservation_time} for {self.guest_count} guests"


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

