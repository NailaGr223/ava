from django.db import models
from accounts.models import CustomUser

class Bird(models.Model):
    LISTING_TYPE_CHOICES = [
        ('sell', 'For Sale'),
        ('rehome', 'Rehoming'),
        ('adopt', 'Adoption'),
        ('food', 'Bird Food & Supplies'),
    ]

    seller = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, default='sell')
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)  # months
    gender = models.CharField(max_length=10, blank=True)
    health_status = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='listings/')
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_listing_type_display()})"
    
class CartItem(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.bird.title}"
    
class Wishlist(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'bird')

    def __str__(self):
        return f"{self.user.username} - {self.bird.title}"