"Constants for Labels application."

from django.utils.translation import gettext_lazy
from django.urls import reverse_lazy
from typing import Dict, Final

from task_manager.constants import REVERSE_LOGIN, MSG_NO_PERMISSION  # noqa: F401


# Route names
LIST_LABELS: Final[str] = 'labels'
CREATE_LABEL: Final[str] = 'label_create'
UPDATE_LABEL: Final[str] = 'label_update'
DELETE_LABEL: Final[str] = 'label_delete'


# Reverses
REVERSE_LABELS: Final = reverse_lazy(LIST_LABELS)
REVERSE_CREATE: Final = reverse_lazy(CREATE_LABEL)


# Templates
# All are default!
TEMPLATE_LIST: Final[str] = 'labels/label_list.html'
TEMPLATE_CREATE: Final[str] = 'labels/label_form.html'
TEMPLATE_UPDATE: Final[str] = 'labels/label_form.html'
TEMPLATE_DELETE: Final[str] = 'labels/label_confirm_delete.html'


# Context Fields
PAGE_TITLE: Final[str] = 'page_title'
PAGE_DESCRIPTION: Final[str] = 'page_description'
PAGE_H1: Final[str] = 'page_h1'
BUTTON_TEXT: Final[str] = 'button_text'


# Meta
# route: /
LIST_TITLE: str = gettext_lazy('Labels')
LIST_DESCRIPTION: str = gettext_lazy('List of Task Manager Labels.')
LIST_H1: str = gettext_lazy('Labels')
# route: /create
CREATE_TITLE: str = gettext_lazy('Label creation')
CREATE_DESCRIPTION: str = gettext_lazy('Label Creation on Task Manager.')
CREATE_H1: str = gettext_lazy('Create label')
# route: /<int:pk>/update/
UPDATE_TITLE: str = gettext_lazy('Label editing')
UPDATE_DESCRIPTION: str = gettext_lazy('Label editing on Task Manager.')
UPDATE_H1: str = gettext_lazy('Change label')
# route: /<int:pk>/delete/
DELETE_TITLE: str = gettext_lazy('Label deleting')
DELETE_DESCRIPTION: str = gettext_lazy('Label deleting on Task Manager.')
DELETE_H1: str = gettext_lazy('Delete label')


# Messages
MSG_CREATED: str = gettext_lazy('Label created successfully')
MSG_UPDATED: str = gettext_lazy('Label changed successfully')
MSG_DELETED: str = gettext_lazy('Label deleted successfully')
LABEL_USED_IN_TASK: str = gettext_lazy('Can\'t delete label because it\'s in use')


# Forms
# Fields
NAME: Final[str] = 'name'


# Buttons
CREATION_BUTTON: str = gettext_lazy('Create')
UPDATE_BUTTON: str = gettext_lazy('Update')
DELETE_BUTTON: str = gettext_lazy('Yes, delete')


# Contexts
CONTEXT_LIST: Dict = {
    PAGE_TITLE: LIST_TITLE,
    PAGE_DESCRIPTION: LIST_DESCRIPTION,
    PAGE_H1: LIST_H1
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
