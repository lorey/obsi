.RECIPEPREFIX = >

.PHONY: all test format build up run precommit
.FORCE:

all: test format precommit

run:
> docker-compose exec app python cli.py run

test:
> docker-compose exec app python -m pytest

coverage: test
> docker-compose exec app python -Bm pytest -p no:cacheprovider --cov=. --cov-report html:.coverage-report
> xdg-open .coverage-report/index.html

format:
> docker-compose exec app isort --profile=black .
> docker-compose exec app black .
> sudo chown -R $(USER) obsi
> sudo chown -R $(USER) tests
> sudo chown -R $(USER) *.py

lint:
> docker-compose exec app flake8 --ignore=E501,W503 .
> @docker-compose exec app pylint obsi || true

build: requirements.txt
> docker-compose build

# update requirements
requirements.txt: requirements.in
> docker-compose exec app pip-compile --upgrade
> sudo chown $(USER) requirements.txt

up:
> docker-compose up -d

precommit: build up test format lint
