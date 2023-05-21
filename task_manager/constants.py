"Constants for Task Manager main application."

from django.utils.translation import gettext_lazy
from django.urls import reverse_lazy
from typing import Final


# Route names
HOME: Final[str] = 'home'
LOGIN: Final[str] = 'login'
LOGOUT: Final[str] = 'logout'


# Reverses
REVERSE_HOME: Final = reverse_lazy(HOME)
REVERSE_LOGIN: Final = reverse_lazy(LOGIN)
REVERSE_LOGOUT: Final = reverse_lazy(LOGOUT)


# Messages
MSG_LOGIN: str = gettext_lazy('You are logged in')
MSG_LOGOUT: str = gettext_lazy('You are logged out')

MSG_NO_PERMISSION = gettext_lazy('You are not authorized! Please sign in.')
MSG_NOT_AUTHOR_FOR_DELETE_TASK = gettext_lazy("A task can only be deleted by its author.")


# Templates
TEMPLATE_INDEX: Final[str] = 'index.html'
