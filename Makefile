install:
	poetry install
	poetry run python manage.py migrate

migrate:
	poetry run python3 manage.py migrate

collectstatic:
	poetry run python3 manage.py collectstatic

build: install migrate collectstatic

run-server:
	 python manage.py runserver

dev:
	poetry run python3 manage.py runserver


test:
	poetry run python manage.py test task_manager.apps.statuses
	poetry run python manage.py test task_manager.apps.users
	poetry run python manage.py test task_manager.apps.labels
	poetry run python manage.py test task_manager.apps.tasks

test-cov:
	poetry run coverage run manage.py test
	poetry run coverage xml

dev-cov:
	poetry run coverage run manage.py test
	poetry run coverage report -m

makemessages:
	poetry run python3 manage.py makemessages -a

compilemessages:
	poetry run python3 manage.py compilemessages

lint:
	poetry run flake8 task_manager --exclude=migrations,settings.py,admin.py