from PIL import Image, ImageDraw
from io import BytesIO
from django.conf import settings
import string, random
from django.core.files.base import ContentFile
import string, random
import base64

from django.core.files.base import ContentFile

def decode_image(base64_image):
    format, imgstr = base64_image.split(';base64,')
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    return data

def pillow_update_avatar(pil_obj, user_obj, format='png'):
    try:
        from StringIO import StringIO
    except ImportError:
        from io import BytesIO
    new_avatar = BytesIO()
    try:
        #update_avatar
        pil_obj.save(new_avatar, format=format)
        s = new_avatar.getvalue()
        user_obj.picture.save(user_obj.picture,
                              ContentFile(s))
        user_obj.save()
    except TypeError:
        # if user_obj has no avatar
        user_obj.picture.save(f'{str(user_obj.id)}.{format}', ContentFile(s))
    finally:
        new_avatar.close()

def update_avatar(base64_image, user_obj, format='png'):
    avatar = decode_image(base64_image)
    try:
        #update avatar
        user_obj.profile.avatar.save(user_obj.profile.avatar, avatar)
        user_obj.save()
    except TypeError:
        # if user_obj has no avatar
        user_obj.profile.avatar.save(f'{str(user_obj.id)}.{format}', avatar)