#!/bin/bash
set -e

addgroup -S ci-dashboard && adduser -S -G ci-dashboard ci-dashboard

chown -R ci-dashboard /app

nginx

exec /usr/local/bin/gosu ci-dashboard uvicorn main:app "$@"
