import random
import string
from django.utils.text import slugify

def generate_slug(string):
    """ Takes in string, adds random ID (number) to it, and creates slug of the same """
    random_id_upper_limit = 99999 # 5-digit number (at most)
    random_id = str(random.randint(0, int(random_id_upper_limit)))
    if len(random_id) < len(str(random_id_upper_limit)):
        digit_diff = abs(len(str(random_id)) - len(str(random_id_upper_limit)))
        random_id = '0' * digit_diff + random_id
    string_with_id = str(string) + '-' + str(random_id)
    slugged_string = string_with_id.replace(' ', '-')
    return slugged_string


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
        slug = slugify(value=instance.title)
    
    Klass = instance.__class__
    queryset_exists = Klass.objects.filter(slug=slug).exists()
    if queryset_exists:
        randstr = random_string_generator(size=4)
        new_slug = f"{slug}-{randstr}"
        return unique_slug_generator(instance=instance, new_slug=new_slug)
    return slug