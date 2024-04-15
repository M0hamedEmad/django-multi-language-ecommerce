from django.utils.text import slugify
from unidecode import unidecode

def create_slug(model, name):
    """ create unique slug from name"""

    slug = slugify(unidecode(name))
    filterd = model.objects.filter(slug = slug)
    if filterd.exists():
        filterd_len = len(filterd)
        while True:
            slug = slugify(unidecode(f"{name}-{ filterd_len }"))
            if model.objects.filter(slug = slug).exists(): filterd_len+=1
            else: break        
    return slug