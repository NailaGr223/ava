from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bird, CartItem
from .forms import BirdForm

# ===================== PUBLIC VIEWS =====================
def bird_listings(request):
    birds = Bird.objects.filter(is_available=True).order_by('-created_at')
    return render(request, 'birds/listings.html', {'birds': birds})

def bird_detail(request, bird_id):
    bird = get_object_or_404(Bird, id=bird_id, is_available=True)
    return render(request, 'birds/bird_detail.html', {'bird': bird})

# ===================== SELLER CRUD =====================
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
        'total_birds': birds.count()
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

# ===================== CART =====================
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