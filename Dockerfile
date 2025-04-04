ARG PYTHON_VERSION=3.12.5

FROM python:${PYTHON_VERSION}-slim-bookworm

LABEL maintainer="imtoopunkforyou"
LABEL email="cptchunk@yandex.ru"
LABEL homepage="https://github.com/imtoopunkforyou/show-me-id"

RUN apt update -y && apt install -y \
    bash \
    curl \
    && exit 0

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN bash /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed
ENV PROJECT_PATH="/src"
ENV SCRIPTS_PATH="$PROJECT_PATH/scripts"
ENV ENTRYPOINT_FILE="$SCRIPTS_PATH/docker-entrypoint.sh"

RUN uv python install 3.12.5

RUN mkdir -p ${PROJECT_PATH}
COPY ./ ${PROJECT_PATH}

RUN chmod +x ${ENTRYPOINT_FILE}
ENTRYPOINT ${ENTRYPOINT_FILE}

WORKDIR ${PROJECT_PATH}
