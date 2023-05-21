"Constants for Tasks application."

from django.utils.translation import gettext_lazy
from django.urls import reverse_lazy
from typing import Dict, Final

from task_manager.constants import \
    REVERSE_LOGIN, MSG_NO_PERMISSION, MSG_NOT_AUTHOR_FOR_DELETE_TASK  # noqa: F401


# Route names
LIST_TASKS: Final[str] = 'tasks'
CREATE_TASK: Final[str] = 'task_create'
UPDATE_TASK: Final[str] = 'task_update'
DELETE_TASK: Final[str] = 'task_delete'
DETAIL_TASK: Final[str] = 'task_detail'


# Reverses
REVERSE_TASKS: Final = reverse_lazy(LIST_TASKS)
REVERSE_CREATE: Final = reverse_lazy(CREATE_TASK)


# Templates
# All are default!
TEMPLATE_LIST: Final[str] = 'tasks/task_filter.html'
TEMPLATE_CREATE: Final[str] = 'tasks/task_form.html'
TEMPLATE_UPDATE: Final[str] = 'tasks/task_form.html'
TEMPLATE_DELETE: Final[str] = 'tasks/task_confirm_delete.html'
TEMPLATE_DETAIL: Final[str] = 'tasks/task_detail.html'


# Context Fields
PAGE_TITLE: Final[str] = 'page_title'
PAGE_DESCRIPTION: Final[str] = 'page_description'
PAGE_H1: Final[str] = 'page_h1'
BUTTON_TEXT: Final[str] = 'button_text'


# Meta
# route: /
LIST_TITLE: str = gettext_lazy('Tasks')
LIST_DESCRIPTION: str = gettext_lazy('List of Task Manager Tasks.')
LIST_H1: str = gettext_lazy('Tasks')
# route: /create
CREATE_TITLE: str = gettext_lazy('Task creation')
CREATE_DESCRIPTION: str = gettext_lazy('Task Creation on Task Manager.')
CREATE_H1: str = gettext_lazy('Create task')
# route: /<int:pk>
DETAIL_TITLE: str = gettext_lazy('Task view')
DETAIL_DESCRIPTION: str = gettext_lazy('Task detail view on Task Manager.')
DETAIL_H1: str = gettext_lazy('Task view')
# route: /<int:pk>/update/
UPDATE_TITLE: str = gettext_lazy('Task editing')
UPDATE_DESCRIPTION: str = gettext_lazy('Task editing on Task Manager.')
UPDATE_H1: str = gettext_lazy('Change task')
# route: /<int:pk>/delete/
DELETE_TITLE: str = gettext_lazy('Task deleting')
DELETE_DESCRIPTION: str = gettext_lazy('Task deleting on Task Manager.')
DELETE_H1: str = gettext_lazy('Delete task')


# Messages
MSG_CREATED: str = gettext_lazy('Task created successfully')
MSG_UPDATED: str = gettext_lazy('Task changed successfully')
MSG_DELETED: str = gettext_lazy('Task deleted successfully')


# Forms
# Fields
NAME: Final[str] = 'name'
STATUS: Final[str] = 'status'
DESCRIPTION: Final[str] = 'description'
EXECUTOR: Final[str] = 'executor'
LABELS: Final[str] = 'labels'


# Buttons
CREATION_BUTTON: str = gettext_lazy('Create')
UPDATE_BUTTON: str = gettext_lazy('Update')
DELETE_BUTTON: str = gettext_lazy('Yes, delete')
FILTER_BUTTON: str = gettext_lazy('Search')


# Contexts
CONTEXT_LIST: Dict = {
    PAGE_TITLE: LIST_TITLE,
    PAGE_DESCRIPTION: LIST_DESCRIPTION,
    PAGE_H1: LIST_H1,
    BUTTON_TEXT: FILTER_BUTTON
}
CONTEXT_CREATE: Dict = {
    PAGE_TITLE: CREATE_TITLE,
    PAGE_DESCRIPTION: CREATE_DESCRIPTION,
    PAGE_H1: CREATE_H1,
    BUTTON_TEXT: CREATION_BUTTON
}
CONTEXT_UPDATE: Dict = {
    PAGE_TITLE: UPDATE_TITLE,
    PAGE_DESCRIPTION: UPDATE_DESCRIPTION,
    PAGE_H1: UPDATE_H1,
    BUTTON_TEXT: UPDATE_BUTTON
}
CONTEXT_DELETE: Dict = {
    PAGE_TITLE: DELETE_TITLE,
    PAGE_DESCRIPTION: DELETE_DESCRIPTION,
    PAGE_H1: DELETE_H1,
    BUTTON_TEXT: DELETE_BUTTON
}
CONTEXT_DETAIL: Dict = {
    PAGE_TITLE: DETAIL_TITLE,
    PAGE_DESCRIPTION: DETAIL_DESCRIPTION,
    PAGE_H1: DETAIL_H1
}
