from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('vet', 'Veterinarian'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # For Vets
    is_verified = models.BooleanField(default=False)
    certificate = models.FileField(upload_to='vet_certificates/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"