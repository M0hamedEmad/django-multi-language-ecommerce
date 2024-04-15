from django.contrib import admin
from .models import Cart, Shippers, WebSiteConfig, WebSiteConfigMultiLanguage, Contact


class WebSiteConfigMultiLanguageAdmin(admin.TabularInline):
    model = WebSiteConfigMultiLanguage


class WebSiteConfigAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    fields = ['website_title', 'description', 'created_at', 'updated_at', 'website_icon']
    list_display = ['website_title']
    inlines = [WebSiteConfigMultiLanguageAdmin]
    
    
    
class ShippersAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    fields = ('name', 'phone', 'created_at')
    list_display = ('name', 'phone', 'created_at')
    search_fields = ('name', 'phone')    
    
    
class CartAdmin(admin.ModelAdmin):
    readonly_fields = (
        'created_at',
    )
    list_display = [
        'user',
        'product',
        'size',
        'quantity',
    ]
    fields = [
        'user',
        'product',
        'size',
        'created_at',
        'quantity',
    ]
    search_fields = [
        'product',
        'user',
    ]
    

class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    list_display = (
        "user",
        "name",
        'email',
        'msg',
        'created',
    )
    list_filter = [
        "name",
        'email',
        'msg',
        'created',
    ]
    search_fields = (
        "user__username",
        "msg",
        'email'
    )


admin.site.register(Cart,CartAdmin)
admin.site.register(Shippers, ShippersAdmin)
admin.site.register(WebSiteConfig, WebSiteConfigAdmin)
admin.site.register(Contact, ContactAdmin)
