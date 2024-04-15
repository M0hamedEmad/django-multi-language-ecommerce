from django.urls import path
from .views import CollectionListView,  ProductListView, ProductDetialView, ProductSearchView


urlpatterns = [
    path('collection/', CollectionListView.as_view(), name='collection'),
    path('collection/<str:slug>/', ProductListView.as_view(), name='collection_page'),
    # path('products/', ProductListView.as_view(), name='products'),
    path('product/<str:slug>/', ProductDetialView.as_view(), name='product'),
    path('product/', ProductSearchView.as_view(), name='product_search'),
    
]