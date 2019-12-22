from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Skill(models.Model):
    name = models.TextField(default="")


class Tag(models.Model):
    pass

class Project(models.Model):
    name = models.TextField(default="", blank=True)
    description = models.TextField(default="", blank=False)
    max_people = models.IntegerField(default=0)  # 0 - no limit

    technical_spec_url = models.URLField(default="", max_length=100)
    is_public = models.BooleanField(default=0)

    status = models.IntegerField(default=True)  # 0 - finding team; 1 - developing; 2 - refinding people; 3 - closed
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)

    trello = models.TextField(default="", blank=True)
    vcs = models.TextField(default="", blank=True)
    callback = models.TextField(default="", blank=True)

    # tags


class ProjectSkills(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    skill = models.ForeignKey(to=Skill, on_delete=models.CASCADE)


class ProjectInvitation(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    message = models.TextField(default="Hey, join my project.")
