API_NAME=api
DB_NAME=db
DOCKER_COMMAND=docker-compose -f docker-compose.yml
DOCKER_HEX_COMMAND=docker-compose -f docker-compose.yml -f docker-compose.hex.yml
LOCAL_TASK_URL=http://localhost:9000/2015-03-31/functions/function/invocations

build:
	bash ./scripts/build.sh

# push last build image to ECR
push:
	bash ./scripts/push.sh

up:
	${DOCKER_COMMAND} up

down:
	${DOCKER_COMMAND} down

api:
	${DOCKER_COMMAND} run --service-ports ${API_NAME}

shell:
	${DOCKER_COMMAND} run --service-ports ${API_NAME} bash

# Run API and install local hex-lib library for development
run_hex_lib:
	${DOCKER_HEX_COMMAND}  run --service-ports ${API_NAME}

run_hex_lib_shell:
	${DOCKER_HEX_COMMAND}  run --service-ports ${API_NAME} bash

reset_db: stop
	${DOCKER_COMMAND} run ${DB_NAME} bash -c "rm -rf /data/db/*"
	${DOCKER_COMMAND} build ${DB_NAME}
	${DOCKER_COMMAND} run --service-ports ${DB_NAME}

test:
	${DOCKER_COMMAND} run ${API_NAME} bash -c "pytest src"

format:
	${DOCKER_COMMAND} run ${API_NAME} bash -c "scripts/lint.sh"

check:
	${DOCKER_COMMAND} run ${API_NAME} bash -c "scripts/lint.sh --check"

# Requires "make init_pipeline apply_pipeline" to be run in infra/ first
deploy:
	bash ./scripts/deploy.sh

clean:
	rm **/**/*.pyc
	rm **/**/__pycache__

update_project:
	bash ./scripts/update_project.sh
