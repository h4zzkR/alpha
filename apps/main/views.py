import json

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from apps.project.models import Project
from django.contrib.auth.models import User
from apps.user.models import UserProfile


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


def json_skills(tags = UserProfile.skills.all()):
    tag_list = []
    for i in range(len(tags)):
        tag = tags[i].name
        tag_list.append({ "value" : str(i), "text" : tag })
    return json.dumps(tag_list, ensure_ascii=False).replace('\"','"')


def index(request):
    if request.user.is_authenticated:
        context = get_context(request, 'Хаб')
        # print(request.user.profile)
        context.update({'projects': Project.objects.all()})

        arguments = {'template_name' : 'concat_reset.html',
                'link' : 'http://127.0.0.1:8000/',
                'unsub' : 'http://127.0.0.1:8000/',
                'domain' : 'concat.org'}

        user = User.objects.get(username=request.user.username)
        user.profile.reset_password()

        return render(request, 'index.html', context)
    else:
        context = get_context(request, 'greetings')
        return render(request, 'greetings.html', context)


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