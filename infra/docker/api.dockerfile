FROM python:3.9

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
WORKDIR /app
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
ARG REPO=hex-lib
ARG CODEARTIFACT_REPOSITORY_URL
ARG CODEARTIFACT_AUTH_TOKEN
ARG CODEARTIFACT_USER
RUN bash -c "poetry config repositories.${REPO} $CODEARTIFACT_REPOSITORY_URL" && \
    bash -c "poetry config http-basic.${REPO} aws $CODEARTIFACT_AUTH_TOKEN" && \
    bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ADD ./app /app

ENV PYTHONPATH /app
CMD ["app.adapter.into.fastapi.lambda.handler"]
