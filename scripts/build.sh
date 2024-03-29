#! /bin/bash

set -e

source $(dirname "$0")/code-artifact-poetry.sh

DOCKER_COMMAND="docker-compose -f docker-compose.yml"
DOCKER_HEX_COMMAND="docker-compose -f docker-compose.yml -f docker-compose.hex.yml"

${DOCKER_COMMAND} build --no-cache \
	--build-arg INSTALL_DEV=true \
	--build-arg CODEARTIFACT_REPOSITORY_URL=${CODEARTIFACT_REPOSITORY_URL} \
	--build-arg CODEARTIFACT_AUTH_TOKEN=${CODEARTIFACT_AUTH_TOKEN}


${DOCKER_HEX_COMMAND} build --no-cache \
	--build-arg INSTALL_DEV=true \
	--build-arg CODEARTIFACT_REPOSITORY_URL=${CODEARTIFACT_REPOSITORY_URL} \
	--build-arg CODEARTIFACT_AUTH_TOKEN=${CODEARTIFACT_AUTH_TOKEN}
