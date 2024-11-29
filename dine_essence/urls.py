from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import check_availability

urlpatterns = [
    path('', views.index, name='index'),  
    path('about/', views.about, name='about'), 
    path('login/', auth_views.LoginView.as_view(template_name='dine_essence/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'), 
    path('reservation/', views.make_reservation, name='make_reservation'),
    path('reservation/confirmation/<int:reservation_id>/', views.reservation_confirmation, name='reservation_confirmation'),
    path('reservation/update/<int:reservation_id>/', views.update_reservation, name='update_reservation'),
    path('reservation/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('check-availability/', check_availability, name='check_availability'),
    path('menu/', views.menu_view, name='menu'),
]