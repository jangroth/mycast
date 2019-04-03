.DEFAULT_GOAL := help

.PHONY: docker_build # - builds container image for downloader.py
docker_build:
	cp ./src/downloader/downloader.py ./docker
	cd ./docker; docker build -t mycast .

.PHONY: docker_run_local # - runs container image for downloader.py
docker_run_local:
	$(eval AWS_ACCESS_KEY_ID=$(shell aws --profile jan configure get aws_access_key_id))
	$(eval AWS_SECRET_ACCESS_KEY=$(shell aws --profile jan configure get aws_secret_access_key))
	@docker run \
	   -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
	   -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
	   mycast:latest

.PHONY: help # - this help
help:
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/\1 \2/' | expand -t20
