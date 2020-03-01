from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
from django import template
from django.contrib.postgres.fields import ArrayField


register = template.Library()

@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)


class Tag(models.Model):
    name = models.CharField(default="", blank=True, max_length=100)

    def __str__(self):
        return self.name


class Collaborator(models.Model):
    member = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    role = models.CharField(default='Роль не задана', blank=True, max_length=30)

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

    technical_spec_url = models.URLField(default="", max_length=100)
    is_public = models.BooleanField(default=True)

    status = models.IntegerField(default=0)  # 0 - finding team; 1 - developing; 2 - refinding people; 3 - closed

    trello = models.TextField(default="", blank=True)
    vcs = models.TextField(default="", blank=True)
    callback = models.TextField(default="", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
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

    def add_member(self, user, role=None, can_edit_project=False, is_teamlead=False, is_author=False):
        c = Collaborator.objects.create(member=user,
                                        role=role, can_edit_project=can_edit_project,
                                        is_teamlead=is_teamlead, is_author=is_author)
        c.save()
        self.collaborators.add(c)

    def kick_member(self, user):
        try:
            self.collaborators.remove(Collaborator.objects.get(member=user))
        except Collaborator.DoesNotExist:
            pass

    def change_rights(self, user, can_edit_project=None, is_teamlead=None, is_author=None):
        col = self.collaborators.get(member=user)
        if can_edit_project is not None:
            col.can_edit_project = can_edit_project
        if is_teamlead is not None:
            col.is_teamlead = is_teamlead
        if is_author is not None:
            col.is_author = is_author
        col.save()

    def request_project(self, user):
        request = ProjectRequest(user=user, project=self)
        request.save()




class ProjectInvitation(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    cancelled = models.IntegerField(default=0)  # 0 - unread, 1 - accepted, 2 - unaccepted
    message = models.TextField(default="Hey, join my project.")


class Skill(models.Model):
    name = models.CharField(max_length=30)


class ProjectSkills(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    skill = models.ForeignKey(to=Skill, on_delete=models.CASCADE)
    # tags = models.ManyToManyField(Tag)
    tags = TaggableManager()


class ProjectRequest(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)  # 1 - pending, 2 - accepted, 3 - rejected

    created_at = models.DateTimeField(auto_now_add=True)


class ProjectInvite(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)  # 1 - pending, 2 - accepted, 3 - rejected
