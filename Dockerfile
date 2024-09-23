FROM python:3.12.5-alpine

LABEL maintainer="imtoopunkforyou"
LABEL email="cptchunk@yandex.ru"
LABEL homepage="https://github.com/imtoopunkforyou/show-me-id"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=0

ENV PIP_ROOT_USER_ACTION=ignore
ENV POETRY_VIRTUALENVS_CREATE=false

ENV PROJECT_PATH="/src"
ENV SCRIPTS_PATH="$PROJECT_PATH/scripts"
ENV ENTRYPOINT_FILE="$SCRIPTS_PATH/docker-entrypoint.sh"

RUN apk update --no-cache && apk add --no-cache \
    bash \
    htop \
    curl \
    && exit 0

RUN mkdir -p $PROJECT_PATH
COPY ./ $PROJECT_PATH

RUN pip install --upgrade pip
RUN pip install poetry
RUN cd $PROJECT_PATH/ && poetry install --without dev --without lint --no-root

RUN chmod +x $ENTRYPOINT_FILE
ENTRYPOINT $ENTRYPOINT_FILE
