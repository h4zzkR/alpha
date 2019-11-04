from django.contrib import admin
from django.urls import path, include
import apps.user.views as u

urlpatterns = [
    path('index', u.index)
]