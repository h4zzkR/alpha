from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput, URLInput, Textarea
from .models import User
from .models import Project
from django.contrib.auth import authenticate
from modules.helpers import update_avatar
from alpha.settings import DEBUG

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _





class ProjectForm(forms.ModelForm):
    # error_messages = {
    #     'password_mismatch': _("Введенные пароли не совпадают"),
    # }

    def __init__(self, user, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.user = user

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
                                        attrs={'class': 'form-control', 'placeholder': 'Максимальное количество участников',
                                                            'label': 'max_people', 'name': 'max_people', 'value' : 0,}))

    technical_spec_url = forms.URLField(required=False, max_length=Project._meta.get_field('technical_spec_url').max_length,
                        widget=URLInput(attrs={'placeholder': "Ссылка на ТЗ (если есть)",
                                               'id': 'technical_spec_url',
                                               'name': 'technical_spec_url',
                                               'class': 'form-control form-control-alternative',
                                               }))

    type = forms.ChoiceField(required=True,
                                     widget=forms.Select(attrs={
                                         'class' : 'form-control form-control-alternative',
                                         'id' : 'type',
                                         'name' : 'type'
                                     }),
                                     choices=('Приватный', 'Открытый')
                                     )

    type = forms.CharField(label='Тип проекта',
                           widget=forms.Select(attrs={'class' : 'form-control form-control-alternative',
                                                      'id': 'type',
                                                      'name': 'type'
                                                      },
                                                    choices=
                                                        [('open', 'Открытый'),
                                                         ('private', 'Приватный')])
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


    class Meta:
        model = Project
        fields = (
            "name", "description", "max_people", "technical_spec_url",
            "trello", "vcs", "callback"
        )

    def save(self, commit=True):
        project = super(ProjectForm, self).save(commit=False)
        if commit:
            project.save()
            project.author = self.user
            if self.cleaned_data['type'] == 'open':
                project.is_public = True
            else:
                project.is_public = False
            project.save()

        return project