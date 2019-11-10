from django.contrib import admin
from django.urls import path, include
import apps.user.views as u
from django.conf import settings
from django.conf.urls.static import static
from apps.user import views


urlpatterns = [
    path('', u.index),
    path('register', u.RegisterFormView.as_view()),
    path('login', u.LoginFormView.as_view()),
    path('logout', u.LogoutView.as_view()),
]