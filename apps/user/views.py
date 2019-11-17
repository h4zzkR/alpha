from django.shortcuts import render, HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from .forms import AuthForm, RegisterForm
from .models import UserProfile

from django.conf import settings
# Create your views here.


def get_context(request, pagename):
    context = {
        'pagename': pagename,
    }

    # if request.user.is_authenticated:
    context.update({'user': request.user})
    try:
        context.update({'user_profile': profile(request.user)})
    except:
        context.update({'user_profile': None })
    return context

def profile(user_obj):
    """
    Вернуть объект UserProfile для объекта User
    :param user_obj:
    :return:
    """
    return UserProfile.objects.get(user=user_obj)


def index(request):
    if request.user.is_authenticated:
        context = get_context(request, 'Хаб')
        return render(request, 'index.html', context)
    else:
        context = get_context(request, 'greetings')
        return render(request, 'greetings.html', context)


class RegisterFormView(FormView):
    form_class = RegisterForm
    success_url = "/accounts/login"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        # Add action to invalid form phase
        print(form.error_messages)
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

