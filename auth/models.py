import pytz
import datetime
from django.db import models
from django.contrib.auth.models import User
from finder.models import Skill, Project


class UserProfile(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    teamlead = models.IntegerField(default=0)
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


class UserFriends(models.Model):
    user1 = models.ForeignKey(to=User, on_delete=models.CASCADE)
    user2 = models.ForeignKey(to=User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
