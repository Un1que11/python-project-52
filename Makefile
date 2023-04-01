install:
		poetry install

build:
		poetry build

lint:
		poetry run flake8 task_manager

reinstall:
		pip install --user --force-reinstall dist/*.whl

dev:
		poetry run python manage.py runserver

start: migrate
		poetry run gunicorn task_manager.wsgi

migrate:
		poetry run python manage.py migrate

make-migrations:
		poetry run python manage.py makemigrations

shell:
		poetry run python manage.py shell

update-locales:
		django-admin makemessages -l ru

compile-locales:
		django-admin compilemessages

test:
		poetry run python manage.py test

test-coverage:
		poetry run coverage run --source='.' manage.py test task_manager
		poetry run coverage xml
		poetry run coverage report
