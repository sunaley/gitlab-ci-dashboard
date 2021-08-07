#!/bin/bash
set -e

addgroup -S ci-dashboard && adduser -S -G ci-dashboard ci-dashboard

chown -R ci-dashboard /app

/usr/local/bin/gosu nginx nginx -g "daemon off;"

exec /usr/local/bin/gosu ci-dashboard uvicorn main:app "$@"
