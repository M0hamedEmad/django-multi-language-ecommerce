from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from product.models import Product, Size
from store.models import Shippers

User = get_user_model()
    
class PaymentData(models.Model):
    status_choices = [
        ('done', 'done'),
        ('canceld', 'canceld'),
        ('waited', 'waited'),
        ('error', 'error'),
    ]    
    payment_type = models.CharField(_('payment type'), max_length=255, null=True, blank=True)
    total = models.DecimalField(_('total'), max_digits=10, decimal_places=2, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=40, null=True, blank=True, choices=status_choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{str(self.payment_type)} => {str(self.status)}"    
    


class Order(models.Model):
    status_choices = (
        ('processing', _('processing')),
        ('in delivery', _('in delivery')),
        ('completed', _('completed')),
        ('cancelled', _('cancelled')),
    )
    
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)
    status = models.CharField(_('status'), max_length=255, null=True, blank=True, choices=status_choices)
    paid = models.BooleanField(_('paid'), default=False)
    shipping = models.ForeignKey(Shippers, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)
    shipping_cost = models.DecimalField(_('shipping cost'), max_digits=10, decimal_places=2)

    customer_first_name = models.CharField(_('customer name'), max_length=255, null=True, blank=True)
    customer_last_name = models.CharField(_('customer last name'), max_length=255, null=True, blank=True)
    customer_email = models.CharField(_('customer email'), max_length=255, null=True, blank=True)
    customer_phone = models.CharField(_('customer phone'), max_length=255, null=True, blank=True)
    adress_line = models.CharField(_('adress_line'), null=True, blank=True, max_length=255)
    city = models.CharField(_('city'), null=True, blank=True, max_length=255)
    state = models.CharField(_('state'), null=True, blank=True, max_length=255)
    zip_code = models.CharField(_('zip_code'), null=True, blank=True, max_length=155)
    payment_data = models.ForeignKey(PaymentData, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)

    created_at = models.DateTimeField( _("created at") ,auto_now_add=True)
    updated_at = models.DateTimeField( _("updated at") ,auto_now=True)

    @property
    def get_total_cost(self):
        order_items = self.order_items.all()
        total_cost = sum((order_item.product.price * order_item.quantity) for order_item in order_items.size.all())
        return total_cost + self.shipping_cost

    def __str__(self):
        return f"{self.id} - {self.customer} ({self.status})"
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='order_items', null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, related_name='order_items', null=True, blank=True)
    quantity = models.IntegerField(_('quantity'), default=1)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    
    def __str__(self):
        return f"{self.order} - {self.product}"
