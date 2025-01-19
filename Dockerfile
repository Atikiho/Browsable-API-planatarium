ARG PYTHON_VERSION=alpine
FROM python:${PYTHON_VERSION} as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN adduser \
    --disabled-password \
    --home /app \
    appuser

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


USER appuser

COPY . .

EXPOSE 8000
