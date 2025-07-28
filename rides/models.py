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


class SharedRideInvite(models.Model):
    ride = models.ForeignKey('rides.SharedRide', related_name='invites', on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(null=True, blank=True)  # None = pending
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invite to {self.invitee.username} for ride ID {self.ride.id}"


class SharedRide(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup = models.CharField(max_length=255)
    dropoff = models.CharField(max_length=255)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"{self.organizer} - {self.pickup} to {self.dropoff}"


def check_ride_status(ride):
    """
    Updates the ride status based on invitations.
    """
    invites = ride.invites.all()
    if all(invite.accepted is not None for invite in invites):
        ride.status = "approved" if any(inv.accepted for inv in invites) else "declined"
        ride.save()


class ChatMessage(models.Model):
    ride = models.ForeignKey('rides.SharedRide', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']