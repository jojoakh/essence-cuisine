from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Table, Reservation
from .models import MenuItem

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


# Register the MenuItem model
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'formatted_price')  # Use 'formatted_price' instead of 'price'
    list_filter = ('category',)
    search_fields = ('name', 'category')

    def formatted_price(self, obj):
        # Return the price with the currency symbol
        currency_symbols = {'USD': '$', 'EUR': '€', 'GBP': '£'}
        currency_symbol = currency_symbols.get(obj.currency, obj.currency)  # Default to currency code if symbol not found
        return f"{currency_symbol}{obj.price:.2f}"  # Format the price with 2 decimal places
    formatted_price.short_description = 'Price'  # Column header in the admin panel






