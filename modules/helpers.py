from PIL import Image, ImageDraw
from io import BytesIO
from django.conf import settings
import string, random
from django.core.files.base import ContentFile
from modules.avatars import Identicon
import string, random

def avatar_generator(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def update_avatar(pil_obj, user_obj):
    try:
        from StringIO import StringIO
    except ImportError:
        from io import BytesIO
    new_avatar = BytesIO()
    try:
        pil_obj.save(new_avatar, format='png')
        s = new_avatar.getvalue()
        user_obj.picture.save(user_obj.picture,
                              ContentFile(s))
        user_obj.save()
    except TypeError:
        # if user_obj has no avatar
        user_obj.picture.save(f'{str(user_obj.id)}_av.png', ContentFile(s))
    finally:
        new_avatar.close()

def gen_avatar():
    hash = avatar_generator()
    return Identicon(hash).generate()