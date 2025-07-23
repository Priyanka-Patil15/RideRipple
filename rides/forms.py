from django import forms
from .models import Ride
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['pickup', 'dropoff', 'ride_type', 'date', 'time']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
