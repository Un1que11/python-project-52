from django.contrib import admin
from django.db.models.base import Model
from typing import Union, Sequence, Callable, TypeVar, Any

from .models import User


_ModelT = TypeVar("_ModelT", bound=Model)


class UsersAdmin(admin.ModelAdmin):
    list_display: Sequence[Union[str, Callable[[_ModelT], Any]]] = \
        ['id', 'username', 'first_name', 'last_name', 'email']


admin.site.register(User, UsersAdmin)
