from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from .utilities import create_slug



class Collection(models.Model):
    name = models.CharField(_('name'), max_length=90)
    arabic_name = models.CharField(_('arabic name'), max_length=90, null=True, blank=True,)
    image = models.ImageField(_('Image'), null=True, blank=True, upload_to='images/collection_images')
    slug = models.SlugField(unique=True, blank=True)
    
    @property
    def get_name(self):
        if get_language() == 'ar' and self.arabic_name:
            return self.arabic_name
        return self.name
    
    @property
    def get_image_url(self):
        return self.image.url if self.image else None
            
        
    def save(self, *args, **kwargs) :
        if not self.slug:
            self.slug = create_slug(Collection, self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"    
    
    
class Cateogry(models.Model):
    name = models.CharField(_('name'), max_length=90)
    arabic_name = models.CharField(_('arabic name'), max_length=90, null=True, blank=True,)
    image = models.ImageField(_('image'), null=True, blank=True, upload_to='images/cateogry_images')
    slug = models.SlugField(unique=True, blank=True)
    collection = models.ForeignKey(Collection, null=True, blank=True, related_name='categories', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


    @property
    def get_name(self):
        if get_language() == 'ar' and self.arabic_name:
            return self.arabic_name
        return self.name
    
    @property
    def get_image_url(self):
        return self.image.url if self.image else None    

    def save(self, *args, **kwargs) :
        if not self.slug:
            self.slug = create_slug(Cateogry, self.name)
        return super().save(*args, **kwargs)        
    
    
    def __str__(self):
        return f"{self.name} - {self.collection.name}"    
    
    
class Product(models.Model):
    availabe_choices = [
        (True, 'avilable'),
        (False, 'not avilable'),
    ]
    
    title = models.CharField( _("title") ,max_length=90)
    color = models.CharField( _("color") ,max_length=90, null=True, blank=True)
    summary = models.TextField( _("summary") ,null=True, blank=True)
    image = models.ImageField( _("image") ,null=True, blank=True, upload_to='images/product_images')
    cateogry = models.ForeignKey(Cateogry, null=True, blank=True, related_name='products', on_delete=models.SET_NULL)
    tags = models.CharField( _("tags") ,max_length=255, null=True, blank=True, help_text="ex: clothes, shoes, ....")
    price = models.DecimalField( _("price") ,max_digits=9, decimal_places=2)
    is_available = models.BooleanField( _("is available") ,default=True, choices=availabe_choices)
    created_at = models.DateTimeField( _("created at") ,auto_now_add=True)
    updated_at = models.DateTimeField( _("updated at") ,auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    sell_counter = models.IntegerField(default=0)


    class Meta:
        ordering = ('-created_at', )            
            
            
    @property
    def get_size(self):
        return Size.objects.filter(product=self.id)
            
    @property
    def get_product_with_active_language(self):
        product_content = self.product_content.filter(language=get_language())
        if product_content and product_content.first().language == get_language(): return product_content.first()
        return self
    
    @property
    def get_title(self):
        return self.get_product_with_active_language.title or self.title
    
    
    @property
    def get_summary(self):
        return self.get_product_with_active_language.summary or self.summary
    
    @property
    def get_tags(self):
        return self.get_product_with_active_language.tags or self.tags    
    
    
    @property
    def get_color(self):
        return self.get_product_with_active_language.color or self.color    
        
    @property
    def get_image_url(self):
        return self.image.url if self.image else None 
    
    @property
    def get_availalbe_quantity(self):
        return sum(size.available_qunatity for size in self.size.all())
    
    
    def save(self, *args, **kwargs) :
        if not self.slug:
            self.slug = create_slug(Product, self.title)
        return super().save(*args, **kwargs)        
    
    def __str__(self):
        return f"{self.title}"
    
    
    
class ProductContentMultiLanguage(models.Model):
    availabe_choices = [
        ('ar', 'Arabic'),
    ]
    title = models.CharField(_('title') ,max_length=90)
    summary = models.TextField(_('summary') ,null=True, blank=True)
    color = models.CharField(_('color') ,null=True, blank=True, max_length=200)
    tags = models.CharField(_('tags') ,max_length=255, null=True, blank=True, help_text="مثال: ملابس, ملابس شتاء, .......")
    product = models.ForeignKey(Product, related_name='product_content', on_delete=models.CASCADE)
    language =  models.CharField(_('language') ,null=True, blank=True, choices=availabe_choices, max_length=200)

    
    
class Size(models.Model):
    size = models.CharField(_('size') ,max_length=20)
    available_qunatity = models.IntegerField(_('available qunatity'), default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='size')
    
    def __str__(self):
        return f"{self.size} - {self.product}"
        