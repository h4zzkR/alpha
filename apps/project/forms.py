from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput, URLInput, Textarea
from .models import User
from .models import Project, Tag, Collaborator
from django.contrib.auth import authenticate
from modules.helpers import update_avatar
from alpha.settings import DEBUG

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from taggit.forms import *


class ProjectForm(forms.ModelForm):
    name = forms.CharField(required=True, max_length=Project._meta.get_field('name').max_length,
                           widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Название',
                                                   'label': 'name', 'name': 'name'}))

    description = forms.CharField(required=False, max_length=Project._meta.get_field('description').max_length,
                                  widget=forms.Textarea(
                                      attrs={'placeholder': "Подробно опишите идею Вашего проекта",
                                             "rows": "4",
                                             'id': 'description',
                                             "maxlength": Project._meta.get_field('description').max_length,
                                             'name': 'description',
                                             'class': 'form-control form-control-alternative'}))

    max_people = forms.IntegerField(required=False, max_value=10,
                                    widget=forms.NumberInput(
                                        attrs={'class': 'form-control',
                                               'placeholder': 'Максимальное количество участников',
                                               'label': 'max_people', 'min': 0, 'max': 10, 'name': 'max_people',
                                               'value': 0, }))

    technical_spec_url = forms.URLField(required=False,
                                        max_length=Project._meta.get_field('technical_spec_url').max_length,
                                        widget=URLInput(attrs={'placeholder': "Ссылка на ТЗ (если есть)",
                                                               'id': 'technical_spec_url',
                                                               'name': 'technical_spec_url',
                                                               'class': 'form-control form-control-alternative',
                                                               }))

    is_public = forms.CharField(label='Тип проекта',
                                widget=forms.Select(attrs={'class': 'selectpicker',
                                                           'id': 'type',
                                                           'name': 'type'
                                                           },
                                                    choices=
                                                    [(1, 'Открытый'),
                                                     (0, 'Приватный')])
                                )

    trello = forms.URLField(required=False, max_length=Project._meta.get_field('trello').max_length,
                            widget=URLInput(attrs={'placeholder': "Ссылка на Kanban (Trello)",
                                                   'id': 'trello',
                                                   'name': 'trello',
                                                   'class': 'form-control form-control-alternative',
                                                   }))

    vcs = forms.URLField(required=False, max_length=Project._meta.get_field('vcs').max_length,
                         widget=URLInput(attrs={'placeholder': "Ссылка на VCS",
                                                'id': 'vcs',
                                                'name': 'vcs',
                                                'class': 'form-control form-control-alternative',
                                                }))

    callback = forms.URLField(required=False, max_length=Project._meta.get_field('callback').max_length,
                              widget=URLInput(attrs={'placeholder': "Связь и общение (Telegram, Discord, Slack)",
                                                     'id': 'callback',
                                                     'name': 'callback',
                                                     'class': 'form-control form-control-alternative',
                                                     }))

    tags = TagField(min_length=2, required=False,
                    widget=forms.TextInput(
                        attrs={
                            'data-role': 'tagsinput',
                            'name': 'tags',
                            'id': 'tags-input'},

                    ))

    class Meta:
        model = Project
        fields = (
            "name", "description", "max_people", "technical_spec_url",
            "trello", "vcs", "callback", 'tags', 'is_public',
        )

    def save(self, user):
        project = super(ProjectForm, self).save(commit=False)
        project.is_public = int(self.cleaned_data['is_public'])

        if project.author is None:
            project.author = user
            project.save()
            t = Collaborator(member=user, is_author=True,
                             can_edit_project=True, is_teamlead=True)
            t.save()
            # print(t)
            project.collaborators.add(t)
        project.save()

        return project
