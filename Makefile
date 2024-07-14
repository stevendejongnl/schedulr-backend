.PHONY: version image flake mypy test pre-commit

version:
	echo "VERSION = \"$$(git describe --tags --match 'v[0-9]*' --abbrev=0 || echo 'v0.0.0')\"" > schedulr/version.py

version-ci:
	echo "VERSION = \"$$(NEW_VERSION)\"" > schedulr/version.py

image: version
	docker build -t stevendejong/schedulr-backend .

flake:
	docker run --rm -v $(CURDIR):/srv -w /srv stevendejong/schedulr-backend flake8

flake-ci: image flake

mypy:
	docker run --rm -v $(CURDIR):/srv -w /srv stevendejong/schedulr-backend mypy --config-file mypy.ini .

mypy-ci: image mypy

lint: flake mypy

test:
	docker run --rm -v $(CURDIR):/srv -w /srv stevendejong/schedulr-backend pytest

test-ci: image test

pre-commit:
	./scripts/pre-commit.sh run --all-files
