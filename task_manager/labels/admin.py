from django.contrib import admin
from django.db.models.base import Model
from typing import Union, Sequence, Callable, TypeVar, Any

from .models import Label


_ModelT = TypeVar("_ModelT", bound=Model)


class LabelAdmin(admin.ModelAdmin):
    list_display: Sequence[Union[str, Callable[[_ModelT], Any]]] = \
        ('id', 'name', 'date_created', 'date_modified')


admin.site.register(Label, LabelAdmin)
