"""deliver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from customer.views import  Index,  LoginView, LogoutPage, SignupView, Order, OrderConfirmation, OrderPayConfirmation, Menu, MenuSearch, personal_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('', LoginView.as_view(), name='new_login'),
    path('new_signups/', SignupView.as_view(), name='new_signups'),
    path('logout/', LogoutPage.as_view(), name='logout'),
    
    path('index', Index.as_view(), name='index'),
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search/', MenuSearch.as_view(), name='menu-search'), 
    path('order/', Order.as_view(), name='order'),
    path('personal_details/', personal_order.as_view(), name='personal_details'),
    path('order-confirmation/<int:pk>', OrderConfirmation.as_view(),
         name='order-confirmation'),
    path('payment-confirmation/', OrderPayConfirmation.as_view(),
         name='payment-confirmation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
