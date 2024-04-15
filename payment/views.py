from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from store.utilities import return_cart_product
from .forms import OrderForm
from django.contrib import messages
from django.utils.translation import gettext as _
from .utilities import get_shipper, from_cart_to_order_item, calc_carts_cost
from django.conf import settings
from .models import PaymentData
from django.contrib.auth.mixins import LoginRequiredMixin


import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckOutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        carts = return_cart_product(self.request, slug_only=False).get('cart_product_list')
        
        carts = [cart for cart in carts if cart.is_quantity_available]
        context = {
            'carts':carts,
            'form':OrderForm,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        }
        return render(request, 'payment/checkout.html', context)
    
    def post(self, request, *args, **kwargs):
        payment_method = request.POST.get('pay_method')
        carts = request.POST.getlist('carts')
        payment_method_id=request.POST['payment_method_id']
        shipping_cost = 0 ## TODO Handle shipping cost
        
        if len(carts) == 0:
            messages.error(request, _('Please add product to cart'))
            return redirect(reverse_lazy('checkout'))        
        
        form = OrderForm(request.POST)
        
        if form.is_valid():
            order_form = form.save(commit=False)
            order_form.shipping_cost = shipping_cost 
            order_form.status = 'in delivery'
            order_form.customer = request.user or None
            order_form.shipper = get_shipper()
        else:
            messages.error(request, _('An error occurred while trying to register the request. Try again or contact support'))
            return redirect(reverse_lazy('checkout'))

        if payment_method != 'cash':
            try:
                amount = calc_carts_cost(carts) + shipping_cost
                intent = stripe.PaymentIntent.create(
                    amount=int(amount*100),  # amount in cents
                    currency='usd',
                    payment_method=payment_method_id,
                    automatic_payment_methods={"enabled": True, 'allow_redirects': 'never'},
                    confirm=True,
                    description=f"Payment process for user No. {request.user}"
                )
                pay_data = PaymentData.objects.create(payment_type = 'visa',
                                            total = calc_carts_cost(carts) + shipping_cost,
                                            transaction_id = intent.id,
                                            status='done')
                order_form.paid = True
                order_form.payment_data = pay_data
                
            except stripe.error.CardError as e:
                messages.error(request, _('Error during payment process. Try again or contact support'))
                return redirect(reverse_lazy('checkout'))
        
        order_form.save()
        from_cart_to_order_item(carts, order_form)

        messages.success(request, _('The order has been added and will reach you within a few days'))
        return redirect(reverse_lazy('home'))





