from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
from .constants import USERNAME, FIRST_NAME, LAST_NAME, EMAIL, \
    FIRST_NAME_LABEL, LAST_NAME_LABEL, EMAIL_LABEL, \
    FIRST_NAME_HELP_TEXT, LAST_NAME_HELP_TEXT


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True, label=FIRST_NAME_LABEL, help_text=FIRST_NAME_HELP_TEXT
    )
    last_name = forms.CharField(
        required=True, label=LAST_NAME_LABEL, help_text=LAST_NAME_HELP_TEXT
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (USERNAME, FIRST_NAME, LAST_NAME)


class UserEditingForm(UserRegistrationForm):
    email = forms.EmailField(label=EMAIL_LABEL, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (USERNAME, FIRST_NAME, LAST_NAME, EMAIL)
