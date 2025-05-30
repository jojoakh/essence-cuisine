from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.utils import timezone
from .forms import ReservationForm
from .forms import EditReservationForm
from .models import Reservation
from .models import MenuItem
from datetime import datetime, time, date, timedelta


# Create your views here.
def index(request):
    return render(request, 'dine_essence/index.html')


def about(request):
    return render(request, 'dine_essence/about.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "Account created successfully! "
                             "You can now log in.")
            return redirect('login')
        else:
            messages.error(request,
                           "Error creating account. Please check the form.")
    else:
        form = UserCreationForm()
    return render(request, 'dine_essence/signup.html', {'form': form})


@login_required
def user_dashboard(request):
    # Get all reservations for the logged-in user
    user_reservations = Reservation.objects.filter(user=request.user)
    return render(
        request,
        'dine_essence/dashboard.html',
        {'reservations': user_reservations}
        )


@login_required
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Save reservation data
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            messages.success(request, "Reservation successfully created!")
            return redirect(
                'reservation_confirmation',
                reservation_id=reservation.id)
    else:
        # Check if a reservation is in progress
        if 'guests' not in request.session:
            # Start the reservation process if not already initiated
            guest_numbers = range(1, 11)  # Adjust range as needed
            today_date = date.today()
            return render(request, 'dine_essence/make_reservation.html', {
                'guest_numbers': guest_numbers,
                'today_date': today_date,
            })

        # If already in progress, populate form with session data
        initial_data = {
            'guest_count': request.session.get('guests'),
            'reservation_date': request.session.get('reservation_date'),
            'reservation_time': request.session.get('reservation_time'),
        }
        form = ReservationForm(initial=initial_data)

    return render(
        request, 'dine_essence/make_reservation.html', {'form': form})


@login_required
def reservation_confirmation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id,
                                    user=request.user)

    return render(
        request,
        'dine_essence/confirmation.html', {'reservation': reservation})


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    # Authorization check to ensure only the owner can edit
    if reservation.user != request.user:
        return HttpResponseForbidden(
            "You are not allowed to access this reservation.")

    # Prevent editing past reservations
    reservation_datetime = timezone.make_aware(
        datetime.combine(reservation.reservation_date,
                         reservation.reservation_time)
    )
    if reservation_datetime < timezone.now():
        messages.error(request,
                       "This reservation has already passed "
                       "and cannot be edited.")
        return redirect('dashboard')

    # Generate available time slots (11:00 AM – 9:00 PM in 30-min intervals)
    start_time = time(11, 0)
    end_time = time(21, 0)
    time_slots = []
    now = timezone.now()
    current_time = datetime.combine(date.today(), start_time)

    while current_time.time() <= end_time:
        # Only show future time slots if the reservation date is today
        if reservation.reservation_date > now.date() or (
            reservation.reservation_date == now.date()
            and current_time.time() >= now.time()
        ):
            time_slots.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=30)

    # Exclude already booked slots (excluding the current reservation)
    if reservation.reservation_date:
        booked_slots = Reservation.objects.filter(
            reservation_date=reservation.reservation_date
        ).exclude(pk=reservation.pk).values_list('reservation_time', flat=True)

        booked_slots = [slot.strftime("%H:%M") for slot in booked_slots]
        time_slots = [slot for slot in time_slots if slot not in booked_slots]

    # 📝 Initialize form with dynamic time slots
    form = EditReservationForm(
        request.POST or None,
        instance=reservation,
        time_slots=time_slots
    )

    if request.method == 'POST':
        if form.is_valid():
            new_reservation_date = form.cleaned_data['reservation_date']
            new_reservation_time = form.cleaned_data['reservation_time']

            # Combine into a datetime object and make it timezone-aware
            new_datetime = timezone.make_aware(datetime.combine(
                new_reservation_date,
                datetime.strptime(new_reservation_time, "%H:%M").time()
            ))

            # Final validation: can't select a past date/time
            if new_datetime < timezone.now():
                form.add_error('reservation_time',
                               "You cannot select a past date or time.")
            elif Reservation.objects.filter(
                reservation_date=new_reservation_date,
                reservation_time=new_reservation_time
            ).exclude(pk=reservation.pk).exists():
                form.add_error('reservation_time',
                               "The selected time slot is already booked.")
            else:
                form.save()
                messages.success(request, "Reservation updated successfully!")
                return redirect('dashboard')

    return render(request, 'dine_essence/edit_reservation.html', {
        'form': form,
        'reservation': reservation,
        'today': timezone.now().date().strftime("%Y-%m-%d"),
        'guest_count_range': range(1, 11),
        'time_slots': time_slots,
    })


def check_availability(request):
    # Get the date from the request
    date = request.GET.get("date")

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


@login_required
def cancel_reservation(request, reservation_id):
    # Fetch user's reservation
    reservation = get_object_or_404(Reservation, id=reservation_id,
                                    user=request.user)

    if request.method == 'POST':
        # Delete the reservation
        reservation.delete()
        messages.success(request,
                         "Your reservation has been successfully canceled.")
        return redirect('dashboard')

    # Render the cancellation confirmation page
    return render(
        request,
        'dine_essence/cancel_reservation.html',
        {'reservation': reservation}
        )


def menu_view(request):
    categories = MenuItem.objects.values('category').distinct()
    menu_items = MenuItem.objects.all()
    context = {
        'categories': categories,
        'menu_items': menu_items,
    }

    return render(request, 'dine_essence/menu.html', context)
