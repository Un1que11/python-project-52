from django.contrib import admin
from django.db.models.base import Model
from typing import Union, Sequence, Callable, TypeVar, Any

from .models import Status


_ModelT = TypeVar("_ModelT", bound=Model)


class StatusAdmin(admin.ModelAdmin):
    list_display: Sequence[Union[str, Callable[[_ModelT], Any]]] = \
        ('id', 'name', 'date_created', 'date_modified')


admin.site.register(Status, StatusAdmin)
