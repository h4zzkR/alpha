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


class UserFriendInvitation(models.Model):
    sender = models.ForeignKey(to=User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(to=User, related_name="receiver", on_delete=models.CASCADE)
    cancelled = models.BooleanField(default=False)


class UserFriend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)
