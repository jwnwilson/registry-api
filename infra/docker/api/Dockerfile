FROM python:3.9

# Install Poetry
ENV PATH="/root/.local/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python - && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
WORKDIR /main
COPY ./pyproject.toml ./poetry.lock* /main/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
ARG REPO=hex-lib
ARG CODEARTIFACT_REPOSITORY_URL
ARG CODEARTIFACT_AUTH_TOKEN
ARG CODEARTIFACT_USER
RUN poetry config repositories.${REPO} $CODEARTIFACT_REPOSITORY_URL && \
    poetry config http-basic.${REPO} aws $CODEARTIFACT_AUTH_TOKEN && \
    bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ADD ./src /main/src

ENV PYTHONPATH /main/src
CMD ["uvicorn", "app.adapter.into.fastapi.main:app", "--host", "0.0.0.0", "--port", "800"]
