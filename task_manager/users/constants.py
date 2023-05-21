"Constants for Users application."

from django.utils.translation import gettext_lazy
from django.urls import reverse_lazy
from typing import Dict, Final

from task_manager.constants import LOGIN


# Route names
CREATE_USER: Final[str] = 'sign_up'
LIST_USERS: Final[str] = 'users'
UPDATE_USER: Final[str] = 'user_update'
DELETE_USER: Final[str] = 'user_delete'


# Reverses
REVERSE_USERS: Final = reverse_lazy(LIST_USERS)
REVERSE_CREATE: Final = reverse_lazy(CREATE_USER)
REVERSE_LOGIN: Final = reverse_lazy(LOGIN)


# Templates
# All are default!
TEMPLATE_CREATE: Final[str] = 'users/user_form.html'
TEMPLATE_LIST: Final[str] = 'users/user_list.html'
TEMPLATE_UPDATE: Final[str] = 'users/user_form.html'
TEMPLATE_DELETE: Final[str] = 'users/user_confirm_delete.html'


# Context Fields
PAGE_TITLE: Final[str] = 'page_title'
PAGE_DESCRIPTION: Final[str] = 'page_description'
PAGE_H1: Final[str] = 'page_h1'
BUTTON_TEXT: Final[str] = 'button_text'


# Meta
# route: /
LIST_TITLE: str = gettext_lazy('Users')
LIST_DESCRIPTION: str = gettext_lazy('List of Task Manager Users.')
LIST_H1: str = gettext_lazy('Users')
# route: /create
CREATE_TITLE: str = gettext_lazy('Registration')
CREATE_DESCRIPTION: str = gettext_lazy('User Registration on Task Manager.')
CREATE_H1: str = gettext_lazy('Registration')
# route: /<int:pk>/update/
UPDATE_TITLE: str = gettext_lazy('User editing')
UPDATE_DESCRIPTION: str = gettext_lazy('User editing on Task Manager.')
UPDATE_H1: str = gettext_lazy('User change')
# route: /<int:pk>/delete/
DELETE_TITLE: str = gettext_lazy('User deleting')
DELETE_DESCRIPTION: str = gettext_lazy('User deleting on Task Manager.')
DELETE_H1: str = gettext_lazy('Deleting a user')


# Messages
MSG_REGISTERED: str = gettext_lazy('User successfully registered')
MSG_UPDATED: str = gettext_lazy('User successfully updated')
MSG_DELETED: str = gettext_lazy('User successfully deleted')
MSG_UNPERMISSION_TO_MODIFY: str = gettext_lazy('You do not have permission to modify another user')
USER_USED_IN_TASK: str = gettext_lazy('Cannot delete user because it is in use')


# Forms
# Fields
USERNAME: Final[str] = 'username'
FIRST_NAME: Final[str] = 'first_name'
LAST_NAME: Final[str] = 'last_name'
EMAIL: Final[str] = 'email'
PASSWORD1: Final[str] = 'password1'
PASSWORD2: Final[str] = 'password2'
# Labels
FIRST_NAME_LABEL: str = gettext_lazy('First Name')
LAST_NAME_LABEL: str = gettext_lazy('Last Name')
EMAIL_LABEL: str = 'Email'
# Help texts
FIRST_NAME_HELP_TEXT: str = gettext_lazy('Required. Please enter your real name.')
LAST_NAME_HELP_TEXT: str = gettext_lazy('Required. Please enter your real surname.')


# Buttons
REGISTER_BUTTON: str = gettext_lazy('Register')
UPDATE_BUTTON: str = gettext_lazy('Change')
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
    BUTTON_TEXT: REGISTER_BUTTON
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
