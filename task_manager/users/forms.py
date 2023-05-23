from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True, label=_('First Name'), help_text=_('Required. Please enter your real name.')
    )
    last_name = forms.CharField(
            required=True, label=_('Last Name'), help_text=_('Required. Please enter your real surname.')  # noqa: E501
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name')


class UserEditingForm(UserRegistrationForm):
    email = forms.EmailField(label='Email', required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
