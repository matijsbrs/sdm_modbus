all: lint

.PHONY: lint
lint:
	flake8 --ignore=E501,W503

.PHONY: test
test:
	poetry run tox

.PHONY: release
release:
	poetry build
	python3 -m twine upload dist/*

.PHONY: clean
clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	rm -rf build
	rm -rf dist
	rm -rf src/*.egg-info
