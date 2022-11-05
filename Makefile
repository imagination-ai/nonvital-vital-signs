.PHONY: install install-dev install-test build-*

ENV ?= .venv
RUN = . $(ENV)/bin/activate &&
GCS_BUCKET = test-bucket

.venv:
	virtualenv $(ENV) --python=python3.8
	touch $@

install: .venv requirements.txt
	$(RUN) pip install -r requirements.txt

install-dev: install-test
	# prep for fake gcs
	# fake buckets
	#mkdir -p fake-gcs/$(GCS_BUCKET)
	#touch fake-gcs/$(GCS_BUCKET)/fake-data.txt

	$(RUN) pre-commit install && pre-commit install -t pre-push
	#brew install httpie

install-test: install
	$(RUN) pip install -r requirements-test.txt

clean:
	rm -rf $(ENV)

test:
	export ENVIRONMENT=test
	PYTHONPATH=$(PWD)/src pytest tests

format:
	 $(RUN) black -t py39 -l 80 $$(find src/* -name "*.py")

steel-thread:
	echo "no steel-thread yet"

e2e-test:
	bash e2e/e2e-signs.sh
