DOCKER_NAME=api
DOCKER_COMMAND=docker-compose -f docker-compose.yml
DOCKER_HEX_COMMAND=docker-compose -f docker-compose.yml -f docker-compose.hex.yml
LOCAL_TASK_URL=http://localhost:9000/2015-03-31/functions/function/invocations

build:
	bash ./scripts/build.sh

# push last build image to ECR
push:
	bash ./scripts/push.sh

run:
	${DOCKER_COMMAND} up

debug:
	${DOCKER_COMMAND} run --service-ports ${DOCKER_NAME}

shell:
	${DOCKER_COMMAND} run --service-ports ${DOCKER_NAME} bash

# Run API and install local hex-lib library for development
run_hex:
	${DOCKER_HEX_COMMAND}  run --service-ports ${DOCKER_NAME}

run_hex_shell:
	${DOCKER_HEX_COMMAND}  run --service-ports ${DOCKER_NAME} bash

reset_db: stop
	${DOCKER_COMMAND} run db bash -c "rm -rf /data/db/*"
	${DOCKER_COMMAND} build db
	${DOCKER_COMMAND} run --service-ports db

stop:
	${DOCKER_COMMAND} down

test:
	${DOCKER_COMMAND} run ${DOCKER_NAME} bash -c "pytest src"

lint:
	${DOCKER_COMMAND} run ${DOCKER_NAME} bash -c "scripts/lint.sh"

static:
	${DOCKER_COMMAND} run ${DOCKER_NAME} bash -c "scripts/lint.sh --check"

# Requires "make init_pipeline apply_pipeline" to be run in infra/ first
deploy:
	bash ./scripts/deploy.sh

clean:
	rm **/**/*.pyc
	rm **/**/__pycache__

update_project:
	bash ./scripts/update_project.sh
