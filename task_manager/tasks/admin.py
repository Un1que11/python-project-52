from django.contrib import admin
from django.db.models.base import Model
from typing import Union, Sequence, Callable, TypeVar, Any

from .models import Task


_ModelT = TypeVar("_ModelT", bound=Model)


class TaskAdmin(admin.ModelAdmin):
    list_display: Sequence[Union[str, Callable[[_ModelT], Any]]] = \
        ('id', 'name', 'status', 'author', 'executor', 'date_created', 'date_modified')


admin.site.register(Task, TaskAdmin)
