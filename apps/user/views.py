from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from .forms import AuthForm, RegisterForm, ProfileEditForm, UserEditForm, SupportForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import json
import pytz
import os

import requests

from modules.helpers import pillow_update_avatar, update_avatar

from github import Github

from django.core.signals import request_finished
from django.dispatch import receiver

from .models import UserPasswordRecovery
from django.http import Http404
import datetime

# To profile fields : user.profile.profile_field
from ..main.views import get_context, ajax_messages, json_skills, Messages
from ..project.views import handler404


class RegisterFormView(FormView):
    form_class = RegisterForm
    success_url = '/account/login/'
    template_name = "register.html"
    extra_context = {'pagename': 'Регистрация'}

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        m = Messages()
        msgs = m.parse_messages(form.error_messages)
        for level in msgs.keys():
            m.add(self.request, level, msgs[level])
        return self.render_to_response(
            self.get_context_data(request=self.request, form=form))


def messages_parser(request, query=None):
    messages.error(request, 'Неправильный логин/пароль', extra_tags='safe')


class LoginFormView(FormView):
    form_class = AuthForm
    template_name = "login.html"
    success_url = "/account/profile/"
    extra_context = {'pagename': 'Вход'}

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        m = Messages()
        m.add(self.request, "Заполните свой профиль как можно больше.", "warning")
        return super(LoginFormView, self).form_valid(form)

    def form_invalid(self, form):
        m = Messages()
        msgs = m.parse_messages(form.error_messages)
        for level in msgs.keys():
            m.add(self.request, level, msgs[level])
        return self.render_to_response(
            self.get_context_data(request=self.request, form=form))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


