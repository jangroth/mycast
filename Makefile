.DEFAULT_GOAL := help

.PHONY: docker_build # - builds container image for downloader.py
docker_build:
	cp ./src/downloader/downloader.py ./docker
	cd ./docker; docker build -t mycast .

.PHONY: docker_run_local # - runs container image for downloader.py
docker_run_local:
	AWS_ACCESS_KEY_ID=$(aws --profile jan configure get aws_access_key_id); \
	echo "${AWS_ACCESS_KEY_ID}"

.PHONY: help # - this help
help:
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/\1 \2/' | expand -t20
