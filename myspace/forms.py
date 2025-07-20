from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Product

# Sign Up Form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

# Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

# Search Form
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search...'}))
#
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Product Description'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Product Price'}),
            'image': forms.ClearableFileInput(attrs={'placeholder': 'Product Image'}),
        }
