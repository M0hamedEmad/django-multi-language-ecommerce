import json
from .models import Cart, WebSiteConfig
from product.models import Product, Collection

def get_wish_list_from_cookies(request):
    wish_list = request.COOKIES.get('wish_list') or '{}'
    return json.loads(wish_list) or []
    

def wishlist_counter(request):
    wish_list = get_wish_list_from_cookies(request)
    return {'wishlist_counter': len(wish_list)}


def get_cart_products_from_cookies(request):
    cart_products = request.COOKIES.get('cartProduct') or '{}'
    return json.loads(cart_products) or []


def get_cart_querset_from_cookies(request):
    cart_products = json.loads(request.COOKIES.get('cartProduct'))
    cart_products = Product.objects.filter(slug__in=cart_products)
    return cart_products

def return_cart_product(request, slug_only=True):
    """return all carts in database of from cookies"""
    if not request.user.is_authenticated:
        if not slug_only:
            cart_product_list = get_cart_querset_from_cookies(request)
        else:
            cart_product_list = get_cart_products_from_cookies(request)
    else:
        cart_product_list = Cart.objects.filter(user=request.user)
        if  slug_only:
            cart_product_list = cart_product_list.values_list('product__slug', flat=True)
            
    return {'cart_product_list': cart_product_list}


def get_website_config(request):
    website_config =  WebSiteConfig.objects.first()
    if website_config:
        return {
            'website_title': website_config.get_website_title,
            'website_description': website_config.get_description,
            'website_icon': website_config.get_icon_url,
        }
    return {'website_title':'ecommerce','website_description':'','website_icon':'',}        


def get_collection(request):
    collection = Collection.objects.all()[:10]
    return {'collection_list': collection}