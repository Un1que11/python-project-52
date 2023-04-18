from django.forms import ModelForm

from .models import Status


class NewStatusCreationForm(ModelForm):

    class Meta:
        model = Status
        fields = ['name']
