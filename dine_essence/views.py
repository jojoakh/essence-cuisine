from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponse
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
    guest_numbers = range(1, 9) 
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()  
            messages.success(request, "Your reservation has been successfully submitted!")
            return redirect('reservation_confirmation', reservation_id=reservation.id)  
    else:
        form = ReservationForm()

    # Render the reservation form on GET request
    return render(request, 'dine_essence/make_reservation.html', {
        'form': form,
        'today_date': today_date,
        'guest_numbers': guest_numbers
    })

    
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
                reservation = Reservation.objects.filter(email=email).first()
                if reservation:
                    reservation.delete()
                    messages.success(request, "Your reservation has been successfully canceled.")
                else:
                    messages.error(request, "No reservations found for the provided email.")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
            return redirect('index')

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

