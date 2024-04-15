from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from product.views import CollectionListView

urlpatterns = [
]

urlpatterns+=i18n_patterns(
    path('admin/', admin.site.urls),
    
    path('account/', include('users.urls'), name='users'),
    path('', include('product.urls')),
    path('', include('store.urls')),
    path('', include('payment.urls')),
    
    
    path('',  CollectionListView.as_view(), name='home'),
)

if settings.DEBUG == True:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)    
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('translation/', include('rosetta.urls'))
    ]