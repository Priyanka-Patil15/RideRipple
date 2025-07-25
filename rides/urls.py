from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('dash/', views.home, name='home'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('login/', auth_views.LoginView.as_view(template_name='rides/login.html'), name='login'),
    path('register/', views.register_view, name='register'),
    path('rides/history/', views.ride_history, name='ride-history'),
    path('rides/book/', views.book_ride, name='book-ride'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('rides/confirmed/', views.ride_confirmed, name='ride-confirmed'),
    path('rides/track/<int:ride_id>/', views.track_ride, name='track-ride'),
    path('schedule-ride/', views.schedule_ride, name='schedule_ride'),
    path('reserved-rides/', views.reserved_rides, name='reserved_rides'),
]
