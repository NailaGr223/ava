from django.db import models
from accounts.models import CustomUser

class Bird(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='birds')
    title = models.CharField(max_length=200)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()  # in months
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    health_status = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='birds/')
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.breed}"
    
class CartItem(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.bird.title}"