#!/bin/bash
set -e

chown -R ci-dashboard /app

exec uvicorn main:app "$@"
