from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)  # Auto-incrementing unique ID
    city = models.CharField(max_length=100)  # Name of the city

    def __str__(self):
        return f"{self.city} (ID: {self.location_id})"

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ['city']

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('Customer', 'Customer'),
        ('Service Provider', 'Service Provider'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"