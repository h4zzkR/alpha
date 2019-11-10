from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
import apps.user.views as u

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.user.urls')),
    # path('', include('apps.project.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
