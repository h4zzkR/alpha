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
# from .forms import AuthForm, RegisterForm, ProfileEditForm, UserEditForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Project
from .forms import ProjectForm
from ..user.views import get_context


from django.views.generic.edit import FormView
from django.views.generic.list import ListView

class ProjectCreate(FormView):
    template_name = 'project_setup.html'
    form_class = ProjectForm
    success_url = '/'   #change

    def get_form_kwargs(self):
        kwargs = super(ProjectCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context(self.request, 'Новый проект')
        return context

    def form_valid(self, form):
        form.save()
        return super(ProjectCreate, self).form_valid(form)

    def form_invalid(self, form):
        # Add action to invalid form phase
        print(form)
        print(form.error_messages)
        # messages.success(self.request, 'An error occured while processing the payment')
        # return self.render_to_response(self.get_context_data(form=form))


class ProjectListView(ListView):

    model = Project
    template_name = 'project_list.html'
    # paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context(self.request, 'Проекты')
        return context



