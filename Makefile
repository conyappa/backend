# Environment stuff
.PHONY: get-poetry
get-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

.PHONY: createvenv
createvenv:
	python3 -m venv .venv
	poetry run pip3 install --upgrade pip
	poetry run poetry install

.PHONY: localsettings
localsettings:
	cp conyappa/main/local_settings.example.py conyappa/main/local_settings.py


# Linters
.PHONY: black
black:
	poetry run black conyappa --check

.PHONY: black!
black!:
	poetry run black conyappa

.PHONY: flake8
flake8:
	poetry run flake8 conyappa

.PHONY: isort
isort:
	poetry run isort conyappa --check

.PHONY: isort!
isort!:
	poetry run isort conyappa

.PHONY: format!
format!: black! isort!


# Builders
.PHONY: build
build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose build --parallel


# Application interactions
.PHONY: tests
tests:
	docker-compose run web python manage.py test


.PHONY: shell
shell:
	docker-compose run web python manage.py shell_plus --plain


.PHONY: ipython
ipython:
	docker-compose run web python manage.py shell_plus --ipython


# Database interactions
.PHONY: migrate
migrate:
	docker-compose run web python manage.py migrate


.PHONY: makemigrations
makemigrations:
	docker-compose run web python manage.py makemigrations
