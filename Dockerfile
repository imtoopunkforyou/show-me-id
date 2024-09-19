FROM python:3.12.5-alpine

LABEL maintainer='imtoopunkforyou'
LABEL email='cptchunk@yandex.ru'
LABEL homepage='https://github.com/imtoopunkforyou/show-me-id'

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=0

ENV PIP_ROOT_USER_ACTION=ignore
ENV POETRY_VIRTUALENVS_CREATE=false

ENV PROJECT_PATH="/smid"
ENV VOLUME_PATH="$PROJECT_PATH/logs"

RUN apk update --no-cache && apk add --no-cache \
    bash \
    htop \
    && exit 0

RUN mkdir -p $VOLUME_PATH
VOLUME $VOLUME_PATH

COPY ./smid/ $PROJECT_PATH

WORKDIR $PROJECT_PATH
RUN pip install poetry
COPY pyproject.toml poetry.lock $PROJECT_PATH
RUN poetry install --without dev --without lint --no-root


COPY entrypoint.sh ./
RUN chmod +x ./entrypoint.sh
ENTRYPOINT $PROJECT_PATH/entrypoint.sh