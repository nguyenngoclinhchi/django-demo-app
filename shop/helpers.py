import random
import string
import uuid
import os
import re
import locale

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('shop/images/product/', filename)

def get_skip_path_slug_article(path): 
    last_path = path.split('/')[-1]
    skip_slug = None
    match = re.search(r'^(?P<product_slug>[\w-]+)-a\d+\.html$', last_path)
    if match: 
        skip_slug = match.group('product_slug')
    return skip_slug

def get_currency_vn(number): 
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    formatted_number = locale.format_string("%d", number, grouping=True) + " VND"
    return formatted_number

def chunked(items, num_per_group=3):
    return [items[i:i+num_per_group] for i in range(0, len(items), num_per_group)]

def generate_order_code(length):
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))