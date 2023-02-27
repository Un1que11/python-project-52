from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django import forms

from task_manager.users.models import User


class NewUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        help_text=_('<ul><li>'
                    'Your password must contain at least 3 characters.'
                    '</li></ul>'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')
