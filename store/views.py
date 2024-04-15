from .models import Cart, Contact
from django.contrib import messages
from django.shortcuts import redirect, render
from product.models import Product, Cateogry
from django.views.generic import ListView, View
from .utilities import get_wish_list_from_cookies, return_cart_product
from django.utils.translation import gettext_lazy as _
class HomeView(ListView):
    template_name = 'store/home.html'
    model = Product
    queryset = Product.objects.filter()[:25]
    context_object_name = 'products'
    
    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Cateogry.objects.all()[:10]
        context['wish_list'] = get_wish_list_from_cookies(self.request)
        return context
    
    
class CartListView(ListView):
    template_name = 'store/carts.html'
    model = Cart
    context_object_name = 'carts'
    
    def get_queryset(self):
        return return_cart_product(self.request, slug_only=False).get('cart_product_list')
    
    
class ContactView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'store/contact.html')    
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('msg')

        if not msg:
            return redirect('home')

        if request.user.is_authenticated:
            Contact.objects.create(
                user=request.user,
                name=name,
                email=email,
                msg=msg
            )
        else:
            Contact.objects.create(
                name=name,
                email=email,
                msg=msg
            )            
        messages.success(request, _("Your message has been sent successfully"))
        return redirect('home')    
    
