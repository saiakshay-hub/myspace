"""
URL configuration for personal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myspace import views  
from django.conf import settings
from  myspace import views
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
admin.site.site_header="Myspace Food Store"

urlpatterns = [
    path('admin/', admin.site.urls),
   path('',views.myspace, name='myspace'),
   path('signup/',views.signup, name='signup'),
   path('login/',views.login_view, name='login'),
   path('search/',views.search, name='search_products'),   
   path('',views.base,name='home'),
   path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
   path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
     path('biryani_items/', views.biryani_items, name='biryani_items'),
    path('burger/', views.burger, name='burger'),
    path('dose/', views.dose, name='dosa'),
     path('pizza/', views.pizza, name='pizza'),
     path('salad/', views.salad, name='salad'),
     path('shake/', views.shake, name='shake'),
     path('south/', views.south, name='south'),
     path('ice/', views.ice, name='ice'),
     path('about/',views.about,name='about'),
     path('checkout/', views.checkout_view, name='checkout'),
     path('success/', views.payment_success_view, name='success'),
     path('my-orders/', views.my_orders_view, name='my-orders'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)