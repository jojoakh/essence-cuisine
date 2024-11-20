from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, 'dine_essence/index.html')


def about(request):
    return render(request, 'dine_essence/about.html')


def book_table(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ReservationForm()
    return render(request, 'book_table.html', {'form': form})


def success(request):
    return render(request, 'success.html')