# Geneweaver Client

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/TheJacksonLaboratory/geneweaver-client/tests.yml?branch=main&style=for-the-badge&logo=github&label=Tests)](https://github.com/TheJacksonLaboratory/geneweaver-client/actions/workflows/tests.yml?query=branch%3Amain++)
[![Style](https://img.shields.io/github/actions/workflow/status/TheJacksonLaboratory/geneweaver-client/style.yml?branch=main&style=for-the-badge&logo=github&label=Style)](https://github.com/TheJacksonLaboratory/geneweaver-client/actions/workflows/style.yml?query=branch%3Amain++)
[![Coverage](https://img.shields.io/github/actions/workflow/status/TheJacksonLaboratory/geneweaver-client/coverage.yml?branch=main&style=for-the-badge&logo=github&label=Coverage)](https://github.com/TheJacksonLaboratory/geneweaver-client/actions/workflows/coverage.yml?query=branch%3Amain++)

![PyPI - License](https://img.shields.io/pypi/l/geneweaver-client?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/geneweaver-client?style=for-the-badge)
[![PyPI - Version](https://img.shields.io/pypi/v/geneweaver-client?style=for-the-badge&logo=pypi&logoColor=%23fff)](https://pypi.org/project/geneweaver-client/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/geneweaver-client?style=for-the-badge)](https://pypi.org/project/geneweaver-client/)



This is a client for the [Geneweaver](https://geneweaver.org) API. It is written in 
Python 3.9 and is intended to be used as a library for other applications. It can also 
be used as a command line tool.

## Installation
This library is tested on python version `3.9`, `3.10`, and `3.11`, on MacOS and on
Ubuntu Linux. The library should work on any version of python `3.9` or higher.

### From PyPI

```bash
pip install geneweaver-client
```

### From Source
Installing from source requires python 3.9 and [poetry](https://python-poetry.org/).


```bash
git clone $GIT_URL
cd geneweaver-client
poetry install
```

## Usage

### As a library

#### Using Authentication Tools
```
from geneweaver.client import auth
auth.login()
auth.get_access_token()
```

#### Complete Example
See the [Geneweaver Docs](https://thejacksonlaboratory.github.io/geneweaver-docs/tutorial/nci_60_example_01/)


### As a command line tool

```bash
gweave --help
```

GeneWeaver CLI client.

**Usage**:

```console
$ gweave [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `alpha`: These commands are in alpha testing.
* `beta`: These commands are in beta testing. 

-----

### `gweave beta`

These commands are in beta testing.

They are subject to future change and/or removal. Beta commands are
intended to be released beyond beta testing, but may have bugs or other
issues. There is also no guarantee that beta commands will be released
beyond beta testing.

Use at your own risk.

**Usage**:

```console
$ gweave beta [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `auth`

#### `gweave beta auth`

**Usage**:

```console
$ gweave beta auth [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `login`: Run the device authorization flow.

##### `gweave beta auth login`

Run the device authorization flow.

:param reauth: Force a re-authentication

**Usage**:

```console
$ gweave beta auth login [OPTIONS]
```

**Options**:

* `--reauth`
* `--help`: Show this message and exit.