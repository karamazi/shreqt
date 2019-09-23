# ShreQT

[![codecov](https://codecov.io/gh/karamazi/shreqt/branch/master/graph/badge.svg)](https://codecov.io/gh/karamazi/shreqt)
[![Build Status](https://travis-ci.org/karamazi/shreqt.svg?branch=master)](https://travis-ci.org/karamazi/shreqt)
[![PyPi Version](https://img.shields.io/pypi/v/shreqt.svg?style=flat)](https://pypi.org/project/shreqt/)


```
⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆
⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿
⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀
⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀  Tests have layers
⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀  Ogres have layers
⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀        ~ Anonymous
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠛⠉
```

# Overview

Query testing framework.

Currently supports only Exasol DB.

This project uses [Poetry](https://github.com/sdispater/poetry) for dependency management and packaging.

# Development

To setup your virtual environment run the following command. The default location for poetry venvs is `~/Library/Caches/pypoetry/virtualenvs`

```bash
poetry install
```

To run tests and lint checks:

```bash
make checks
```

To format on all files:

```bash
make fmt
```

# Usage

### Prequisite

Currently we only support Exasol connections.
To run local instance of Exasol as docker container run:

```bash
docker run  -p 8999:8888 --detach --privileged --stop-timeout 120  exasol/docker-db:6.0.13-d1
```

_(MacOS)_ Keep in mind that Exasol is memory-heavy and you need to increase docker memory limit to at least `4GB`

### Credentials

ShreQT uses following environment variables to connect to database.

| Variable    | Default Value  |
| ----------- | -------------- |
| SHREQT_DSN  | localhost:8999 |
| SHREQT_USER | sys            |
| SHREQT_PASS | exasol         |

## Example

The `example` directory contains simple example which illustrates the example usage.

- `conftest.py` includes simple User schema and code which sets up the database for test session.
- `example.py` includes a tested function.
- `example_test.py` include example test function.

You can run the example with:

```bash
make run-example
```

# Build && Deploy

Setup `~/.pypirc` with credentials.

Run checks and build package:

```bash
make build
```

Deploy package to pypi using poetry:

```bash
make deploy
```

### TODO

- Automate deployment step with travis
- Decorator functionality for temporary layer
