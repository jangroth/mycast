#!/usr/bin/env bash

set -eux

cp ../src/downloader/downloader.py .

docker build -t mycast .

