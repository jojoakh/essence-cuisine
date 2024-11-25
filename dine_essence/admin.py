from django.contrib import admin
from .models import Table, Reservation
from django_summernote.admin import SummernoteModelAdmin

# Register the Table model
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'seats')  
    search_fields = ('number',)  
    ordering = ('number',)  

# Register the Reservation model
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'reservation_date', 'guests')  
    search_fields = ('first_name', 'last_name', 'email', 'phone')  
    list_filter = ('reservation_date',) 
    ordering = ('reservation_date',) 
    date_hierarchy = 'reservation_date' 

