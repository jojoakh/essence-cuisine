from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('about/', views.about, name='about'),  
    path('reservation/', views.make_reservation, name='make_reservation'),
    path('menu/', views.menu_view, name='menu'),
]
