from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from modules.helpers import pillow_update_avatar
from PIL import Image

class Command(BaseCommand):
    help = 'Custom superuser creation'

    def handle(self, *args, **options):
        try:
            user = User.objects.create_superuser(username='root',
                                     email='root@gmail.com',
                                     password='root',
                                    )
        except IntegrityError:
            user = User.objects.get(email='root@gmail.com')
            user.delete()
            user = User.objects.create_superuser(username='root',
                                                 email='root@gmail.com',
                                                 password='root',
                                                 )
        user.save(); user.refresh_from_db()
        pillow_update_avatar(Image.open("media/profile/default.png"), user)
        print('Superuser [root@gmail.com:root] created.')
