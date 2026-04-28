from django.contrib import admin
from .models import Bird, CartItem, Wishlist

admin.site.register(Bird)
admin.site.register(CartItem)
admin.site.register(Wishlist)