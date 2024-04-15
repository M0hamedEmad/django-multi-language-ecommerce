from django.urls import path, include
from .views import HomeView, CartListView, ContactView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('carts/', CartListView.as_view(), name='cart'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('api', include('store.api.urls'))
    
]
