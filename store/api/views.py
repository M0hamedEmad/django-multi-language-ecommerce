from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import CartSerializer
from store.models import Cart, Size
from django.utils.translation import gettext_lazy as _

def check_if_cart_exist(user, product_id):
    cart = Cart.objects.filter( product__id=product_id, user=user )
    return cart
    

@api_view(['POST'])
def create_cart(request):
    size_id = request.data.get('sizeSelectId')
    product_id = request.data.get('product')
    
    serializer = CartSerializer( data=request.data )
    if serializer.is_valid():
        cart = check_if_cart_exist( request.user, product_id )
        if cart:
            cart.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        size = None
        if size_id:
            size = Size.objects.filter(id=size_id).first()
        if not size:
            size = Size.objects.filter(product__id=product_id, available_qunatity__gt=0).first() or None
        
        serializer.save(user=request.user, size=size)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def check_if_quantity_available(cart, quantity):
    size = cart.size
    if size:
        return (True, 1) if size.available_qunatity >= quantity else (False, size.available_qunatity)
    else:
        return (True, 1) if cart.product.get_availalbe_quantity >= quantity else (False, cart.product.get_availalbe_quantity)


@api_view(['POST'])
def edit_cart(request):
    action = request.data.get('action')
    product_id = request.data.get('product')
    instance = request.data.get('instance')
    
    cart_obj = Cart.objects.filter(id=instance).first()
    
    serializer = CartSerializer(instance=cart_obj, data=request.data )
    if serializer.is_valid():
        cart = check_if_cart_exist( request.user, product_id )
        if cart:
            if action == 'plus':
                quantity = cart_obj.quantity + 1
            else:
                quantity = cart_obj.quantity - 1
                if quantity <=0:
                    cart_obj.delete()
                    return Response({'msg': 'delete', 'data':serializer.data}, status=status.HTTP_200_OK)
                
            is_avilalbe = check_if_quantity_available(cart_obj, quantity)
            if not is_avilalbe[0]:
                serializer.save(instance=cart_obj, quantity=is_avilalbe[1])
                return Response(
                    {
                    'msg': 'quantityNotAvailalbe', 
                    'msgContent': _(f'The required quantity is not available. The largest number of this product is { is_avilalbe[1]}'),
                    'quatity': is_avilalbe[1],
                    'data':serializer.data},
                    status=status.HTTP_400_BAD_REQUEST)
            serializer.save(instance=cart_obj, quantity=quantity)
            return Response({'msg': 'edit', 'data':serializer.data}, status=status.HTTP_200_OK)
        return Response({
            'msg': 'not found',
            'msgContent': _('something error happened may be cart is not found'),
            'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    