def support(request):
    m = Messages()
    u = request.user
    if request.method == 'POST':
        support_form = SupportForm(request.POST)
        if support_form.is_valid():
            arguments = {"domain": settings.HOST}
            template_name = os.path.join(settings.BASE_DIR, 'templates/mail/concat_support.html')
            with open(template_name, "r", encoding='utf-8') as f:
                html_content = f.read()
                for var in arguments.keys():
                    html_content = html_content.replace('{{ ' + var + ' }}', arguments[var])
                msg = EmailMultiAlternatives("Обращение в Тех.Поддержку", "", settings.EMAIL_HOST_USER, [support_form.data['email']])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            msg = EmailMultiAlternatives(f"Обращение от пользователя {request.user.username}.", f'Текст Обращения: {support_form.data["question"]}\n Email: {support_form.data["email"]}\n Имя: {support_form.data["name"]}', settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
            msg.send()
            m.add(request, 'success', 'Обращение было успешно отправлено.')
        else:
            m.add(request, 'error', 'Что-то пошло не так...')
        return redirect('/')
    else:
        support_form = SupportForm()
        if request.user.is_authenticated:
            support_form.email = request.user.email

    context = get_context(request, 'Поддержка')
    context.update({'form': support_form})
    return render(request, 'support.html', context)


def profile_resolver(request, username):
    if request.user.is_authenticated and request.user.username == username:
        # user is profile owner
        a = update_profile(request)
        return redirect(reverse('user_profile'), get_context(request, 'Профиль'))
    else:
        # client tries to look smb profile
        try:
            u = User.objects.get(username=username)
            user_form = UserEditForm(instance=u)
            for field_name in user_form.fields:
                user_form.fields[field_name].disabled = True
            profile_form = ProfileEditForm(instance=u.profile)
            for field_name in profile_form.fields:
                profile_form.fields[field_name].disabled = True
            context = get_context(request, 'Профиль')
            context.update({'form': user_form})
            context.update({'form2': profile_form})
            context.update({'user_profile': u})
            context.update({'skills': json_skills()})
            return render(request, 'profile_view.html', context)
        except User.DoesNotExist:
            return handler404(request)


def render_to_json(request, data):
    return HttpResponse(
        json.dumps(data, ensure_ascii=False),
        mimetype=request.is_ajax() and "application/json" or "text/html"
    )


@login_required
def update_profile(request):
    m = Messages()
    u = request.user
    if request.method == 'POST':
        response_data = {}
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            obj = profile_form.save(commit=False)
            profile_form.save_m2m()
            u.save()
            response_data.update(user_form.cleaned_data)
            response_data.update(profile_form.cleaned_data)
            m.add(request, 'success', 'Ваш профиль был успешно обновлен!')
            response_data.update({'messages': ajax_messages(request)})
        else:
            print(profile_form.errors)
            m.add(request, 'error', 'Что-то пошло не так...')
            response_data.update({'messages': ajax_messages(request)})
        return JsonResponse(response_data)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = get_context(request, 'Профиль')
    context.update({'form': user_form})
    context.update({'form2': profile_form})
    context.update({'user': u})
    context.update({'skills': json_skills()})
    return render(request, 'profile_.html', context)


@login_required
@csrf_exempt
def update_profile_avatar(request):
    from modules.helpers import update_avatar
    m = Messages()
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        update_avatar(request.POST['image'], user)
        user.save()
        response_data = {}
        m.add(request, 'success', 'Аватар обновлен!')
        response_data.update({'messages': ajax_messages(request)})
        return JsonResponse(response_data)


def reset_password(request, reset_obj):
    if request.method == 'POST':
        m = Messages()
        try:
            password = request.POST.get('password')
            reset_obj = UserPasswordRecovery.objects.get(key1=reset_obj)
            user = reset_obj.user
            user.set_password(password)
            user.save()
            reset_obj.delete()
            m.add(request, 'success', 'Ваш пароль обновлён. Войдите с новыми данными.')
            return redirect('/', request)
        except Exception as err:
            print(err)
            raise Http404
    else:
        return render(request, 'reset_password.html', {'reset_obj': reset_obj.key1, 'user': reset_obj.user.username})


def reset_password_check_hash(request, hash):
    try:
        reset_obj = UserPasswordRecovery.objects.get(key1=hash)
    except:
        raise Http404
    if reset_obj.expires > datetime.datetime.now(pytz.utc):
        return reset_password(request, reset_obj)

    else:
        raise Http404


def request_reset(request):
    if request.method == 'POST':
        user_or_mail = request.POST.get('user_or_email')
        m = Messages()
        try:
            if '@' in user_or_mail:
                mail = user_or_mail
                User.objects.get(email=mail).profile.reset_password()
            else:
                username = user_or_mail
                User.objects.get(username=username).profile.reset_password()
            m.add(request, 'success', 'Письмо с ссылкой на страницу восстановление пароля отправлено.')
        except User.DoesNotExist:
            m.add(request, 'error', 'Такого пользователя не существует. Проверьте введенные данные.')
            return redirect('/account/reset/', request)
        return redirect('/', request)
    else:
        return render(request, 'reset_password_request.html')


def github_api(access_token):
    g = Github(access_token)
    return g


def get_json_response(url):
    return json.loads(requests.get(url).content)


def github_count_commits_stars(repos_url):
    response = requests.get(repos_url)
    repos = json.loads(response.content)
    total_commits, total_stars = 0, 0
    for r in repos:
        stars = get_json_response(r['stargazers_url'])
        commits = get_json_response(r['commits_url'])
        total_commits += len(commits)
        total_stars += len(stars)
    return total_stars, total_commits


def save_profile(backend, user, response, *args, **kwargs):
    from io import BytesIO
    from PIL import Image

    if backend.name == 'github':
        if user is None:
            user = User(user_id=user.id)
        user.profile.github_account = response.get('login')
        user.email = response.get('email')
        if user.email == "":
            user.email = "wrongemail"
        if response['bio'] is None:
            user.profile.bio = "Нет биографии"
        else:
            user.profile.bio = response['bio']
        img = Image.open(BytesIO(requests.get(response.get('avatar_url')).content))
        pillow_update_avatar(img, user)
        user.profile.github_projects_cnt = response.get('public_repos', 0)
        user.profile.github = response.get('html_url')
        if user.username == response.get('login'):
            user.username = response.get('login')

        user.github_id = response.get('id')
        user.profile.confirmed = True

        name = response.get('name')
        if name is not None:
            if len(name.split()) == 2:
                user.profile.first_name = name.split()[0]
                user.profile.last_name = name.split()[1]
            else:
                user.profile.first_name = name.split()[0]
        else:
            name = "Anonymous User"
        user.profile.github_access_token = response.get('access_token')
        user.profile.github_followers = response.get('followers')
        location = response.get('location')
        if location is not None:
            user.profile.location = location
        else:
            user.profile.location = "NO LOCATION"
        repos = response.get('repos_url')
        # stars, commits = github_count_commits_stars(repos)
        # print(stars, commits)
        # user.profile.github_commits = commits
        # user.profile.github_stars = stars
        user.save()
