from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user_app.apps import UsersConfig
from user_app.views import RegisterView, ProfileView, activate_user, RestoreUser

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='user_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify/', activate_user),
    path('generate_password/', RestoreUser.as_view(), name='generate_password'),
]
