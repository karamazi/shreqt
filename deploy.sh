#!/usr/bin/env bash

if [ -z "$PYPIUSER" ]; then
    PYPIUSER="$(grep '\[pypi\]' ~/.pypirc -A2 | grep username  | cut -f 2 -d ':' |  xargs)"
fi

if [ -z "$PYPIPASS" ]; then
    PYPIPASS="$(grep '\[pypi\]' ~/.pypirc -A2 | grep password  | cut -f 2 -d ':' |  xargs)"
fi
poetry publish -u "$PYPIUSER" -p "$PYPIPASS"
