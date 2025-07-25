from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username