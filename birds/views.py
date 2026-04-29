from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bird, CartItem, Wishlist
from .forms import BirdForm
from django.db import models


def bird_listings(request):
    # Show ALL birds, ignore filters for now
    birds = Bird.objects.all()
    
    print("DEBUG: Total birds loaded =", birds.count())
    
    context = {
        'for_sale': birds,
        'rehoming': birds,
        'adoption': birds,
        'food': birds,
    }
    
    return render(request, 'birds/listings.html', context)

def bird_detail(request, bird_id):
    bird = get_object_or_404(Bird, id=bird_id, is_available=True)
    return render(request, 'birds/bird_detail.html', {'bird': bird})


@login_required
def add_bird(request):
    if request.user.role != 'seller':
        messages.error(request, "Only sellers can add birds.")
        return redirect('home')
    
    if request.method == 'POST':
        form = BirdForm(request.POST, request.FILES)
        if form.is_valid():
            bird = form.save(commit=False)
            bird.seller = request.user
            bird.save()
            messages.success(request, "Bird listed successfully!")
            return redirect('seller_dashboard')
    else:
        form = BirdForm()
    return render(request, 'birds/add_bird.html', {'form': form})

@login_required
def seller_dashboard(request):
    if request.user.role != 'seller':
        messages.error(request, "Access denied.")
        return redirect('home')
    
    birds = Bird.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'seller/dashboard.html', {
        'birds': birds,
        'total_birds': birds.count(),
        'total_sales': birds.filter(is_available=False).count(),
        'total_items_sold': birds.filter(is_available=False).aggregate(total=models.Sum('quantity'))['total'] or 0
    })

@login_required
def edit_bird(request, bird_id):
    bird = get_object_or_404(Bird, id=bird_id, seller=request.user)
    if request.method == 'POST':
        form = BirdForm(request.POST, request.FILES, instance=bird)
        if form.is_valid():
            form.save()
            messages.success(request, "Bird updated successfully!")
            return redirect('seller_dashboard')
    else:
        form = BirdForm(instance=bird)
    return render(request, 'birds/edit_bird.html', {'form': form, 'bird': bird})

@login_required
def delete_bird(request, bird_id):
    bird = get_object_or_404(Bird, id=bird_id, seller=request.user)
    if request.method == 'POST':
        bird.delete()
        messages.success(request, "Bird deleted successfully!")
        return redirect('seller_dashboard')
    return render(request, 'birds/confirm_delete.html', {'bird': bird})


@login_required
def add_to_cart(request, bird_id):
    bird = get_object_or_404(Bird, id=bird_id, is_available=True)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, bird=bird)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{bird.title} added to your cart!")
    return redirect('bird_listings')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.bird.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_view')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.bird.price * item.quantity for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})


@login_required
def add_to_wishlist(request, bird_id):
    bird = get_object_or_404(Bird, id=bird_id, is_available=True)
    Wishlist.objects.get_or_create(user=request.user, bird=bird)
    messages.success(request, f"{bird.title} added to wishlist!")
    return redirect('bird_listings')


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('bird')
    return render(request, 'buyer/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Removed from wishlist.")
    return redirect('wishlist_view')



@login_required
def buyer_dashboard(request):
    if request.user.role != 'buyer':
        messages.error(request, "This page is for buyers only.")
        return redirect('home')
    
    cart_items = CartItem.objects.filter(user=request.user).select_related('bird')
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('bird')
    
    total_cart = sum(item.bird.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'wishlist_items': wishlist_items,
        'total_cart': total_cart,
    }
    return render(request, 'buyer/dashboard.html', context)
@login_required
def vet_dashboard(request):
    if request.user.role != 'vet':
        messages.error(request, "Access denied.")
        return redirect('home')
    
    return render(request, 'vet/dashboard.html', {})
def search(request):
    query = request.GET.get('q', '').strip()
    results = Bird.objects.none()
    
    if query:
        results = Bird.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(breed__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(location__icontains=query)
        ).filter(is_available=True)[:20]
    
    return render(request, 'search_results.html', {
        'query': query,
        'results': results
    })