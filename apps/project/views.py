from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProjectForm, ProjectAddForm
# from .forms import AuthForm, RegisterForm, ProfileEditForm, UserEditForm
from .models import Project, ProjectRequest
from ..main.views import ajax_messages, json_skills, Messages, get_context
import os
from django.conf import settings

from django.contrib.auth.decorators import login_required

def handler404(request):
    """
    Страница ошибки 404
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    :rtype: :class:`django.http.HttpResponse`
    """
    return render(request, "404.html", status=404)


def handler403(request):
    """
    Страница ошибки 403
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    :rtype: :class:`django.http.HttpResponse`
    """
    return render(request, "403.html", status=403)


def handler500(request):
    """
    Страница ошибки 505
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    :rtype: :class:`django.http.HttpResponse`
    """
    return render(request, "505.html", status=500)


def ProjectCreate(request):
    template_name = 'project_setup.html'
    form_class = ProjectForm
    success_url = '/'  # change

    def get_form_kwargs(self):
        kwargs = super(ProjectCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'pagename': 'Новый проект',
        })

    def form_valid(self, form):
        form.save(commit=False)
        return super(ProjectCreate, self).form_valid(form)

    def form_invalid(self, form):
        # Add action to invalid form phase
        print("Invalid Form on  CREATE PROJECT VIEW")
        # print(form.error_messages)
        # messages.success(self.request, 'An error occured while processing the payment')
        # return self.render_to_response(self.get_context_data(form=form))


def projects_list(request):
    if request.user.is_authenticated:
        template_name = 'project_list.html'
        context = {}
        # paginate_by = 100  # if pagination is desired
        context = get_context(request, 'MyProjects')

        user_projects = Project.objects.filter(collaborators__member=request.user).order_by("-created_at")
        context['projects'] = user_projects

        out_pending_projects = [i.project for i in ProjectRequest.objects.filter(user=request.user, status=1)]
        context.update({'out_pending_projects' : out_pending_projects})

        in_pending_projects = ProjectRequest.objects.filter(project__in=user_projects, status=1)
        context.update({'in_pending_projects' : in_pending_projects})

        print(in_pending_projects)
        return render(request, template_name, context)
    else:
        return redirect('/account/login/')


def project_create(request):
    m = Messages()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(request.user)
            form.save_m2m()
            return redirect('/projects/')
        else:
            print(form.errors)
    else:
        form = ProjectForm()

    context = get_context(request, 'Новый проект')
    context.update({
        'form': form,
        'pagename': 'Новый проект',
        'tags': json_skills(Project.tags.all())
    })

    return render(request, 'project_setup.html', context)


