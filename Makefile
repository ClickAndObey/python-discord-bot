all: clean lint test

MAJOR_VERSION := 1
MINOR_VERSION := 0
BUILD_VERSION ?= $(USER)
VERSION := $(MAJOR_VERSION).$(MINOR_VERSION).$(BUILD_VERSION)

ORGANIZATION := clickandobey
SERVICE_NAME := python-discord-bot

PACKAGE_IMAGE_NAME := ${ORGANIZATION}-${SERVICE_NAME}-package

APP_IMAGE_NAME := ${ORGANIZATION}-${SERVICE_NAME}-app
GITHUB_REPO := "ghcr.io"
APP_REPO_IMAGE_NAME := ${GITHUB_REPO}/${ORGANIZATION}/${SERVICE_NAME}:${VERSION}
APP_CONTAINER_NAME := ${APP_IMAGE_NAME}

ROOT_DIRECTORY := `pwd`
MAIN_PATH := ${ROOT_DIRECTORY}/src/main
PYTHON_PATH := ${MAIN_PATH}/python
SCRIPTS_PATH := ${MAIN_PATH}/scripts
COMMANDS_YAML_DIRECTORY := ${MAIN_PATH}/commands

ifneq ($(DEBUG),)
  INTERACTIVE=--interactive
  PDB=--pdb
  DETACH=--env "DETACH=None"
else
  INTERACTIVE=--env "INTERACTIVE=None"
  PDB=
  DETACH=--detach
endif

# Code Packaging Targets

package: $(shell find src/main/python -name "*") docker/Dockerfile.package
	@docker build \
		-t ${PACKAGE_IMAGE_NAME} \
		-f docker/Dockerfile.package \
		.
	@docker run \
		--rm \
		--env VERSION=$(VERSION) \
		-v ${ROOT_DIRECTORY}/dist:/python/dist \
		${PACKAGE_IMAGE_NAME}
	@touch package

# Local App Targets

run-bot:
	@export PYTHONPATH=${PYTHON_PATH}; \
	export COMMANDS_YAML_DIRECTORY=${COMMANDS_YAML_DIRECTORY}; \
	export DISCORD_TOKEN=${DISCORD_TOKEN}; \
	cd ${PYTHON_PATH}; \
	pipenv run python ../scripts/run_bot --debug

# Docker App Targets

docker-build-app: package docker/Dockerfile.app
	@docker build \
		-t ${APP_IMAGE_NAME} \
		-f docker/Dockerfile.app \
		--build-arg VERSION=${VERSION} \
		.
	@touch docker-build-app

docker-run-bot: docker-build-app stop-bot
	@docker run \
		--rm \
		${DETACH} \
		${INTERACTIVE} \
		--env DISCORD_TOKEN=${DISCORD_TOKEN} \
		--name ${APP_CONTAINER_NAME} \
		${APP_IMAGE_NAME}

stop-bot:
	@docker kill ${APP_CONTAINER_NAME} || true

# Testing

test: unit-test integration-test
test-docker: unit-test-docker integration-test-docker

unit-test:
	@echo TODO Implement Me!

unit-test-docker:
	@echo TODO Implement Me!

integration-test:
	@echo TODO Implement Me!

integration-test-docker:
	@echo TODO Implement Me!

# Release

release: docker-build-app github-docker-login
	@echo Tagging webservice image to ${APP_REPO_IMAGE_NAME}...
	@docker tag ${APP_IMAGE_NAME} ${APP_REPO_IMAGE_NAME}
	@echo Pushing webservice docker image to ${APP_REPO_IMAGE_NAME}...
	@docker push ${APP_REPO_IMAGE_NAME}

# Linting

lint: lint-markdown lint-python

lint-markdown:
	@echo Linting markdown files...
	@docker run \
		--rm \
		-v `pwd`:/workspace \
		wpengine/mdl \
			/workspace
	@echo Markdown linting complete.

lint-python:
	@echo Linting Python files...
	@docker build \
		-t ${SERVICE_NAME}/pylint \
		-f docker/Dockerfile.pylint \
		.
	@docker run --rm \
		${SERVICE_NAME}/pylint \
			pylint \
				--rcfile /workspace/.pylintrc \
				/src_workspace
	@echo Python linting complete

# Utilities

clean:
	@echo Cleaning Make Targets...
	@rm -f package
	@rm -f docker-build-app
	@echo Cleaned Make Targets.
	@echo Removing Build Targets...
	@rm -rf ${ROOT_DIRECTORY}/dist
	@echo Removed Build Targets.

setup-env:
	@cd ${PYTHON_PATH}; \
	pipenv install --dev

update-dependencies:
	@cd ${PYTHON_PATH}; \
	pipenv lock

github-docker-login:
	@echo ${CR_PAT} | docker login ${GITHUB_REPO} -u ${GITHUB_USER} --password-stdin