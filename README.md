# Task Manager
___

The training project "Task Manager" on the Python Development course on [Hexlet.io](https://ru.hexlet.io/programs/python).

[![Actions Status](https://github.com/Un1que11/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/Un1que11/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/efa05876d1635d2f3e0d/maintainability)](https://codeclimate.com/github/Un1que11/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/efa05876d1635d2f3e0d/test_coverage)](https://codeclimate.com/github/Un1que11/python-project-52/test_coverage)
[![tests](https://github.com/Un1que11/python-project-52/actions/workflows/test-checker.yml/badge.svg?branch=main)](https://github.com/IgorGakhov/python-project-52/actions/workflows/test-checker.yml)

### Dependencies
List of dependencies, without which the project code will not work correctly:
- python = "^3.8"
- python-dotenv = "^0.21.0"
- Django = "^4.1.3"
- django-bootstrap4 = "^22.2"
- django-filter = "^22.1"
- dj-database-url = "0.5.0"
- gunicorn = "^20.1.0"
- psycopg2-binary = "^2.9.5"
- whitenoise = "^6.2.0"
- rollbar = "^0.16.3"

## Description
**Task Manager** is a task management system. It allows you to set tasks, assign performers and change their statuses. Registration and authentication are required to work with the system.

### Summary
* [Description](#description)
* [Installation for contributors](#installation-for-contributors)
* [Usage](#usage)
* [Development](#development)
  * [Dev Dependencies](#dev-dependencies)
  * [Project Organization](#project-organization)
  * [Useful commands](#useful-commands)


___

## Installation for contributors

To install, you must first install the following software:
| Tool | Description |
|----------|---------|
| [Python](https://www.python.org/downloads/) |  Programming language |
| [Poetry](https://python-poetry.org/) |  Python dependency manager |

```Bash
# clone via HTTPS:
$ git clone https://github.com/Un1que11/python-project-52.git
# or clone via SSH:
$ git clone git@github.com:Un1que11/python-project-52.git
$ cd python-project-52
$ make install
$ touch .env
You have to write into .env file SECRET_KEY for Django app and token for Rollbar. See .env.example.
To get SECRET_KEY for Django app:
$ python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> get_random_secret_key()
Then add new SECRET_KEY to .env file
$ make migrate
$ make dev-start
```


___

## Usage
Here are some hints for using the app.
| Steps        | Description                                                                                                                                                               |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Registration | First you need to register in the app using the provided form of registration.                                                                                            |
| Log in       | Then you have to log in using the information you've filled in the registration form.                                                                                     |
| User         | You can see all users on the relevant page. You can change the information only about yourself. If the user is an author or an executor of the task he cannot be deleted. |
| Statuses     | You can add, update, delete statuses of the tasks, if you are logged in. The statuses which correspond with any tasks cannot be deleted.                                  |
| Labels       | You can add, update, delete labels of the tasks, if you are logged in. The label which correspond with any tasks cannot be deleted.                                       |
| Tasks        | You can add, update, delete tasks, if you are logged in. You can also filter tasks on the relevant page with given statuses, exetutors and labels.                        |


___

## Development

### Dev Dependencies

List of dev-dependencies:
- flake8 = "^5.0.4"
- coverage = "^6.5.0"

### Project Organization

```bash
>> tree .
```
```bash
.
├── README.md
├── pyproject.toml
├── poetry.lock
├── Makefile
├── Procfile
├── requirements.txt
├── runtime.txt
├── setup.cfg
├── coverage.xml
├── staticfiles
├── manage.py
├── locale
│   └── ru
│       └── LC_MESSAGES
│           ├── django.mo
│           └── django.po
└── task_manager
    ├── __init__.py
    ├── wsgi.py
    ├── asgi.py
    ├── constants.py
    ├── urls.py
    ├── views.py
    ├── mixins.py
    ├── settings.py
    ├── templates
    │   ├── index.html
    │   ├── registration
    │   │   └── login.html
    │   └── components
    │       ├── base.html
    │       ├── footer.html
    │       ├── form.html
    │       └── navbar.html
    ├── users
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── constants.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── migrations
    │   └── templates
    │       └── users
    │           ├── user_confirm_delete.html
    │           ├── user_form.html
    │           └── user_list.html
    ├── labels
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── constants.py
    │   ├── models.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── migrations
    │   └── templates
    │       └── labels
    │           ├── label_confirm_delete.html
    │           ├── label_form.html
    │           └── label_list.html
    ├── statuses
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── constants.py
    │   ├── models.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── migrations
    │   └── templates
    │       └── statuses
    │           ├── status_confirm_delete.html
    │           ├── status_form.html
    │           └── status_list.html
    ├── tasks
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── constants.py
    │   ├── filters.py
    │   ├── models.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── migrations
    │   └── templates
    │       └── tasks
    │           ├── task_confirm_delete.html
    │           ├── task_detail.html
    │           ├── task_filter.html
    │           └── task_form.html
    └── tests
        ├── fixtures
        │   ├── label.json
        │   ├── status.json
        │   ├── task.json
        │   └── user.json
        ├── test_labels.py
        ├── test_statuses.py
        ├── test_task_manager.py
        ├── test_tasks.py
        └── test_users.py
```

### Useful commands

The commands most used in development are listed in the Makefile:

<dl>
    <dt><code>make package-install</code></dt>
    <dd>Installing a package in the user environment.</dd>
    <dt><code>make build</code></dt>
    <dd>Building the distribution of he Poetry package.</dd>
    <dt><code>make package-force-reinstall</code></dt>
    <dd>Reinstalling the package in the user environment.</dd>
    <dt><code>make lint</code></dt>
    <dd>Checking code with linter.</dd>
    <dt><code>make test</code></dt>
    <dd>Tests the code.</dd>
    <dt><code>make fast-check</code></dt>
    <dd>Builds the distribution, reinstalls it in the user's environment, checks the code with tests and linter.</dd>
    <dt><code>make dev-start</code></dt>
    <dd>Starts the server on localhost (at IP address 127.0.0.1 with port 8000 by default).</dd>
</dl>

___

**Thank you for attention!**

:man_technologist: Author: [@Un1que11](https://github.com/Un1que11)
