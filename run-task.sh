#!/usr/bin/env bash
here=$(dirname "$(readlink -f "$0")")
export FLASK_APP="$here/task/app.py"
export FLASK_ENV=development
flask run --host 0.0.0.0 --port 42069 --debug
