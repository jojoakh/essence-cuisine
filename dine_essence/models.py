from django.db import models

# Create your models here.
class Table(models.Model):
    number = models.IntegerField(unique=True)
    seats = models.IntegerField()

    def __str__(self):
        return f"Table {self.number} - {self.seats} seats"

class Reservation(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    reservation_date = models.DateTimeField()
    guests = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation for {self.full_name} on {self.reservation_date}"

