from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservationForm
from .models import MenuItem



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


def menu_view(request):
    categories = MenuItem.objects.values('category').distinct()  
    menu_items = MenuItem.objects.all()  
    context = {
        'categories': categories,
        'menu_items': menu_items,
    }

    return render(request, 'dine_essence/menu.html', context)

