from django.db import models
import datetime
from django.contrib.auth.models import User



class categories(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField (upload_to='category_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class customer(models.Model):
    name = models.CharField(max_length=50)
    phone =models.CharField(max_length=10)
    email =models.CharField(max_length=100)
    password =models.CharField(max_length=100)
    
    def __str__(self):
        return  self.name


class Product(models.Model):
    name =models.CharField(max_length=50)
    price =models.DecimalField(default=0, decimal_places=2,max_digits=7)
    catrgory =models.ForeignKey(categories, on_delete=models.CASCADE, default=1)
    resturant =models.ForeignKey(customer, on_delete=models.CASCADE, default=1)
    description =models.CharField(max_length=250,default='',blank=True, null= True)
    image =models.ImageField(upload_to='uploads/product/')
    def __str__(self):
        return self.name
    
class Order(models.Model):
<<<<<<< HEAD
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     Product = models.ForeignKey(Product, on_delete=models.CASCADE)
     price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
=======
     Product = models.ForeignKey(Product, on_delete=models.CASCADE)
>>>>>>> 242906dff4c207d97b7e3881b97ee299ca0aeb29
     customer = models.ForeignKey(customer, on_delete=models.CASCADE,null=True, blank=True)
     quantity =models.IntegerField(default=1)
     address =models.CharField(max_length=100,default='',blank=True)
     phone=models.CharField(max_length=20,default='',blank=True)
     date=models.DateField(default=datetime.datetime.today)
<<<<<<< HEAD
     status=models.BooleanField(default=False)
     def __str__(self):
               return f"{self.user.username} - {self.Product.name} - Qty: {self.quantity}"
=======
     
     status=models.BooleanField(default=False)
     def __str__(self):
        return self.product
>>>>>>> 242906dff4c207d97b7e3881b97ee299ca0aeb29
     
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"


<<<<<<< HEAD

=======
>>>>>>> 242906dff4c207d97b7e3881b97ee299ca0aeb29
class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.total_amount} "
    

class CheckoutItem(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

