from django.contrib import admin
from .models import categories
from .models import customer
from .models import Product
from .models import Order, Cart
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Checkout,CheckoutItem



# Register your models here.
admin.site.register(categories)
admin.site.register(customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Checkout)
admin.site.register(CheckoutItem)

class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class loginAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email', 'is_staff')


class signupAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email', 'is_staff')
    
    
class customerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'password')


