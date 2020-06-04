.PHONY: default install wheel dev test coverage  black-check black-diff safety tag

guard-%:
	@ if [ "${${*}}" = "" ]; then echo "Run 'pipenv shell' before command"; exit 1; fi

default: test

install: guard-PIPENV_ACTIVE
	pip install -e .

wheel: guard-PIPENV_ACTIVE coverage black-check safety
	python setup.py bdist_wheel

dev: guard-PIPENV_ACTIVE
	pipenv install --dev --skip-lock

test: guard-PIPENV_ACTIVE
	PYTHONPATH=./src pytest

coverage: guard-PIPENV_ACTIVE
	PYTHONPATH=./src pytest --cov-report term --cov=./src/sps ./tests --cov-report term-missing

black-check: guard-PIPENV_ACTIVE
	black --check src/ tests/

black-diff: guard-PIPENV_ACTIVE
	black --diff src/ tests/

safety: guard-PIPENV_ACTIVE
	pip freeze | safety check --stdin

tag: guard-PIPENV_ACTIVE wheel
	@bash tag.sh
