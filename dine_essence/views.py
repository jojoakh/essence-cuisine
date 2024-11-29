from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from datetime import datetime
from .forms import ReservationForm
from .models import Reservation
from .models import MenuItem
from datetime import date


# Create your views here.
def index(request):
    return render(request, 'dine_essence/index.html')


def about(request):
    return render(request, 'dine_essence/about.html')


def make_reservation(request):
    today_date = date.today()
    guest_numbers = range(1, 9)  # Allow guests between 1 and 8
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Save the reservation
            reservation = form.save()
            
            # Provide success message to the user
            messages.success(request, "Your reservation has been successfully submitted!")
            
            # Redirect to confirmation page
            return redirect('reservation_confirmation', reservation_id=reservation.id)
        else:
            # If form is not valid, show an error message or return the form with errors
            messages.error(request, "There was an error with your reservation. Please check the form.")
    else:
        form = ReservationForm()

    # Render the reservation form on GET request with context for today_date and guest_numbers
    return render(request, 'dine_essence/make_reservation.html', {
        'form': form,
        'today_date': today_date,
        'guest_numbers': guest_numbers
    })

    
def check_availability(request):
    # Get the date and number of guests from the request
    date = request.GET.get("date")
    guests = int(request.GET.get("guests"))

    # Ensure the date is valid
    if not date:
        return JsonResponse({"error": "Date is required"}, status=400)

    # Parse the date (optional: validate date format)
    parsed_date = parse_date(date)
    if not parsed_date:
        return JsonResponse({"error": "Invalid date format"}, status=400)

    # Retrieve all reservations for the given date
    booked_slots = Reservation.objects.filter(reservation_date=parsed_date)

    # Define all available time slots
    slots = [
        {"time": "11:00", "available": True},
        {"time": "11:30", "available": True},
        {"time": "12:00", "available": True},
        {"time": "12:30", "available": True},
        {"time": "13:00", "available": True},
        {"time": "13:30", "available": True},
        {"time": "14:00", "available": True},
        {"time": "14:30", "available": True},
        {"time": "15:00", "available": True},
        {"time": "15:30", "available": True},
        {"time": "16:00", "available": True},
        {"time": "16:30", "available": True},
        {"time": "17:00", "available": True},
        {"time": "17:30", "available": True},
        {"time": "18:00", "available": True},
        {"time": "18:30", "available": True},
        {"time": "19:00", "available": True},
        {"time": "19:30", "available": True},
        {"time": "20:00", "available": True},
        {"time": "20:30", "available": True},
        {"time": "21:00", "available": True},
    ]

    # Loop through booked slots and mark them as unavailable
    for slot in slots:
        if booked_slots.filter(reservation_time=slot["time"]).exists():
            slot["available"] = False

    return JsonResponse({"slots": slots})
    
def reservation_confirmation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'dine_essence/confirmation.html', {'reservation': reservation})

def cancel_reservation(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        confirm = request.POST.get('confirm', 'no')  # Check if this is a confirmation step

        # Validate the email input
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return render(request, 'dine_essence/cancel_reservation.html')  # Re-render the form with an error

        # Handle confirmation step
        if confirm == 'yes':
            try:
                # Find the reservation by email
                reservation = Reservation.objects.filter(email=email).first()
                if reservation:
                    reservation.delete()  # Delete the reservation
                    messages.success(request, "Your reservation has been successfully canceled.")
                else:
                    messages.error(request, "No reservations found for the provided email.")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
            return redirect('index')  # Redirect to homepage or another page after cancellation

        # Handle showing reservation details
        reservation = Reservation.objects.filter(email=email).first()
        if reservation:
            return render(request, 'dine_essence/confirm_cancellation.html', {'reservation': reservation, 'email': email})
        else:
            messages.error(request, "No reservations found for the provided email.")
            return redirect('cancel_reservation')  # Redirect back to the cancellation form

    # Render the cancellation form on GET request
    return render(request, 'dine_essence/cancel_reservation.html')

    
def menu_view(request):
    categories = MenuItem.objects.values('category').distinct()  
    menu_items = MenuItem.objects.all()  
    context = {
        'categories': categories,
        'menu_items': menu_items,
    }

    return render(request, 'dine_essence/menu.html', context)

