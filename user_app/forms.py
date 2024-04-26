from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm

from client.forms import StyleFormMixin
from user_app.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'country', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class RestoreUserForm(StyleFormMixin, PasswordResetForm):
    class Meta:
        model = User
        fields = ('email',)
