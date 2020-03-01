from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput, URLInput, Textarea
from .models import User
from django.contrib.auth import authenticate
from modules.helpers import update_avatar
from .models import UserProfile
from alpha.settings import DEBUG

from django.core.exceptions import ValidationError
from taggit.forms import *
from django.utils.translation import ugettext_lazy as _


class AuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Никнейм',
                                                       'label': 'username', 'name': 'username'}))

    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль',
                                                           'label': 'password', 'name': 'password'}))

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'name': 'remember', 'id': 'customCheckLogin',
        'class': 'custom-control-input'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        remember_me = self.cleaned_data.get('remember_me')

        # if not remember_me:
        #     self.request.session.set_expiry(0)

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RegisterForm(UserCreationForm):
    # TODO add errors callback

    error_messages = {
        'password_mismatch': _("Введенные пароли не совпадают"),
    }

    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Никнейм',
                                                       'label': 'username', 'name': 'username'}))

    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль',
                                                            'label': 'password1', 'name': 'password1'}))

    password2 = forms.CharField(
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль',
                                    'label': 'password2', 'name': 'password2'}))

    email = forms.CharField(widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Почта',
                                                     'label': 'email', 'name': 'email'}))
    agreed = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={
        'name': 'agreed', 'id': 'customCheckRegister',
        'class': 'custom-control-input'}))

    class Meta:
        model = User
        fields = ("username", 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user.refresh_from_db()
            # TODO: Connect userprofile
            if DEBUG == True:
                user.profile.confirmed = True
            update_avatar(self.data['avatar'], user)
            user.save()

        # print(profile)
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", 'email', 'first_name', 'last_name')

    username = forms.CharField(max_length=User._meta.get_field('username').max_length, required=True,
                               widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Новый никнейм',
                                                       'label': 'username', 'name': 'username', 'id': 'username'}))

    email = forms.CharField(max_length=User._meta.get_field('email').max_length, required=True,
                            widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Новая почта',
                                                     'label': 'email', 'name': 'email', 'id': 'email',
                                                     'readonly' : True,}))

    first_name = forms.CharField(max_length=UserProfile._meta.get_field('first_name').max_length, required=False,
                                 widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя',
                                                         'label': 'first_name', 'name': 'first_name',
                                                         'id': 'first_name'}))

    last_name = forms.CharField(max_length=UserProfile._meta.get_field('last_name').max_length, required=False,
                                widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия',
                                                        'label': 'last_name', 'name': 'last_name', 'id': 'last_name'}))

    # def clean(self):
    #     super(UserEditForm, self).clean()


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('github', 'telegram',
                  'linked_in', 'vk', 'bio',
                  'skills',)


    github = forms.URLField(required=False, max_length=UserProfile._meta.get_field('github').max_length,
                            widget=URLInput(attrs={'placeholder': "Ссылка на ваш профиль",
                                                   'id': 'github',
                                                   'name': 'github',
                                                   'class': 'form-control form-control-alternative',
                                                   'onchange': "checkURL(this)",
                                                   }))

    telegram = forms.URLField(required=False, max_length=UserProfile._meta.get_field('telegram').max_length,
                              widget=URLInput(attrs={'placeholder': "Ссылка на ваш профиль",
                                                     'id': 'telegram',
                                                     'name': 'telegram',
                                                     'class': 'form-control form-control-alternative',
                                                     'onchange': "checkURL(this)",
                                                     }))

    linked_in = forms.URLField(required=False, max_length=UserProfile._meta.get_field('linked_in').max_length,
                               widget=URLInput(attrs={'placeholder': "Ссылка на ваш профиль",
                                                      'id': 'linked_in',
                                                      'name': 'linked_in',
                                                      'class': 'form-control form-control-alternative',
                                                      'onchange': "checkURL(this)",
                                                      }))

    vk = forms.URLField(required=False, max_length=UserProfile._meta.get_field('vk').max_length,
                        widget=URLInput(attrs={'placeholder': "Ссылка на ваш профиль",
                                               'id': 'vk',
                                               'name': 'vk',
                                               'class': 'form-control form-control-alternative',
                                               'onchange': "checkURL(this)",
                                               }))

    bio = forms.CharField(required=False, max_length=UserProfile._meta.get_field('bio').max_length,
                          widget=forms.Textarea(
                              attrs={'placeholder': "Любые детали такие как возраст, страна или город.",
                                     "rows": "4",
                                     'id': 'bio',
                                     "maxlength": UserProfile._meta.get_field('bio').max_length,
                                     'name': 'bio',
                                     'class': 'form-control form-control-alternative'}))


    skills = TagField(min_length=2, required=False, widget=forms.TextInput(
        attrs={
               'data-role' : 'tagsinput',
               'name' : 'skills',},

    ))


    # def clean(self):
    #     # Then call the clean() method of the super  class
    #     cleaned_data = super(ProfileEditForm, self).clean()
    #     cleaned_data.update({'github_stars' : int(list(self.data.values())[4])})
    #     return cleaned_data
