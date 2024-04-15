from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Cateogry, Collection, Product
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
import json
from store.utilities import get_wish_list_from_cookies

class CollectionListView(ListView):
    template_name = 'product/collection.html'
    model = Collection
    context_object_name = 'collection_list'    
    

    
class ProductListView(View):
    def get(self, request, *args, **kwargs):
        ## GET CATEGORY
        collection_slug = self.kwargs['slug']
        collection = get_object_or_404(Collection, slug=collection_slug)
        categories = Cateogry.objects.filter(collection=collection)
        
        category_filter = categories.filter(slug=request.GET.get('category'))
        if category_filter:
            products_list = Product.objects.filter(is_available=True, cateogry=category_filter.first())
        else:
            products_list = Product.objects.filter(is_available=True, cateogry__in=categories)
            
        order = request.GET.get('order')
        if order == 'best_selling':
            products_list = products_list.order_by('-sell_counter')  
        elif order == 'a-z':
            print(order)
            products_list = products_list.order_by('title')  
        elif order == 'z-a':
            products_list = products_list.order_by('-title')  
        elif order == 'low_to_high':
            products_list = products_list.order_by('price')  
        elif order == 'high_to_low':
            products_list = products_list.order_by('-price')   
        elif order == 'old_to_new':
            products_list = products_list.order_by('created_at')  
        elif order == 'new_to_old':
            products_list = products_list.order_by('-created_at')                                                  
            
            
        page = request.GET.get('page') or 1
        paginator = Paginator(products_list, 25)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page( paginator.num_pages )
        
        wish_list = self.request.COOKIES.get('wish_list') or '{}'
        w_list = json.loads(wish_list) or []
        
        context = {
            'products': products,
            'categories':categories,
            'collection':collection,
            'wish_list' : w_list
        }
        return  render(request, 'product/products.html', context)


class ProductDetialView(DetailView):
    template_name = 'product/product_detail.html'
    queryset = Product.objects.filter(is_available=True)
    context_object_name = 'product'
    
    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        more_product = Product.objects.filter(
            cateogry = self.get_object().cateogry,
            is_available=True
        )
        if len(more_product) < 5:
            more_product |= Product.objects.filter(is_available=True,).order_by('-created_at')[:5-len(more_product)]
        context['more_product'] = more_product
        
        w_list = get_wish_list_from_cookies(self.request)
        context['is_wishlist'] = self.get_object().slug in ( w_list )
        
        return context
    
    
class ProductSearchView(View):
    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        wish_list = get_wish_list_from_cookies(request)
        
        products = Product.objects.all()
        if search:
            if search == 'wishlist':
                products = products.filter(slug__in=wish_list)
            else: 
                products = products.filter(
                    Q(title__icontains=search)|
                    Q(tags__icontains=search)|
                    Q(color__icontains=search)|
                    Q(product_content__title__icontains=search)|
                    Q(product_content__tags__icontains=search)
                )
                
        order = request.GET.get('order')
        if order == 'best_selling':
            products = products.order_by('-sell_counter')  
        elif order == 'a-z':
            print(order)
            products = products.order_by('title')  
        elif order == 'z-a':
            products = products.order_by('-title')  
        elif order == 'low_to_high':
            products = products.order_by('price')  
        elif order == 'high_to_low':
            products = products.order_by('-price')   
        elif order == 'old_to_new':
            products = products.order_by('created_at')  
        elif order == 'new_to_old':
            products = products.order_by('-created_at')              
            
        paginator = Paginator(products, 25)
        page = request.GET.get('page') or 1
        try:
            products = paginator.page( page )
        except PageNotAnInteger:
            products = paginator.page( 1 )
        except EmptyPage:
            products = paginator.page( paginator.num_pages )
        
        context = {
            'products':products,
            'wish_list' : wish_list
            }
        return render(request, 'product/products.html',  context)
