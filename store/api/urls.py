from django.urls import path, include
from .views import create_cart,edit_cart

urlpatterns = [
    path('create_cart/', create_cart, name='create_cart'),
    path('edit_cart/', edit_cart, name='edit_cart'),
]
