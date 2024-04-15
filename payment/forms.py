from django import forms
from .models import Order, OrderItem, PaymentData


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_first_name',
                'customer_last_name', 
                'customer_phone', 
                'adress_line', 
                'city', 
                'state', 
                'zip_code',
                'customer_email'
                ]
        
