from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound
from django.views.generic.edit import FormView, UpdateView
from django.conf import settings
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from .forms import AuthForm, RegisterForm, ProfileEditForm, UserEditForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import json
from .models import UserSkill, UserProfile
from apps.project.models import Project
from django.core.serializers import serialize


# To profile fields : user.profile.profile_field


def get_context(request, pagename):
    context = {
        'pagename': pagename,
    }
    context.update({'user': request.user})
    # TEMP FIX OF MISSING MEDIA_URL AND STATIC_URL
    # context.update({'BASE_DIR': settings.BASE_DIR})
    return context


def ajax_messages(request):
    django_messages = []

    for message in messages.get_messages(request):
        django_messages.append({
            "level": settings.MESSAGE_TAGS[message.level],
            "message": message.message,
            "extra_tags": message.tags,
        })

    return django_messages


def index(request):
    if request.user.is_authenticated:
        context = get_context(request, 'Хаб')
        # print(request.user.profile)
        context.update({'projects': Project.objects.all()})
        print(context)
        return render(request, 'index.html', context)
    else:
        context = get_context(request, 'greetings')
        return render(request, 'greetings.html', context)


class RegisterFormView(FormView):
    form_class = RegisterForm
    success_url = '/account/login/'
    template_name = "register.html"

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


class Messages():
    def __init__(self):
        pass

    def parse_messages(self, st):
        msgs = {}
        for k in st.keys():
            if k != 'inactive':
                if k == 'invalid_login':
                    msgs.update({'error': 'Неправильный логин/пароль'})
                else:
                    msgs.update({'error': st[k]})
        return msgs

    def add(self, request, level, message):
        if level == 'error':
            messages.error(request, message, extra_tags='safe')
        elif level == 'warning':
            messages.warning(request, message, extra_tags='safe')
        elif level == 'success':
            messages.success(request, message, extra_tags='safe')
        elif level == 'info':
            messages.info(request, message, extra_tags='safe')


class LoginFormView(FormView):
    form_class = AuthForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

    def form_invalid(self, form):
        m = Messages()
        msgs = m.parse_messages(form.error_messages)
        for level in msgs.keys():
            m.add(self.request, level, msgs[level])
        # m.add(self.request, level, msgs[level])
        return self.render_to_response(
            self.get_context_data(request=self.request, form=form))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


def profile_resolver(request, username):
    if request.user.is_authenticated and request.user.username == username:
        # user is profile owner
        a = update_profile(request)
        return redirect(reverse('user_profile'), get_context(request, 'Профиль'))
    else:
        # client tries to look smb profile
        try:
            User.objects.get(username=username)
            return HttpResponse('Good but 404')
        except ObjectDoesNotExist:
            return HttpResponseNotFound


def render_to_json(request, data):
    return HttpResponse(
        json.dumps(data, ensure_ascii=False),
        mimetype=request.is_ajax() and "application/json" or "text/html"
    )


@login_required
def update_profile(request):
    m = Messages()
    if request.method == 'POST':
        response_data = {}
        # print(request.POST)
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            response_data.update(user_form.cleaned_data)
            response_data.update(profile_form.cleaned_data)
            m.add(request, 'success', 'Ваш профиль был успешно обновлен!')
            response_data.update({'messages': ajax_messages(request)})
            # return redirect(reverse('user_profile'), get_context(request, 'Профиль'))
        else:
            m.add(request, 'error', 'Что-то пошло не так...')
            response_data.update({'messages': ajax_messages(request)})
        return JsonResponse(response_data)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'profile_.html', {
        'form': user_form,
        'form2': profile_form
    })


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
