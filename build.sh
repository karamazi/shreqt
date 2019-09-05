#!/usr/bin/env bash
set -e

rm -rf dist
poetry run pytest .
poetry run black --check .
poetry build
