from django.contrib import admin
from .models import Order, OrderItem, PaymentData


class PaymentDataAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    fields = ('payment_type', 'total', 'transaction_id', 'status', 'created', 'updated')
    list_display = ('payment_type', 'total', 'status', 'created', 'updated')
    search_fields = ('payment_type', 'transaction_id')
    list_filter = ('status',)



class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'get_total_cost')
    fieldsets = (
        ('customer', {
            'fields': (
                'customer',
                'customer_first_name',
                'customer_last_name',
                'customer_phone',
                'adress_line',
                'city',
                'state',
                'zip_code',
            ),
        }), ('shipping',  {
            'fields': ('shipping', 'shipping_cost', 'status')
        }), ('payment', {
            'fields': ('paid', 'get_total_cost', 'payment_data')
        })
    )

    list_display = ('id', 'customer', 'customer_first_name', 'state', 'shipping','shipping_cost', 'status', 'paid', 'created_at')
    search_fields = ('customer', 'customer_first_name', 'customer_last_name', 'customer_phone', 'adress_line', 'city','state', 'zip_code')
    list_filter = ('status',)
    
    
class OrderItemAdmin(admin.ModelAdmin):
    fields = ('order', 'product', 'quantity', 'price', 'size')
    list_display = ('id', 'product', 'quantity', 'order')
    search_fields = ('id', 'product', 'order')


admin.site.register(Order, OrderAdmin)
admin.site.register(PaymentData, PaymentDataAdmin)
admin.site.register(OrderItem, OrderItemAdmin)