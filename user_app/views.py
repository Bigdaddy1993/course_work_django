import random
import string

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView

from user_app.forms import UserRegisterForm, UserProfileForm, RestoreUserForm
from user_app.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user_app/register.html'
    success_url = reverse_lazy('user_app:login')

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_active = False
        secrets_token = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        new_user.token = secrets_token
        message = f'Для подтверждения вашего Е-mail перейдите по ссылке http://127.0.0.1:8000/user_app/verify/?token={secrets_token}'
        send_mail(
            subject='Вы зарегистрированы на нашей платформе',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


def activate_user(request):
    key = request.GET.get('token')
    current_user = User.objects.filter(is_active=False)
    for user in current_user:
        if str(user.token) == str(key):
            user.is_active = True
            user.token = None
            user.save()
    response = redirect(reverse_lazy('user_app:login'))
    return response


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('user_app:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('user_app:profile')
    form_class = UserProfileForm
    template_name = 'user_app/profile.html'
    permission_required = 'user_app.set_is_active'

    def get_object(self, queryset=None):
        return self.request.user


def generate_password():
    length = 10
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


class RestoreUser(FormView):
    template_name = 'user_app/generate_password.html'
    form_class = RestoreUserForm
    success_url = reverse_lazy('user_app:login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        new_password = generate_password()
        user.password = make_password(new_password)
        user.save()
        send_mail(
            subject='Смена пароля',
            message=f'У Вашего аккаунта новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )
        return super().form_valid(form)


@login_required
@permission_required(['user_app.view_user', 'user_app.set_is_active'])
def get_user_list(request):
    user_list = User.objects.all()
    context = {
        'object_list': user_list,
        'title': 'Список пользователей'
    }
    return render(request, 'user_app/user_app_list.html', context)
