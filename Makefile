install:
		poetry install

build:
		poetry build

lint:
		poetry run flake8 task_manager

reinstall:
		pip install --user --force-reinstall dist/*.whl

test:
		poetry run pytest -v

coverage:
		poetry run pytest --cov=task_manager

dev:
		poetry run python manage.py runserver

start:
		poetry run gunicorn task_manager.wsgi