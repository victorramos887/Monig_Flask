#!/usr/bin/env bash

set -e

# ls /usr/src/app/
# echo "Reset DB!!"


# echo "Run wsgi!!"

gunicorn --bind 0.0.0.0:${APP_PORT} src:app