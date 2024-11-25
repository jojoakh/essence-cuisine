from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservationForm


# Create your views here.
def index(request):
    return render(request, 'dine_essence/index.html')


def about(request):
    return render(request, 'dine_essence/about.html')


def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your reservation has been successfully submitted!")
            return redirect('index')  
    else:
        form = ReservationForm()
    return render(request, 'dine_essence/make_reservation.html', {'form': form})


