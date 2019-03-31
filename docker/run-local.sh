#!/usr/bin/env bash

set -eux

AWS_ACCESS_KEY_ID=$(aws --profile jan configure get aws_access_key_id)

set +x
AWS_SECRET_ACCESS_KEY=$(aws --profile jan configure get aws_secret_access_key)
set -x

docker run \
   -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
   -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
   mycast:latest

