FROM node:12.18.4 AS www-builder

COPY ./www /www
WORKDIR /www
RUN npm install && npm run build

FROM --platform=linux/amd64 tianon/gosu:alpine AS gosu-builder

FROM python:3.9-alpine3.12
COPY --from=gosu-builder /usr/local/bin/gosu /usr/local/bin/gosu

RUN apk update \
    && apk upgrade \
    && apk add --no-cache --virtual .build-deps gcc musl-dev build-base nginx bash \
    && addgroup -S ci-dashboard \
    && adduser -S ci-dashboard -G ci-dashboard \
    && mkdir /run/nginx \
    && chown -R nginx:nginx /run/nginx/ \
    && chmod 775 /run/nginx/

COPY . /app
COPY --from=www-builder --chown=nginx:nginx /www/dist /www
COPY --chown=nginx:nginx ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT ["/app/dockerfile/docker-entrypoint.sh"]
