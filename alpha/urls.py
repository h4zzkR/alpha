from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
import apps.user.views as u
from apps.user.urls import urlpatterns as upatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', u.index, name="index"),
    path('accounts/', include('apps.user.urls'), name="user"),
    # path('projects/', include('apps.project.urls'), name="projects"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    upatterns
