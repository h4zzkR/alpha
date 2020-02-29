import pytz
import datetime
from django.db import models
from django.contrib.auth.models import User
from apps.project.models import Project
from django.core.cache import cache
import os
from django.core.mail import EmailMultiAlternatives

from django.conf import settings

from django.dispatch import receiver

from django.db.models.signals import post_save
from taggit.managers import TaggableManager

import hashlib
from modules.helpers import random_string


class UserPasswordRecovery(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    key1 = models.TextField(max_length=64)
    expires = models.DateTimeField(default=datetime.datetime.now(
        pytz.utc) + datetime.timedelta(hours=24))


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # user.profile.fields

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    last_seen = models.DateTimeField(auto_now_add=True, blank=True)
    avatar = models.ImageField(upload_to="profile/photos/", blank=True)
    confirmed = models.BooleanField(default=False) # is account confirmed by email
    rating = models.IntegerField(default=0)
    active_projects_cnt = models.IntegerField(default=0)

    good_teamlead = models.IntegerField(default=0) # users sets this user as a good teamlead
    # phone = models.TextField(default="")
    status = models.TextField(default="")

    # trello = models.TextField(default="")
    vk = models.URLField(default="", max_length=len('https://vk.com/') + 20, blank=True)
    linked_in = models.URLField(default="", max_length=len('https://') + 20, blank=True)
    telegram = models.URLField(default="",  max_length=len('https://t.me/') + 20, blank=True)
    bio = models.TextField(default="", max_length=3000)
    location = models.CharField(default="", max_length=80)

    github_account = models.CharField(default="", max_length=100)
    github_projects_cnt = models.IntegerField(default=0)
    github = models.URLField(default="", max_length=len('https://') + 30, blank=True)
    github_id = models.IntegerField(blank=True, unique=True, null=True)
    github_followers = models.IntegerField(default=0)
    github_access_token = models.CharField(blank=True, null=True, max_length=40)
    github_commits = models.IntegerField(default=0)
    github_stars = models.IntegerField(default=0)

    skills = TaggableManager()

    def __str__(self):
        return self.user.username

    def link(self):
        return 'http://217.182.75.251/u/' + self.user.username

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def list_skills(self):
        return ','.join([t.name for t in self.skills.all()])

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                    seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return 'media/profile/photos/default.png'

    def email_user(self, subject, arguments, text_content=None, message=None):
        # arguments = { KEY : VALUE } for template
        # {{ link }}
        template_name = os.path.join(settings.BASE_DIR, 'templates/mail/' + arguments['template_name'])
        del arguments['template_name']
        arguments.update({'username' : self.user.username})

        text_content = f'Привет, { self.user.username }!'

        with open(template_name, "r", encoding='utf-8') as f:
            html_content = f.read()
            for var in arguments.keys():
                html_content = html_content.replace('{{ ' + var + ' }}', arguments[var])


            msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [self.user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    def reset_password(self):
        hash = str(hashlib.md5(self.user.username.encode('utf-8')).hexdigest()) + random_string(10)
        hash = hashlib.md5(hash.encode('utf-8')).hexdigest()

        # http://127.0.0.1:8000/

        arguments = arguments = {'template_name' : 'concat_reset.html',
                'link' : settings.HOST + 'reset_password/' + hash,
                'unsub' : os.path.join(settings.HOST, 'unsub_email'),
                'domain' : settings.DOMAIN
                                 }

        reset_object = UserPasswordRecovery(user=self.user, key1=hash)
        reset_object.save()

        self.email_user('Восстановление пароля', arguments)



@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


class UserEmailConfirmation(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    key1 = models.TextField(max_length=64)
    key2 = models.TextField(max_length=64)
    expires = models.DateTimeField(default=datetime.datetime.now(
        pytz.utc) + datetime.timedelta(hours=24))


class UserFriendInvitation(models.Model):
    sender = models.ForeignKey(to=User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(to=User, related_name="receiver", on_delete=models.CASCADE)
    cancelled = models.BooleanField(default=False)


class UserFriend(models.Model):
    users = models.ForeignKey(to=User, related_name="user", on_delete=models.CASCADE)
    follower = models.ForeignKey(to=User, related_name="follower", on_delete=models.CASCADE)

# class Skill(models.Model):
#     name = models.CharField(max_length=30)
#
# class Skills(models.Model):
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE)
#     skill = models.ForeignKey(to=Skill, on_delete=models.CASCADE)
