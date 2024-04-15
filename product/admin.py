from django.contrib import admin
from .models import Collection, Cateogry, Product, Size, ProductContentMultiLanguage


class SizeInline(admin.TabularInline):
    model = Size


class ProductContentMultiLanguageInline(admin.TabularInline):
    model = ProductContentMultiLanguage
    fieldsets = (
        ('content', {
            "fields": (
                'title','summary'
            ),
        }),        (None, {
            "fields": (
                'color','tags', 'language'
            ),
        }),
    )
    


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = [
        'created_at',
        'updated_at',
        'slug'        
    ]
    list_display = [
        'title',
        'slug',
        'tags',
        'price',
        'is_available',
    ]
    fields = [
        'title',
        'summary',
        'price',
        'color',
        'cateogry',
        'image',
        'tags',
        'is_available',
        'sell_counter',
        'created_at',
        'updated_at',
        'slug',
    ]
    search_fields = [
        'title',
        'summary',
        'cateogry',
        'tags',
        'slug'
    ]
    list_filter = [
        'cateogry',
        'is_available',
    ]
    inlines = [
        ProductContentMultiLanguageInline,
        SizeInline,
    ]
    
    
class CollectionAdmin(admin.ModelAdmin):
    readonly_fields = (
            'slug',
    )
    list_display = [
        'name',
        'slug',
    ]
    fields = [
        'name',
        'arabic_name',
        'image',
        'slug',
    ]
    search_fields = [
        'name',
    ]
    
    
class CateoryAdmin(admin.ModelAdmin):
    readonly_fields = (
            'slug',
    )
    list_display = [
        'name',
        'slug',
        'collection'
    ]
    fields = [
        'name',
        'arabic_name',
        'image',
        'slug',
        'collection',
    ]
    search_fields = [
        'name',
        'slug',
        'collection'
    ]    
    
    
admin.site.register( Product, ProductAdmin )    
admin.site.register( Collection, CollectionAdmin )
admin.site.register( Cateogry, CateoryAdmin )