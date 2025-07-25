from django.db import models
from django.contrib.auth.models import User  # Import User model


class Ride(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides', null=True)  # New field
    pickup = models.CharField(max_length=255)
    dropoff = models.CharField(max_length=255)
    ride_type = models.CharField(max_length=50, choices=[
        ('UberX', 'UberX'),
        ('Comfort', 'Comfort'),
        ('Black', 'Black'),
        ('XL', 'UberXL')
    ])
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    pickup_lat = models.FloatField(null=True, blank=True)
    pickup_lng = models.FloatField(null=True, blank=True)
    dropoff_lat = models.FloatField(null=True, blank=True)
    dropoff_lng = models.FloatField(null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pickup} to {self.dropoff} ({self.ride_type})"
