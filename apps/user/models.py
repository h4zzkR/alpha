import pytz
import datetime
from django.db import models
from django.contrib.auth.models import User
from apps.project.models import Skill, Project


class UserProfile(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    userpic = models.ImageField(upload_to="userpics", blank=True) # TODO add default userpic
    confirmed = models.BooleanField(default=False) # is account confirmed by email
    rating = models.IntegerField(default=0)
    good_teamlead = models.IntegerField(default=0) # users sets this user as a good teamled
    phone = models.TextField(default="")
    status = models.TextField(default="")
    github = models.TextField(default="")
    trello = models.TextField(default="")
    vk = models.TextField(default="")
    facebook = models.TextField(default="")


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


class UserSkill(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    skill = models.ForeignKey(to=Skill, on_delete=models.CASCADE)


class UserProject(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)


class UserFriendInvitation(models.Model):
    sender = models.ForeignKey(to=User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(to=User, related_name="receiver", on_delete=models.CASCADE)
    cancelled = models.BooleanField(default=False)


class UserFriend(models.Model):
    users = models.ForeignKey(to=User, related_name="user", on_delete=models.CASCADE)
    follower = models.ForeignKey(to=User, related_name="follower", on_delete=models.CASCADE)
