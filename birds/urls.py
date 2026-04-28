from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.bird_listings, name='bird_listings'),
    path('<int:bird_id>/', views.bird_detail, name='bird_detail'),

   
    path('add/', views.add_bird, name='add_bird'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('<int:bird_id>/edit/', views.edit_bird, name='edit_bird'),
    path('<int:bird_id>/delete/', views.delete_bird, name='delete_bird'),

    path('add-to-cart/<int:bird_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    
    path('add-to-wishlist/<int:bird_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    
    path('buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('vet/dashboard/', views.vet_dashboard, name='vet_dashboard'),
]