from django.contrib import admin
from .models import Bird, CartItem, Wishlist

@admin.register(Bird)
class BirdAdmin(admin.ModelAdmin):
    list_display = ('title', 'listing_type', 'breed', 'price', 'location', 'is_available', 'created_at')
    list_filter = ('listing_type', 'is_available', 'seller')
    search_fields = ('title', 'breed', 'description', 'location')
    ordering = ('-created_at',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'bird', 'quantity', 'added_at')
    list_filter = ('user',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'bird', 'added_at')
    list_filter = ('user',)