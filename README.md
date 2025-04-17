[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/_images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

***

1. [Feature: OpenStudioLandscapes-Kitsu](#feature-openstudiolandscapes-kitsu)
   1. [Brief](#brief)
   2. [Requirements](#requirements)
   3. [Install](#install)
      1. [This Feature](#this-feature)
   4. [Add to OpenStudioLandscapes](#add-to-openstudiolandscapes)
   5. [Testing](#testing)
      1. [pre-commit](#pre-commit)
      2. [nox](#nox)
   6. [Variables](#variables)
      1. [Feature Configs](#feature-configs)
   7. [Community](#community)

***

# Feature: OpenStudioLandscapes-Kitsu

## Brief

This is an extension to the OpenStudioLandscapes ecosystem. The full documentation of OpenStudioLandscapes is available [here](https://github.com/michimussato/OpenStudioLandscapes).

You feel like writing your own Feature? Go and check out the [OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template).

## Requirements

- `python-3.11`
- `OpenStudioLandscapes`

## Install

### This Feature

Clone this repository into `OpenStudioLandscapes/.features`:

```shell

# cd .features
git clone https://github.com/michimussato/OpenStudioLandscapes-Kitsu.git

```

Create `venv`:

```shell

# cd .features/OpenStudioLandscapes-Kitsu
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools

```

Configure `venv`:

```shell

# cd .features/OpenStudioLandscapes-Kitsu
pip install -e "../../[dev]"
pip install -e ".[dev]"

```

For more info see [VCS Support of pip](https://pip.pypa.io/en/stable/topics/vcs-support/).

## Add to OpenStudioLandscapes

Add the following code to `OpenStudioLandscapes.engine.constants` (`THIRD_PARTY`):

```python

THIRD_PARTY.append(
   {
      "enabled": True,
      "module": "Kitsu.definitions",
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

#### Generate Report

```shell

nox --no-error-on-missing-interpreters --report .nox/nox-report.json

```

#### Re-Generate this README

```shell

nox --session readme

```

#### Generate Sphinx Documentation

```shell

nox --session docs

```

#### pylint

```shell

nox --session lint

```

##### pylint: disable=redefined-outer-name

- [`W0621`](https://pylint.pycqa.org/en/latest/user_guide/messages/warning/redefined-outer-name.html): Due to Dagsters way of piping arguments into assets.

#### SBOM

Acronym for Software Bill of Materials

```shell

nox --session sbom

```

We create the following SBOMs:

- [`cyclonedx-bom`](https://pypi.org/project/cyclonedx-bom/)
- [`pipdeptree`](https://pypi.org/project/pipdeptree/) (Dot)
- [`pipdeptree`](https://pypi.org/project/pipdeptree/) (Mermaid)

SBOMs for the different Python interpreters defined in [`.noxfile.VERSIONS`](https://github.com/michimussato/OpenStudioLandscapes-Kitsu/tree/main/noxfile.py) will be created in the [`.sbom`](https://github.com/michimussato/OpenStudioLandscapes-Kitsu/tree/main/.sbom) directory of this repository.

- `cyclone-dx`
- `pipdeptree` (Dot)
- `pipdeptree` (Mermaid)

Currently, the following Python interpreters are enabled for testing:

- `python3.11`
- `python3.12`

## Variables

The following variables are being declared in [`Kitsu`](https://github.com/michimussato/OpenStudioLandscapes-Kitsu/tree/main/src/OpenStudioLandscapes/Kitsu/constants.py) published throughout the `OpenStudioLandscapes-Kitsu` package.

| Variable                   | Type   |
| :------------------------- | :----- |
| `DOCKER_USE_CACHE`         | `bool` |
| `KITSUDB_INSIDE_CONTAINER` | `bool` |
| `GROUP`                    | `str`  |
| `KEY`                      | `list` |
| `ASSET_HEADER`             | `dict` |
| `FEATURE_CONFIGS`          | `dict` |

### Feature Configs

#### Feature Config: default

| Variable                             | Type   | Value                                                                                                                                      |
| :----------------------------------- | :----- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| `DOCKER_USE_CACHE`                   | `bool` | `True`                                                                                                                                     |
| `KITSU_HOSTNAME`                     | `str`  | `kitsu`                                                                                                                                    |
| `KITSU_ADMIN_USER`                   | `str`  | `michimussato@gmail.com`                                                                                                                   |
| `KITSU_DB_PASSWORD`                  | `str`  | `myp4ssword`                                                                                                                               |
| `KITSU_SECRET_KEY`                   | `str`  | `yourrandomsecretkey`                                                                                                                      |
| `KITSU_PREVIEW_FOLDER`               | `str`  | `/opt/zou/previews`                                                                                                                        |
| `KITSU_TMP_DIR`                      | `str`  | `/opt/zou/tmp`                                                                                                                             |
| `KITSU_PORT_HOST`                    | `str`  | `4545`                                                                                                                                     |
| `KITSU_PORT_CONTAINER`               | `str`  | `80`                                                                                                                                       |
| `KITSU_POSTGRES_CONF`                | `str`  | `/home/michael/git/repos/OpenStudioLandscapes/.features/OpenStudioLandscapes-Kitsu/.payload/config/etc/postgresql/14/main/postgresql.conf` |
| `KITSU_DATABASE_INSTALL_DESTINATION` | `str`  | `{DOT_LANDSCAPES}/{LANDSCAPE}/Kitsu__Kitsu/data/kitsu`                                                                                     |

## Community

| GitHub                                                                                                                       | Discord                                                                                                                | Slack                                                                                                  |
| ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| [OpenStudioLandscapes](https://github.com/michimussato/OpenStudioLandscapes)                                                 | [# openstudiolandscapes-general](https://discord.com/channels/1357343453364748419/1357343454065328202)                 | [# openstudiolandscapes-general](https://app.slack.com/client/T08L6M6L0S3/C08LK80NBFF)                 |
| [OpenStudioLandscapes-Ayon](https://github.com/michimussato/OpenStudioLandscapes-Ayon)                                       | [# openstudiolandscapes-ayon](https://discord.com/channels/1357343453364748419/1357722468336271411)                    | [# openstudiolandscapes-ayon](https://app.slack.com/client/T08L6M6L0S3/C08LLBC7CB0)                    |
| [OpenStudioLandscapes-Dagster](https://github.com/michimussato/OpenStudioLandscapes-Dagster)                                 | [# openstudiolandscapes-dagster](https://discord.com/channels/1357343453364748419/1358016764608249856)                 | [# openstudiolandscapes-dagster](https://app.slack.com/client/T08L6M6L0S3/C08LZR5JFA6)                 |
| [OpenStudioLandscapes-Deadline-10-2](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2)                     | [# openstudiolandscapes-deadline-10-2](https://discord.com/channels/1357343453364748419/1357343453364748419)           | [# openstudiolandscapes-deadline-10-2](https://app.slack.com/client/T08L6M6L0S3/C08LZR963A6)           |
| [OpenStudioLandscapes-Deadline-10-2-Worker](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2-Worker)       | [# openstudiolandscapes-deadline-10-2-worker](https://discord.com/channels/1357343453364748419/1357343453364748419)    | [# openstudiolandscapes-deadline-10-2-worker](https://app.slack.com/client/T08L6M6L0S3/C08LZSBM998)    |
| [OpenStudioLandscapes-NukeRLM-8](https://github.com/michimussato/OpenStudioLandscapes-NukeRLM-8)                             | [# openstudiolandscapes-nukerlm-8](https://discord.com/channels/1357343453364748419/1358017656732782672)               | [# openstudiolandscapes-nukerlm-8](https://app.slack.com/client/T08L6M6L0S3/C08LZDLFTMH)               |
| [OpenStudioLandscapes-SESI-gcc-9-3-Houdini-20](https://github.com/michimussato/OpenStudioLandscapes-SESI-gcc-9-3-Houdini-20) | [# openstudiolandscapes-sesi-gcc-9-3-houdini-20](https://discord.com/channels/1357343453364748419/1357343453364748419) | [# openstudiolandscapes-sesi-gcc-9-3-houdini-20](https://app.slack.com/client/T08L6M6L0S3/C08LUTR1WG5) |
| [OpenStudioLandscapes-Kitsu](https://github.com/michimussato/OpenStudioLandscapes-Kitsu)                                     | [# openstudiolandscapes-kitsu](https://discord.com/channels/1357343453364748419/1357638253632688231)                   | [# openstudiolandscapes-kitsu](https://app.slack.com/client/T08L6M6L0S3/C08L6M70ZB9)                   |