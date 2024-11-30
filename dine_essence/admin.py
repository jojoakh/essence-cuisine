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
    # Fields to display in the list view of the admin
    list_display = ('user', 'reservation_date', 'reservation_time', 'guest_count', 'email','first_name', 'last_name','phone')  
    
    # Searchable fields in the admin interface
    search_fields = ('user__username', 'user__email', 'email', 'reservation_date', 'reservation_time')  
    
    # Filters to make it easier to narrow down the results
    list_filter = ('reservation_date', 'reservation_time')  
    
    # Default ordering of the reservations by reservation date
    ordering = ('reservation_date',)  
    
    # Allows quick filtering by date in the admin interface
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






