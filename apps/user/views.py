from django.shortcuts import render, HttpResponse
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from .forms import AuthForm, RegisterForm, ProfileEditForm
from .models import UserProfile
from django.contrib.auth.models import User

from django.conf import settings

# To profile fields : user.profile.profile_field


def get_context(request, pagename):
    context = {
        'pagename': pagename,
    }
    context.update({'user': request.user})
    # TEMP FIX OF MISSING MEDIA_URL AND STATIC_URL
    # context.update({'BASE_DIR': settings.BASE_DIR})
    return context


def index(request):
    if request.user.is_authenticated:
        context = get_context(request, 'Хаб')
        # print(request.user.profile)
        return render(request, 'index.html', context)
    else:
        context = get_context(request, 'greetings')
        return render(request, 'greetings.html', context)


class RegisterFormView(FormView):
    form_class = RegisterForm
    success_url = "/accounts/login"
    template_name = "register.html"
    errors = {}
    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context.update({'error': list(self.errors.items())[0][1]})
        except:
            pass
        return context

    def form_invalid(self, form):
        # Add action to invalid form phase
        print(form.error_messages)
        self.errors = form.error_messages
        return super(RegisterFormView, self).form_invalid(form)
        # messages.success(self.request, 'An error occured while processing the payment')
        # return self.render_to_response(self.get_context_data(form=form))


class LoginFormView(FormView):
    form_class = AuthForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


def get_user(request, username=None):
    if username == request.user.username or username is None:
        return UserUpdate.as_view()(request, username)
    else:
        # return profile page for showing
        pass


class UserUpdate(UpdateView):
    form_class = ProfileEditForm
    template_name = 'profile_.html'
    success_url = '/profile'


    def get_object(self, queryset=None):
        # username = self.kwargs.get("username")
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context(self.request, 'Профиль'))
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        super(UserUpdate, self).form_valid(form)
        return super(UserUpdate, self).form_valid(form)