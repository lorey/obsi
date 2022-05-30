.RECIPEPREFIX = >

.PHONY: all test format build up run precommit example
.FORCE:

all: build up run

run:
> docker-compose exec -T app python cli.py run
> docker-compose exec -T app python cli.py anki-deck

test:
> docker-compose exec -T app python -m pytest

coverage: test
> docker-compose exec -T app python -Bm pytest -p no:cacheprovider --cov=. --cov-report html:.coverage-report
> xdg-open .coverage-report/index.html

format:
> docker-compose exec -T app isort --profile=black .
> docker-compose exec -T app black .
> sudo chown -R $(USER) obsi
> sudo chown -R $(USER) tests
> sudo chown -R $(USER) *.py

lint:
> docker-compose exec -T app flake8 --ignore=E501,W503 .
> @docker-compose exec -T app pylint obsi || true

build: requirements.txt
> docker-compose build --build-arg USER_ID=$$(id -u) --build-arg GROUP_ID=$$(id -g)

# update requirements
requirements.txt: requirements.in
> docker-compose exec -T app pip-compile --upgrade
> sudo chown $(USER) requirements.txt

up:
> docker-compose up -d

example:
> sudo rm -rf example/output/*
> make run

precommit: build up test format lint
