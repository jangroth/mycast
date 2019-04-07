.DEFAULT_GOAL := help

.PHONY: help # - this help
help:
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/\1 \2/' | expand -t20

.PHONY: docker-build # - builds container image for downloader.py
docker-build:
	$(info [*] Building container image for ECS task)
	cp ./src/downloader/downloader.py ./docker
	cd ./docker; docker build -t mycast .

.PHONY: docker-run-local # - runs container image for downloader.py
docker-run-local:
	$(info [*] Running ECS task locally locally...)
	$(eval AWS_ACCESS_KEY_ID=$(shell aws --profile jan configure get aws_access_key_id))
	$(eval AWS_SECRET_ACCESS_KEY=$(shell aws --profile jan configure get aws_secret_access_key))
	@docker run \
	   -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
	   -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
	   mycast:latest

.PHONY: docker-push-to-ecr # - pushes latest image to ecr
docker-push-to-ecr: docker-login docker-tag-latest
	$(info [*] Pushing latest image to ecr)
	docker push 010316939032.dkr.ecr.ap-southeast-2.amazonaws.com/mycast-ecs-repository

docker-tag-latest:
	$(info [*] Tagging latest image)
	docker tag mycast:latest 010316939032.dkr.ecr.ap-southeast-2.amazonaws.com/mycast-ecs-repository

docker-login:
	$(info [*] Logging into ECR)
	@eval $(ECR_LOGIN)

.PHONY: deploy # - deploy stack to AWS
deploy:
	$(info [*] Deploying to AWS)
	aws cloudformation deploy --template-file template.yaml --stack-name mycast --capabilities CAPABILITY_IAM


ECR_LOGIN := eval $$\(aws ecr get-login --region ap-southeast-2 --no-include-email\)