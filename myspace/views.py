from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Order,Checkout,CheckoutItem,Product
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



def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
        request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
        request.session['cart'] = cart
    return redirect('cart')

def cart_view(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    total = sum(p.price for p in products)
    return render(request, 'cart.html', {'products': products, 'total': total})

@login_required
@csrf_protect
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # we will Send to checkout via POST form
    if request.method == 'POST':
        return render(request, 'checkout.html', {'total': product.price})
    
    return render(request, 'buy.html', {'product': product})

def about(request): 
    return render(request, 'about.html')




@login_required
def checkout_view(request):
    if request.method == 'POST':
        total_str = request.POST.get('total')
        print ("received total:",total_str)
        try:
            total = float(total_str) 
        except (ValueError, TypeError):
            return HttpResponse("Invalid total amount", status=400)
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
 
