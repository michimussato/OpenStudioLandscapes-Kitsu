[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/_images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

***

1. [OpenStudioLandscapes-Kitsu](#openstudiolandscapes-kitsu)
   1. [Brief](#brief)
   2. [Requirements](#requirements)
   3. [Install](#install)
      1. [From Github directly](#from-github-directly)
      2. [From local Repo](#from-local-repo)
   4. [Add to OpenStudioLandscapes](#add-to-openstudiolandscapes)
   5. [Testing](#testing)
      1. [pre-commit](#pre-commit)
      2. [nox](#nox)
      3. [pylint](#pylint)
      4. [SBOM](#sbom)
   6. [Variables](#variables)
      1. [Environment](#environment)
   7. [Community](#community)

***

# OpenStudioLandscapes-Kitsu

## Brief

This is an extension to the OpenStudioLandscapes ecosystem. The full documentation of OpenStudioLandscapes is available [here](https://github.com/michimussato/OpenStudioLandscapes).

You feel like writing your own module? Go and check out the [OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template).

## Requirements

- `python-3.11`

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

- `cyclone-dx`
- `pipdeptree` (Dot)
- `pipdeptree` (Mermaid)

Currently, the following Python interpreters are enabled for testing:

- `python3.11`
- `python3.12`

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

## Community

| GitHub                                                                                   | Discord                                                                                                | Slack                                                                                  |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| [OpenStudioLandscapes](https://github.com/michimussato/OpenStudioLandscapes)             | [# openstudiolandscapes-general](https://discord.com/channels/1357343453364748419/1357343454065328202) | [# openstudiolandscapes-general](https://app.slack.com/client/T08L6M6L0S3/C08LK80NBFF) |
| [OpenStudioLandscapes-Ayon](https://github.com/michimussato/OpenStudioLandscapes-Ayon)   | [# openstudiolandscapes-ayon](https://discord.com/channels/1357343453364748419/1357722468336271411)    | [# openstudiolandscapes-ayon](https://app.slack.com/client/T08L6M6L0S3/C08LLBC7CB0)    |
| [OpenStudioLandscapes-Kitsu](https://github.com/michimussato/OpenStudioLandscapes-Kitsu) | [# openstudiolandscapes-kitsu](https://discord.com/channels/1357343453364748419/1357638253632688231)   | [# openstudiolandscapes-kitsu](https://app.slack.com/client/T08L6M6L0S3/C08L6M70ZB9)   |