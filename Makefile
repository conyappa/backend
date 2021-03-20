localsettings:
	cp conyappa/main/local_settings.example.py conyappa/main/local_settings.py

createvenv:
	python3 -m venv .venv
	poetry run pip3 install --upgrade pip
	poetry run poetry install

makemigrations:
	docker-compose run web python manage.py makemigrations

migrate:
	docker-compose run web python manage.py migrate

shell:
	docker-compose run web python manage.py shell_plus

test:
	docker-compose run web python manage.py test

format:
	poetry run black conyappa
	poetry run isort conyappa
