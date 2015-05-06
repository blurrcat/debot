.PHONY: clean-pyc clean-build docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "config - install config and scripts in virtualenv"
	@echo "coverage - run coverage test"
	@echo "lint - check style with pylint"
	@echo "test - run tests"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

config: clean
	pip install -r requirements.txt
	pip install -e .

config-test: config
	pip install -r requirements-test.txt

config-dev: config-test
	pip install -r requirements-dev.txt

lint:
	pylint --rcfile=.pylint.rc debot tests

test:
	py.test -v --cov-report term --cov debot tests

coverage:
	py.test -v --cov-report html --cov debot tests
	open htmlcov/index.html

docs:
	rm -f docs/debot.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ debot
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	@echo "open docs/_build/html/index.html"

release: clean docs test
	python setup.py sdist upload

sdist: clean docs test
	python setup.py sdist
	ls -l dist

build: clean
	docker build -t debot .
