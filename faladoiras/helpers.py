
#ESte código copieino desta páxina (https://www.codingforentrepreneurs.com/blog/a-unique-slug-generator-for-django/) e básicamente o que fai é meter como slug
# o nome do artículo separandoo con guión medio. E se o nomeestá duplicado pois genera outro distinto para que o slug sexa único. 

'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''
import random
import string
from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.faladoiras_persoa)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug