from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Skill(models.Model):
    name = models.TextField(default="")


class Project(models.Model):
    name = models.TextField(default="")
    description = models.TextField(default="")
    max_people = models.IntegerField(default=0)  # 0 - no limit
    public = models.BooleanField(default=True)
    status = models.IntegerField(default=True)  # 0 - finding team; 1 - developing; 2 - refinding people; 3 - closed
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    trello = models.TextField(default="")
    github = models.TextField(default="")
    discord = models.TextField(default="")


class ProjectSkills(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    skill = models.ForeignKey(to=Skill, on_delete=models.CASCADE)


class ProjectInvitation(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    message = models.TextField(default="Hey, join my project.")
