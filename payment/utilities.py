from .models import OrderItem
from store.models import Cart, Shippers 

def from_cart_to_order_item(carts, order):
    """move product from cart to product items and delete the cart"""
    for cart in carts:
        cart_item = Cart.objects.get(id=cart)
        order_item = OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            size=cart_item.size,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        order_item.save()
        
        if order_item.size:
            size = order_item.size
            size.available_qunatity -= cart_item.quantity
            size.save()
        
        cart_item.delete()
    return order


def calc_carts_cost(carts):
    """Calc All Cart Cost From List"""
    total = 0
    for cart in carts:
        cart_item = Cart.objects.get(id=cart)
        total += (cart_item.quantity * cart_item.product.price)
    return total
       


def get_shipper():
    ## TODO Handle Shipper - return shipper depending on the place
    
    try: return Shippers.objects.get()
    except: return None
    