def project_view(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return handler404(request)
    if project.is_public:
        context = get_context(request, 'Проект')
        context.update({'project' : project})
        context.update({"user": request.user})
        context.update({'is_in': False})
        if request.user.is_authenticated is True:
            for i in project.collaborators.all():
                if request.user == i.member:
                    context.update({'is_in': True})
                    break
        else:
            context.update({'is_in': True}) #do not touch, it is hack for non display on unloginned
        return render(request, 'project_view.html', context)
    else:
        return handler403(request)


def project_view_or_edit(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return handler404(request)

    m = Messages()
    if request.method == 'POST':
        response_data = {}
        try:
            col = project.collaborators.get(member=request.user)
        except ObjectDoesNotExist:
            # just view project
            return redirect(f'project/v/{id}', request)
        if request.user.is_authenticated and col.can_edit_project is True:
            project_form = ProjectForm(request.POST, instance=project)
            if project_form.is_valid():
                project = project_form.save(request.user)
                # response_data.update(project_form.cleaned_data)
                # response_data.update(project_form.cleaned_data)
                # m.add(request, 'success', 'Успешно')
                project.save()
                project_form.save_m2m()
                response_data.update({'messages': ajax_messages(request)})
            else:
                print(project_form.errors)
                m.add(request, 'error', 'Что-то пошло не так...')
                response_data.update({'messages': ajax_messages(request)})
            # return JsonResponse(response_data)
        else:
            # just view project
            return redirect(f'/project/v/{id}', request)
    else:
        if not request.user.is_authenticated:
            return redirect(f'/project/v/{id}', request)
        try:
            col = project.collaborators.get(member=request.user)
        except ObjectDoesNotExist:
            return redirect(f'/project/v/{id}', request)
        if col.can_edit_project is False:
            return redirect(f'/project/v/{id}', request)
        else:
            project_form = ProjectForm()
            project = Project.objects.get(id=id)

    context = get_context(request, 'Проект')
    context.update({
        'form': project_form,
        'user_id': project.id,
        'project': project,
        'tags': json_skills(Project.tags.all())
    })
    return render(request, 'project_edit.html', context)


def project_team_view(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return handler404(request)
    if project.is_public:
        context = get_context(request, 'Проект')
        context.update({'project': project})
        context.update({"user": request.user})
        return render(request, 'project_team_view.html', context)
    else:
        return handler403(request)


def project_team_edit(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return handler404(request)

    m = Messages()
    if request.method == 'POST':
        response_data = {}
        try:
            col = project.collaborators.get(member=request.user)
        except ObjectDoesNotExist:
            # just view project
            return redirect(f'project/v/{id}', request)
        if request.user.is_authenticated and col.can_edit_project is True:
            project_form = ProjectAddForm(request.POST)
            if project_form.is_valid():
                project = project_form.save()
                # response_data.update(project_form.cleaned_data)
                # response_data.update(project_form.cleaned_data)
                # m.add(request, 'success', 'Успешно')
                project.save()
                project_form.save_m2m()
                response_data.update({'messages': ajax_messages(request)})
            else:
                print(project_form.errors)
                m.add(request, 'error', 'Что-то пошло не так...')
                response_data.update({'messages': ajax_messages(request)})
            # return JsonResponse(response_data)
        else:
            # just view project
            return redirect(f'/project/v/{id}/team/', request)
    else:
        if not request.user.is_authenticated:
            return redirect(f'/project/v/{id}/team/', request)
        try:
            col = project.collaborators.get(member=request.user)
        except ObjectDoesNotExist:
            return redirect(f'/project/v/{id}/team/', request)
        if col.can_edit_project is False:
            return redirect(f'/project/v/{id}/team/', request)
        else:
            project_form = ProjectAddForm()
            project = Project.objects.get(id=id)

    context = get_context(request, 'Команда')
    context.update({
        'form': project_form,
        'user_id': project.id,
        'project': project,
        'tags': json_skills(Project.tags.all())
    })
    return render(request, 'project_team_edit.html', context)


@login_required
def project_request(request, id):
    m = Messages()
    project = Project.objects.get(id=id)
    user = request.user
    response_data = {}
    for i in project.collaborators.all():
        if user == i.member:
            m.add(request, 'error', 'Вы уже в составе команды проекта.')
            return redirect('/', request)
    check = ProjectRequest.objects.filter(user=user, project=project, status=1)

    if len(check) != 0:
        m.add(request, 'error', 'Вы уже отправляли запрос, дождитесь рассмотрения вашей заявки.')
    else:
        project.request_project(request.user)
        #TODO
        args = {'template_name' : 'concat_request_project.html',
                'username' : request.user.username,
                'user' : request.user.username,
                'link' : settings.HOST + 'projects/',
                'unsub' : os.path.join(settings.HOST, 'unsub_email'),
                'domain' : settings.DOMAIN
                                 }
        project.author.profile.email_user('Вашим проектом кто-то заинтересовался!', args)
        m.add(request, 'success', 'Ваш запрос отправлен тимлиду проекта.')
    response_data.update({'messages': ajax_messages(request)})
    return JsonResponse(response_data)

@login_required
def projects_undo_request(request, id):
    project = Project.objects.get(id=id)
    for i in ProjectRequest.objects.filter(project=project, user=request.user, status=1):
        i.delete()
    return redirect('/projects/')

def projects_accept_request(request):
    username, pr_id = request.GET['user'], request.GET['project']
    m = Messages()
    project = Project.objects.get(id=pr_id)
    user = User.objects.get(username=username)
    proj_request = ProjectRequest.objects.get(project=project, user=user)
    print(project.author)
    if request.user == project.author:
        project.add_member(user, role='')
        project.save()
        m.add(request, 'success', f'{username} был добавлен в Вашу команду!')
        args = {'template_name' : 'concat_request_accept.html',
                'project' : project.name,
                'username': username,
                'unsub' : os.path.join(settings.HOST, 'unsub_email'),
                'domain' : settings.DOMAIN,
                'link': settings.HOST + 'project/v/' + pr_id,
                                 }
        user.profile.email_user('Вы были добавлены в команду.', args)
        proj_request.delete()
    else:
        return handler404(request)
    return redirect('/projects', request)


def projects_decline_request(request):
    username, pr_id = request.GET['user'], request.GET['project']
    m = Messages()
    project = Project.objects.get(id=pr_id)
    user = User.objects.get(username=username)
    proj_request = ProjectRequest.objects.get(project=project, user=user)
    print(project.author)
    if request.user == project.author:
        m.add(request, 'success', f'Запрос пользователя {username} был отклонен.')
        args = {'template_name': 'concat_request_decline.html',
                'project': ' ' + project.name,
                'username': username,
                'unsub': os.path.join(settings.HOST, 'unsub_email'),
                'domain': settings.DOMAIN,
                'link': settings.HOST + 'project/v/' + pr_id,
                }
        user.profile.email_user('Запрос на вступление в команду отклонен.', args)
        proj_request.delete()
    else:
        return handler404(request)
    return redirect('/projects', request)




def kick_from_project(request, project_id, user_to_kick):
    user_to_kick = User.objects.get(username=user_to_kick)
    project = Project.objects.get(id=project_id)
    m = Messages()

    response_data = {}
    if request.user in project.members_with_edit_rights():
        project.kick_member(user_to_kick)
    else:
        return handler404(request)
    response_data.update({'messages': ajax_messages(request)})
    response_data.update(project.collaborators.all())
    m.add(request, 'success', f'Пользователь {user_to_kick.username} больше не в команде!')
    return JsonResponse(response_data)
    # email kicked user

