from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProjectForm
# from .forms import AuthForm, RegisterForm, ProfileEditForm, UserEditForm
from .models import Project
from ..main.views import ajax_messages, json_skills, Messages


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
        context['nav_projects'] = Project.objects.filter(collaborators__member=self.request.user).order_by(
            "-created_at")
        return context

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
        context.update({'pagename': 'Мои Проекты'},)
        context['nav_projects'] = Project.objects.filter(collaborators__member=request.user).order_by(
            "-created_at")
        context['projects'] = Project.objects.filter(collaborators__member=request.user).order_by("-created_at")
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

    return render(request, 'project_setup.html', {
        'form': form,
        'pagename': 'Новый проект',
        'nav_projects': Project.objects.filter(collaborators__member=request.user).order_by(
            "-created_at"),
        'tags': json_skills(Project.tags.all())
    })


def project_view(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return handler404(request)

    # project.add_member(role='aas', user=User.objects.get(username='root'), is_author=False,
    #                  can_edit_project=True, is_teamlead=False)
    # project.save()

    m = Messages()
    if request.method == 'POST':
        response_data = {}
        try:
            col = project.collaborators.get(member=request.user)
        except ObjectDoesNotExist:
            return handler403(request)
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
                m.add(request, 'error', 'Что-то пошло не так...')
                response_data.update({'messages': ajax_messages(request)})
            # return JsonResponse(response_data)
        else:
            return handler403(request)
    else:
        try:
            col = project.collaborators.get(member=request.user)
        except ObjectDoesNotExist:
            return handler403(request)
        if not request.user.is_authenticated or col.can_edit_project is False:
            return handler403(request)
        else:
            project_form = ProjectForm()
            project = Project.objects.get(id=id)

    return render(request, 'project_view.html', {
        'form': project_form,
        'user_id': project.id,
        'project': project,
        'nav_projects': Project.objects.filter(collaborators__member=request.user).order_by(
            "-created_at"),
        'tags': json_skills(Project.tags.all())
    })


def kick_from_project(request, project_id, user_to_kick):
    project = Project.objects.get(id=project_id)
    m = Messages()
    response_data = {}
    if request.user in project.members_with_edit_rights():
        project.kick_member(user_to_kick)
    else:
        raise handler404(request)
    response_data.update({'messages': ajax_messages(request)})
    response_data.update(project.collaborators.all())
    m.add(request, 'success', f'Пользователь {user_to_kick.username} больше не в команде!')
    return JsonResponse(response_data)
    # email kicked user
