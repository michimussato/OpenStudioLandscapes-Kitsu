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
2. [Community](#community)
3. [Kitsu Documentation](#kitsu-documentation)

***

This `README.md` was dynamically created with [OpenStudioLandscapesUtil-ReadmeGenerator](https://github.com/michimussato/OpenStudioLandscapesUtil-ReadmeGenerator).

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

Add the following code to `OpenStudioLandscapes.engine.constants` (`FEATURES`):

```python

FEATURES.update(
    "OpenStudioLandscapes-Kitsu": {
        "enabled": True,
        "module": "OpenStudioLandscapes.Kitsu.definitions",
        "compose_scope": ComposeScope.DEFAULT,
        "feature_config": OpenStudioLandscapesConfig.DEFAULT,
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

nox -v --add-timestamp --session readme

```

#### Generate Sphinx Documentation

```shell

nox -v --add-timestamp --session docs

```

#### pylint

```shell

nox -v --add-timestamp --session lint

```

##### pylint: disable=redefined-outer-name

- [`W0621`](https://pylint.pycqa.org/en/latest/user_guide/messages/warning/redefined-outer-name.html): Due to Dagsters way of piping arguments into assets.

#### SBOM

Acronym for Software Bill of Materials

```shell

nox -v --add-timestamp --session sbom

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

The following variables are being declared in `OpenStudioLandscapes.Kitsu.constants` and are accessible throughout the [`OpenStudioLandscapes-Kitsu`](https://github.com/michimussato/OpenStudioLandscapes-Kitsu/tree/main/src/OpenStudioLandscapes/Kitsu/constants.py) package.

| Variable                   | Type   |
| :------------------------- | :----- |
| `DOCKER_USE_CACHE`         | `bool` |
| `KITSUDB_INSIDE_CONTAINER` | `bool` |
| `ASSET_HEADER`             | `dict` |
| `FEATURE_CONFIGS`          | `dict` |

### Feature Configs

#### Feature Config: default

| Variable                             | Type   | Value                                                                                              |
| :----------------------------------- | :----- | :------------------------------------------------------------------------------------------------- |
| `DOCKER_USE_CACHE`                   | `bool` | `False`                                                                                            |
| `KITSU_ENABLE_JOB_QUEUE`             | `bool` | `True`                                                                                             |
| `KITSU_HOSTNAME`                     | `str`  | `kitsu`                                                                                            |
| `KITSU_ADMIN_USER`                   | `str`  | `admin@example.com`                                                                                |
| `KITSU_DB_PASSWORD`                  | `str`  | `mysecretpassword`                                                                                 |
| `KITSU_SECRET_KEY`                   | `str`  | `yourrandomsecretkey`                                                                              |
| `KITSU_PREVIEW_FOLDER`               | `str`  | `/opt/zou/previews`                                                                                |
| `KITSU_TMP_DIR`                      | `str`  | `/opt/zou/tmp`                                                                                     |
| `KITSU_PORT_HOST`                    | `str`  | `4545`                                                                                             |
| `KITSU_PORT_CONTAINER`               | `str`  | `80`                                                                                               |
| `KITSU_POSTGRES_CONF`                | `str`  | `{DOT_FEATURES}/OpenStudioLandscapes-Kitsu/.payload/config/etc/postgresql/14/main/postgresql.conf` |
| `KITSU_DATABASE_INSTALL_DESTINATION` | `str`  | `{DOT_LANDSCAPES}/{LANDSCAPE}/Kitsu__Kitsu/data/kitsu`                                             |

# Community

| GitHub                                                                                                                       | Discord                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| [OpenStudioLandscapes](https://github.com/michimussato/OpenStudioLandscapes)                                                 | [# openstudiolandscapes-general](https://discord.com/channels/1357343453364748419/1357343454065328202)                 |
| [OpenStudioLandscapes-Ayon](https://github.com/michimussato/OpenStudioLandscapes-Ayon)                                       | [# openstudiolandscapes-ayon](https://discord.com/channels/1357343453364748419/1357722468336271411)                    |
| [OpenStudioLandscapes-Dagster](https://github.com/michimussato/OpenStudioLandscapes-Dagster)                                 | [# openstudiolandscapes-dagster](https://discord.com/channels/1357343453364748419/1358016764608249856)                 |
| [OpenStudioLandscapes-Deadline-10-2](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2)                     | [# openstudiolandscapes-deadline-10-2](https://discord.com/channels/1357343453364748419/1357343453364748419)           |
| [OpenStudioLandscapes-Deadline-10-2-Worker](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2-Worker)       | [# openstudiolandscapes-deadline-10-2-worker](https://discord.com/channels/1357343453364748419/1357343453364748419)    |
| [OpenStudioLandscapes-filebrowser](https://github.com/michimussato/OpenStudioLandscapes-filebrowser)                         | [# openstudiolandscapes-filebrowser](https://discord.com/channels/1357343453364748419/1364746200175083520)             |
| [OpenStudioLandscapes-NukeRLM-8](https://github.com/michimussato/OpenStudioLandscapes-NukeRLM-8)                             | [# openstudiolandscapes-nukerlm-8](https://discord.com/channels/1357343453364748419/1358017656732782672)               |
| [OpenStudioLandscapes-SESI-gcc-9-3-Houdini-20](https://github.com/michimussato/OpenStudioLandscapes-SESI-gcc-9-3-Houdini-20) | [# openstudiolandscapes-sesi-gcc-9-3-houdini-20](https://discord.com/channels/1357343453364748419/1357343453364748419) |
| [OpenStudioLandscapes-Syncthing](https://github.com/michimussato/OpenStudioLandscapes-Syncthing)                             | [# openstudiolandscapes-syncthing](https://discord.com/channels/1357343453364748419/1364746871381168138)               |
| [OpenStudioLandscapes-Kitsu](https://github.com/michimussato/OpenStudioLandscapes-Kitsu)                                     | [# openstudiolandscapes-kitsu](https://discord.com/channels/1357343453364748419/1357638253632688231)                   |
| [OpenStudioLandscapes-Watchtower](https://github.com/michimussato/OpenStudioLandscapes-Watchtower)                           | [# openstudiolandscapes-watchtower](https://discord.com/channels/1357343453364748419/1364747275938562079)              |

To follow up on the previous LinkedIn publications, visit:

- [OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/company/106731439/).
- [Search for tag #OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/search/results/all/?keywords=%23openstudiolandscapes).

***

# Kitsu Documentation

- [https://kitsu.cg-wire.com](https://kitsu.cg-wire.com)

[![ Logo Kitsu ](https://camo.githubusercontent.com/023fe0d7cf9dc4bd4258a299a718a8c98d94be4357d72dfda0fcb0217ba1582c/68747470733a2f2f7a6f752e63672d776972652e636f6d2f6b697473752e706e67)](https://github.com/cgwire/zou)

Kitsu is written and maintained by CGWire, a company based in France:

[![ Logo CGWire ](https://www.cg-wire.com/_nuxt/logo.4d5a2d7e.png)](https://www.cg-wire.com)

Kitsu itself consists of two modules:

1. [Gazu - Kitsu Python Client](https://gazu.cg-wire.com)
2. [Zou - Kitsu Python API](https://zou.cg-wire.com)

`OpenStudioLandscapes-Kitsu` is based on the Kitsu provided Docker image:

- [https://kitsu.cg-wire.com/installation/#using-docker-image](https://kitsu.cg-wire.com/installation/#using-docker-image)
- [https://hub.docker.com/r/cgwire/cgwire](https://hub.docker.com/r/cgwire/cgwire)

The default credentials are:

- User: `admin@example.com`
- Password: `mysecretpassword`

You can override the default credentials by setting:

- `KITSU_ADMIN_USER`
- `KITSU_DB_PASSWORD`