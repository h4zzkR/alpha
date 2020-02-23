import json

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from apps.project.models import Project
from django.contrib.auth.models import User
from apps.user.models import UserProfile

from django.db.models import Q


def get_context(request, pagename):
    context = {
        'pagename': pagename,
    }
    context.update({'user': request.user})
    if request.user.is_authenticated:
        context.update({'nav_projects' : Project.objects.filter(collaborators__member=request.user).order_by("-created_at")})
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
        context = get_context(request, 'Dashboard')
        # print(request.user.profile)
        # context.update({'projects': Project.objects.all()})

        # arguments = {'template_name' : 'concat_reset.html',
        #         'link' : 'http://127.0.0.1:8000/',
        #         'unsub' : 'http://127.0.0.1:8000/',
        #         'domain' : 'concat.org'}

        # user = User.objects.get(username=request.user.username)
        # github_login = user.social_auth.get(provider='github')
        # user.profile.reset_password()
        # print(user.profile.github_stars)

        projects = Project.objects.all().order_by("-created_at")
        context.update({'object_list' : projects})
        context.update({'type' : 'projects'})
        context.update({'sort' : '-created_at'})

        # print(projects)


        return render(request, 'index.html', context)
    else:
        context = get_context(request, 'greetings')
        return render(request, 'login.html', context)



def search_engine(request):
    data = request.GET['q'].split('+')
    type = request.GET['type']
    sort = request.GET['sort']

    # new_context = Project.objects.filter(collaborators__in=[self.request.user]).order_by("-created_at")
    # new_context = Project.objects.filter(collaborators__member=self.request.user).order_by("-created_at")

    # q = Entry.objects.filter(headline__startswith="What")
    # q = q.filter(pub_date__lte=datetime.date.today())
    # q = q.exclude(body_text__icontains="food")
    # print(q)

    p = Project.objects.none()
    if type == 'projects':
        for i in data:
            s = Project.objects.filter(Q(name__icontains=i) | Q(tags__name=i)).order_by(sort)
            p |= s

    context = get_context(request, 'Dashboard')
    context.update({'object_list' : p})
    context.update({'type' : type})
    context.update({'value' : ' '.join(data)})
    context.update({'sort': sort})

    return render(request, 'index.html', context)









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