FROM python:3.9-alpine

RUN apk update \
    && apk upgrade \
    && apk add --no-cache --virtual .build-deps gcc musl-dev build-base bash \
    && addgroup -S ci-dashboard \
    && adduser -S ci-dashboard -G ci-dashboard

USER ci-dashboard

COPY --chown=ci-dashboard:ci-dashboard . /app

EXPOSE 80

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PATH="/home/ci-dashboard/.local/bin:${PATH}"

WORKDIR /app

ENTRYPOINT ["/app/dockerfile/docker-entrypoint.sh"]
