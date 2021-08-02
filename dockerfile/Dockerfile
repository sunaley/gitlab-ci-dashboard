FROM --platform=linux/amd64 tianon/gosu:alpine AS gosu-builder

FROM python:3.9-alpine

COPY --from=gosu-builder /usr/local/bin/gosu /usr/local/bin/gosu

RUN apk update \
    && apk upgrade \
    && apk add --no-cache --virtual .build-deps gcc musl-dev build-base bash \
    && addgroup -S ci-dashboard \
    && adduser -S ci-dashboard -G ci-dashboard

COPY . /app

EXPOSE 80

RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT ["/app/dockerfile/docker-entrypoint.sh"]
