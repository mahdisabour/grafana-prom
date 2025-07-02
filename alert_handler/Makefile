NAME := app
IMAGE := alert-handler
CONTAINER := alert-handler-container
REDIS_CONTAINER := redis_container
POETRY := $(shell command -v poetry 2> /dev/null)
DOCKER := $(shell command -v docker 2> /dev/null)


install:
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) init
	$(POETRY) install

.PHONY: ci
ci:
	pre-commit run --all-files

.PHONY: build
build:
	$(POETRY) export --without-hashes --without dev -f requirements.txt -o requirements.txt
	$(DOCKER) build -t $(IMAGE) -f Dockerfile .

.PHONY: run
run:
	$(DOCKER) run --rm -p 8000:8000 -p 2001:2001/udp --name $(CONTAINER) $(IMAGE)