from django.shortcuts import render, redirect, get_object_or_404
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


def menu_view(request):
    categories = MenuItem.objects.values('category').distinct()  
    menu_items = MenuItem.objects.all()  
    context = {
        'categories': categories,
        'menu_items': menu_items,
    }

    return render(request, 'dine_essence/menu.html', context)

