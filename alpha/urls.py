from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

import apps.main.views
import apps.user.views as u
import apps.project.views as p


handler404 = 'apps.project.views.handler404'
handler403 = 'apps.project.views.handler403'
handler500 = 'apps.project.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', apps.main.views.index, name="index"),
    path('account/register/', u.RegisterFormView.as_view(), name="user_register"),
    path('account/login/', u.LoginFormView.as_view(), name="user_login"),
    path('account/logout/', u.LogoutView.as_view(), name="user_logout"),
    path('account/profile/', u.update_profile, name="user_profile"),
    path('reset_password/<str:hash>/', u.reset_password_check_hash, name='reset_password'),
    path('u/<str:username>/', u.profile_resolver, name="user_get_profile"),
    path('account/update_avatar/', u.update_profile_avatar, name="user_update_avatar"),
    path('account/reset/', u.request_reset, name='request_reset'),
    path('reset_update/<str:reset_obj>/', u.reset_password, name='reset_update'),
    path('projects/new/', p.project_create, name="project_create"),
    path('projects/', p.projects_list, name='projects_list'),
    path('project/e/<int:id>/team/', p.project_team_edit, name='project_team_edit'),
    path('project/v/<int:id>/team/', p.project_team_view, name='project_team_view'),
    path('project/v/<int:id>/team/add/', p.project_team_view, name='project_team_add'),
    path('project/v/<int:id>/', p.project_view, name='project_view'),
    path('project/e/<int:id>/', p.project_view_or_edit, name='project_edit'),
    path('project/r/<int:id>/', p.project_request, name='project_request'),
    path('project/d/<int:id>/', p.project_delete, name='project_delete'),
    path('project/ur/<int:id>', p.projects_undo_request, name='project_request_undo'),
    path('project/accept/', p.projects_accept_request, name='project_request_accept'),
    path('project/decline/', p.projects_decline_request, name='project_request_decline'),
    path('list_skills/', apps.main.views.json_skills),
    path('search/', apps.main.views.search_engine),
    path('oauth/', include('social_django.urls', namespace='social')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
