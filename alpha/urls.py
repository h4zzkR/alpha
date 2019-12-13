from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
import apps.user.views as u

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', u.index, name="index"),
    path('accounts/register/', u.RegisterFormView.as_view(), name="user_register"),
    path('account/login/', u.LoginFormView.as_view(), name="user_login"),
    path('account/logout/', u.LogoutView.as_view(), name="user_logout"),
    path('accounts/profile/', u.update_profile, name="user_profile"),
    path('accounts/user/<str:username>', u.profile_resolver, name="user_get_profile"),
    path('accounts/update_avatar/', u.update_profile_avatar, name="user_update_avatar"),
    # path('projects/', include('apps.project.urls'), name="projects"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
