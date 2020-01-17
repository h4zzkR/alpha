import pytz
import datetime
from django.db import models
from django.contrib.auth.models import User
from apps.project.models import Skill, Project
from django.core.cache import cache
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db.models.signals import post_save
from taggit.managers import TaggableManager


# class UserSkill(models.Model):
#     name = models.CharField(default="", blank=True, max_length=100)
#
#     def __str__(self):
#         return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # user.profile.fields

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    last_seen = models.DateTimeField(auto_now_add=True, blank=True)
    avatar = models.ImageField(upload_to="profile/photos/", blank=True)  # TODO add default userpic
    confirmed = models.BooleanField(default=False) # is account confirmed by email
    rating = models.IntegerField(default=0)
    active_projects_cnt = models.IntegerField(default=0)
    good_teamlead = models.IntegerField(default=0) # users sets this user as a good teamlead
    # phone = models.TextField(default="")
    status = models.TextField(default="")
    github = models.URLField(default="", max_length=len('https://') + 30, blank=True) # or another vcs
    # trello = models.TextField(default="")
    vk = models.URLField(default="", max_length=len('https://vk.com/') + 20, blank=True)
    linked_in = models.URLField(default="", max_length=len('https://') + 20, blank=True)
    telegram = models.URLField(default="",  max_length=len('https://t.me/') + 20, blank=True)
    bio = models.TextField(default="", max_length=80)

    skills = TaggableManager()

    def __str__(self):
        return self.user.username

    def link(self):
        return 'http://127.0.0.1:8000/u/' + self.user.username

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


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


class UserPasswordRecovery(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    key1 = models.TextField(max_length=64)
    key2 = models.TextField(max_length=64)
    expires = models.DateTimeField(default=datetime.datetime.now(
        pytz.utc) + datetime.timedelta(hours=24))


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
