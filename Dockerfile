FROM python:3.12-alpine
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  OAUTHLIB_INSECURE_TRANSPORT=1

STOPSIGNAL SIGINT
RUN apk update && apk add --no-cache git curl
RUN curl -sSL install.python-poetry.org | POETRY_HOME=/opt/poetry python -
ENV PATH /opt/poetry/bin:$PATH

WORKDIR /app
COPY . /app
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
CMD ["poetry", "run", "gunicorn", "-w", "3", "--access-logfile=-", "-b", "0.0.0.0:80", "s3htmlviewer.web:app"]