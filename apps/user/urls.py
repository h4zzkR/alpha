from django.urls import path, include
import apps.user.views as u


urlpatterns = [
    path('register/', u.RegisterFormView.as_view(), name="user_register"),
    path('login/', u.LoginFormView.as_view(), name="user_login"),
    path('logout/', u.LogoutView.as_view(), name="user_logout"),
    # path('u/<str:username>', u.UserUpdate.as_view(), name="user_profile"),
    path('u/<str:username>', u.get_user, name="user_profile"),
]