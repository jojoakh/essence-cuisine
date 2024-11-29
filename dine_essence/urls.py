from django.urls import path
from . import views
from .views import check_availability

urlpatterns = [
    path('', views.index, name='index'),  
    path('about/', views.about, name='about'),  
    path('reservation/', views.make_reservation, name='make_reservation'),
    path('reservation/confirmation/<int:reservation_id>/', views.reservation_confirmation, name='reservation_confirmation'),
    path('reservation/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('check-availability/', check_availability, name='check_availability'),
    path('menu/', views.menu_view, name='menu'),
]