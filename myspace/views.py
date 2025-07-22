from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Order,Checkout,CheckoutItem,Product,customer
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def myspace(request):
    return render(request, 'myspace.html')


def search(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'search_results.html', {'products': products})





def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.info(request, 'Signup successful')
            if request.user.is_authenticated:
                return redirect('myspace.html')
            return redirect('login')
        except Exception as e:
            messages.info(request, f'Error during signup: {e}')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, 'Login successful')
            return redirect('myspace')
        else:
            messages.info(request, 'Invalid username or password')
    return render(request, 'login.html')

from django.views.decorators.csrf import csrf_protect
@csrf_protect
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, {"Logged out successfully"})
        return redirect('login')


def base(request):
    return render(request, 'base.html')


def biryani_items(request):
    Products = Product.objects.filter(catrgory__name='Biryani')
    return render(request, 'biryani_items.html', {'products': Products})  

def burger(request):
    Products = Product.objects.filter(catrgory__name='Burger')
    return render(request, 'burger.html', {'products': Products})

def dose(request):
    Products = Product.objects.filter(catrgory__name='dosa')
    return render(request, 'dose.html', {'products': Products})

def pizza(request):
    Products = Product.objects.filter(catrgory__name='Pizza')
    return render(request, 'pizza.html', {'products': Products})

def salad(request):
    Products = Product.objects.filter(catrgory__name='Salad')
    return render(request, 'salad.html', {'products': Products})

def shake(request):
    Products = Product.objects.filter(catrgory__name='Shake')
    return render(request, 'shake.html', {'products': Products})

def south(request):
    Products = Product.objects.filter(catrgory__name='South_Indian')
    return render(request, 'south.html', {'products': Products})

def ice(request):
    Products = Product.objects.filter(catrgory__name='Ice Cream')
    return render(request, 'ice.html', {'products': Products},)



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    Cart.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('cart')


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def about(request): 
    return render(request, 'about.html')




@login_required
def checkout_view(request):
    if request.method == 'POST':
        total_str = request.POST.get('total')
        try:
            total = float(total_str)
        except (ValueError, TypeError):
            return HttpResponse("Invalid total amount", status=400)

        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return HttpResponse("Your cart is empty", status=400)

        for item in cart_items:
            Order.objects.create(
                user=request.user,
                Product=item.product,
                quantity=item.quantity,
                price=item.product.price * item.quantity
            )

        # Clear cart after successful checkout
        cart_items.delete()

        return render(request, 'checkout.html', {'total': total})
    else:
        return redirect('cart')
    



@login_required
def payment_success_view(request):
    if request.method == 'POST':
        total = request.POST.get('total')
        payment_mode = request.POST.get('payment_mode')
        print ("Raw total from POST:",total)
        print ("payment mode",payment_mode)

        try:
            total_decimal = Decimal(total)
        except (InvalidOperation, TypeError):
            # Handle the error: you can redirect with a message or assign a fallback
            return HttpResponse("Invalid total amount", status=400)

        
        checkout = Checkout.objects.create(
            user=request.user,
            total_amount=total_decimal,
            payment_mode=payment_mode
        )

    
        cart = request.session.get('cart', [])
        for product_id in cart:
            product = Product.objects.get(id=product_id)
            CheckoutItem.objects.create(
                checkout=checkout,
                product=product,
                quantity=1  
            )

        request.session['cart'] = []

        return render(request, 'success.html', {
            'total': total_decimal,
            'payment_mode': payment_mode
        })

    return redirect('cart')





@login_required
def my_orders_view(request):
    orders = Checkout.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my-orders.html', {'orders': orders})
 
