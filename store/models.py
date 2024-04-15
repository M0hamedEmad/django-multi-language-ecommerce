from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product, Size
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

User = get_user_model()

class WebSiteConfig(models.Model):
    website_title = models.CharField(_("website_title"), max_length=255, null=True, blank=True)
    description = models.TextField(_("description"), null=True, blank=True)
    website_icon = models.ImageField(_("website icon"), upload_to='images/store', null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    
    @property
    def get_website_title(self):
        lang = get_language()
        if lang != 'en':
            obj = WebSiteConfigMultiLanguage.objects.filter(language=lang).first()
            if obj: return obj.website_title
        return self.website_title
    
    @property
    def get_description(self):
        lang = get_language()
        if lang != 'en':
            obj = WebSiteConfigMultiLanguage.objects.filter(language=lang).first()
            if obj: return obj.description
        return self.description    
    
    @property
    def get_icon_url(self):
        return self.website_icon.url if self.website_icon else None 
    
    def __str__(self):
        return self.website_title
    
    
class WebSiteConfigMultiLanguage(models.Model):
    website_title = models.CharField(_("website_title"), max_length=255)
    description = models.TextField(_("description"), null=True, blank=True)
    language = models.CharField(_("language"), max_length=255)
    main_conig = models.ForeignKey(WebSiteConfig, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.website_title    


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(_("created at") ,auto_now_add=True)
    quantity = models.IntegerField(_('quantity'), default=1)
    
    
    @property
    def is_quantity_available(self):
        if self.size is not None:
            return self.size.available_qunatity >= self.quantity
        return self.product.get_availalbe_quantity >= self.quantity
    
    def __str__(self):
        return f"{self.user.username} cart"


    
class Shippers(models.Model):
    name = models.CharField(_('name'), max_length=255, null=True, blank=True)
    phone = models.CharField(_('phone'), max_length=20, null=True, blank=True)
    created_at = models.DateTimeField( _("created at") ,auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"
    
    

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    msg = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user)} => {str(self.msg)}"    