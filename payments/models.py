from django.db import models
from django.contrib.auth.models import User


class Ride(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup = models.CharField(max_length=255)
    dropoff = models.CharField(max_length=255)
    ride_type = models.CharField(max_length=100)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.pickup} to {self.dropoff}"