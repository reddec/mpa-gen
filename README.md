# mpa-gen

[![PyPI version](https://badge.fury.io/py/mpa-gen.svg)](https://badge.fury.io/py/mpa-gen)
[![GitHub license](https://img.shields.io/github/license/reddec/mpa-gen)](https://github.com/reddec/mpa-gen/blob/master/LICENSE)

Generates directories and files for multi-page
site with backend on Go (gin).



Generates:

- layouts
- views (page templates)
- controller stub with in/out params parsing
- utils for bootstrap

Requirements:

- Jinja2
- Python3.4+ (actually could run even on lower version but I didn't test)

## Installation

`pip install mpa-gen`

## Quick start from scratch

1. Create empty directory and go into it
2. Install latest mpa-gen `pip3 install --upgrade --user mpa-gen`
3. Initialize go project `go mod init myproject`
4. Generate site structure `mpa-gen portal main`

![Peek 2019-10-02 13-16](https://user-images.githubusercontent.com/6597086/66019781-453aca00-e517-11e9-80ee-016d4285af56.gif)


## Usage

```
usage: mpa-gen [-h] [--dir DIR] [--method METHOD] section name

multi-page site generator

positional arguments:
  section          Section name (ex: user/messages)
  name             Resource name (ex: dialog)

optional arguments:
  -h, --help       show this help message and exit
  --dir DIR        Root directory
  --method METHOD  HTTP method: GET or POST

```

- default method: `GET`
- default directory: current working dir