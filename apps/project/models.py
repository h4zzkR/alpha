from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager

from django import template

register = template.Library()

@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)

# Create your models here.

class Skill(models.Model):
    name = models.TextField(default="")


class Tag(models.Model):
    name = models.CharField(default="", blank=True, max_length=100)

    def __str__(self):
        return self.name


class Collaborator(models.Model):
    member = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    role = models.CharField(default='не задано', blank=True, max_length=30)

    entered_at = models.DateTimeField(auto_now_add=True)
    can_edit_project = models.BooleanField(default=False)
    is_teamlead = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)

class Project(models.Model):
    name = models.TextField(default="", blank=True)
    description = models.TextField(default="", blank=False)
    max_people = models.IntegerField(default=0)  # 0 - no limit

    author = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    collaborators = models.ManyToManyField(Collaborator, related_name='collabs')
    # collaborators = models.ManyToManyField(User, related_name='collabs')

    technical_spec_url = models.URLField(default="", max_length=100)
    is_public = models.BooleanField(default=0)

    status = models.IntegerField(default=True)  # 0 - finding team; 1 - developing; 2 - refinding people; 3 - closed

    trello = models.TextField(default="", blank=True)
    vcs = models.TextField(default="", blank=True)
    callback = models.TextField(default="", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # tags = models.ManyToManyField(Tag)
    tags = TaggableManager()

    def get_status(self):
        if self.status == 0:
            return 'Набор в проект'
        elif self.status == 1:
            return 'В разработке'
        elif self.status == 2:
            return 'Поиск участников'
        elif self.status == 3:
            return 'Завершен'

    def list_tags(self):
        return ','.join([t.name for t in self.tags.all()])

    def members_with_edit_rights(self):
        return [i.member for i in self.collaborators.filter(can_edit_project=True)]





class ProjectSkills(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    skill = models.ForeignKey(to=Skill, on_delete=models.CASCADE)


class ProjectInvitation(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    message = models.TextField(default="Hey, join my project.")
