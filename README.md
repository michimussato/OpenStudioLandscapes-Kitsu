1. [Kitsu](#kitsu)
   1. [Brief](#brief)
   2. [Install](#install)
      1. [From Github directly](#from-github-directly)
      2. [From local Repo](#from-local-repo)
   3. [Add to OpenStudioLandscapes](#add-to-openstudiolandscapes)
   4. [Testing](#testing)
      1. [pre-commit](#pre-commit)
      2. [nox](#nox)
      3. [pylint](#pylint)
      4. [SBOM](#sbom)
   5. [Variables](#variables)
      1. [Environment](#environment)

***

# Kitsu

## Brief

[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/_images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

This is an extension to the OpenStudioLandscapes ecosystem. The full documentation of OpenStudioLandscapes is available [here](https://github.com/michimussato/OpenStudioLandscapes).

## Install

### From Github directly

WIP: This does not work as expected yet.

For more info see [VCS Support of pip](https://pip.pypa.io/en/stable/topics/vcs-support/).

### From local Repo

Clone repository:

```shell

git clone https://github.com/michimussato/OpenStudioLandscapes-Kitsu.git
cd OpenStudioLandscapes-Kitsu

```

Create venv, activate it and upgrade:

```shell

python3.11 -m venv .venv
source .venv/bin/activate
pip install setuptools --upgrade

```

```shell

pip install -e .[dev]

```

For more info see [VCS Support of pip](https://pip.pypa.io/en/stable/topics/vcs-support/).

## Add to OpenStudioLandscapes

Add the following code to `OpenStudioLandscapes.engine.constants` (`THIRD_PARTY`):

```python

THIRD_PARTY.append(
   {
      "enabled": True,
      "module": "OpenStudioLandscapes.Kitsu.definitions",
      "compose_scope": ComposeScope.DEFAULT,
   }
)

```

## Testing

### pre-commit

- https://pre-commit.com
- https://pre-commit.com/hooks.html

```shell

pre-commit install

```

### nox

```shell

nox --no-error-on-missing-interpreters --report .nox/nox-report.json

```

### pylint

#### pylint: disable=redefined-outer-name

- [`W0621`](https://pylint.pycqa.org/en/latest/user_guide/messages/warning/redefined-outer-name.html): Due to Dagsters way of piping arguments into assets.

### SBOM

Acronym for Software Bill of Materials

We create the following SBOMs:

- [`cyclonedx-bom`](https://pypi.org/project/cyclonedx-bom/)
- [`pipdeptree`](https://pypi.org/project/pipdeptree/) (Dot)
- [`pipdeptree`](https://pypi.org/project/pipdeptree/) (Mermaid)

SBOMs for the different Python interpreters defined in [`.noxfile.VERSIONS`](https://github.com/michimussato/OpenStudioLandscapes-Kitsu/tree/main/noxfile.py) will be created in [`.sbom`](https://github.com/michimussato/OpenStudioLandscapes-Kitsu/tree/main/.sbom)

Currently, the following Python interpreters are enabled for testing:

- `cyclone-dx`
- `pipdeptree` (Dot)
- `pipdeptree` (Mermaid)

## Variables

The following variables are being declared in [`OpenStudioLandscapes.Kitsu.constants`](https://github.com/michimussato/OpenStudioLandscapes-Kitsu/tree/main/src/OpenStudioLandscapes/Kitsu/constants.py) published throuout the `OpenStudioLandscapes-Kitsu` package.

| Variable                   | Type           |
| :------------------------- | :------------- |
| `DOCKER_USE_CACHE`         | `bool`         |
| `KITSUDB_INSIDE_CONTAINER` | `bool`         |
| `GROUP`                    | `str`          |
| `KEY`                      | `list`         |
| `ASSET_HEADER`             | `dict`         |
| `ENVIRONMENT`              | `dict`         |
| `COMPOSE_SCOPE`            | `ComposeScope` |

### Environment

| Variable                             | Type   |
| :----------------------------------- | :----- |
| `DOCKER_USE_CACHE`                   | `bool` |
| `KITSU_HOSTNAME`                     | `str`  |
| `KITSU_ADMIN_USER`                   | `str`  |
| `KITSU_DB_PASSWORD`                  | `str`  |
| `KITSU_SECRET_KEY`                   | `str`  |
| `KITSU_PREVIEW_FOLDER`               | `str`  |
| `KITSU_TMP_DIR`                      | `str`  |
| `KITSU_PORT_HOST`                    | `str`  |
| `KITSU_PORT_CONTAINER`               | `str`  |
| `KITSU_POSTGRES_CONF`                | `str`  |
| `KITSU_DATABASE_INSTALL_DESTINATION` | `str`  |
