from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.project.models import Project
from django.db.utils import IntegrityError
from modules.helpers import pillow_update_avatar
from PIL import Image
import string
import random


def rs(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class Command(BaseCommand):
    help = 'Custom superuser creation'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='root')
            for i in range(20):
                name = rs(15)
                pr = Project.objects.create(author=user,
                                            name=name,
                                            description=rs(150),

                                            )
                pr.save();
                pr.refresh_from_db()
                print(f'Project {name} created.')
        except IntegrityError:
            pass