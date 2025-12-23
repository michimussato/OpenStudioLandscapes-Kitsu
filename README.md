[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

***

1. [Feature: OpenStudioLandscapes-Kitsu](#feature-openstudiolandscapes-kitsu)
   1. [Brief](#brief)
   2. [Configuration](#configuration)
2. [External Resources](#external-resources)
3. [Community](#community)
4. [Technical Reference](#technical-reference)
   1. [Requirements](#requirements)
   2. [Install](#install)
      1. [This Feature](#this-feature)
   3. [Testing](#testing)
      1. [pre-commit](#pre-commit)
      2. [nox](#nox)

***

This `README.md` was dynamically created with [OpenStudioLandscapesUtil-ReadmeGenerator](https://github.com/michimussato/OpenStudioLandscapesUtil-ReadmeGenerator).

***

# Feature: OpenStudioLandscapes-Kitsu

## Brief

This is an extension to the OpenStudioLandscapes ecosystem. The full documentation of OpenStudioLandscapes is available [here](https://github.com/michimussato/OpenStudioLandscapes).

> [!NOTE]
> 
> You feel like writing your own Feature? Go and check out the 
> [OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template).

## Configuration

OpenStudioLandscapes will search for a local config store. The default location is `~/.config/OpenStudioLandscapes/config-store/` but you can specify a different location if you need to.

A local config store location will be created if it doesn't exist, together with the `config.yml` files for each individual Feature.

> [!TIP]
> 
> The config store root will be initialized as a local Git
> controlled repository. This makes it easy to track changes
> you made to the `config.yml`.

> [!TIP]
> 
> To specify a config store location different than
> the default, you can do so be setting the environment variable
> `OPENSTUDIOLANDSCAPES__CONFIGSTORE_ROOT`:
> 
> ```shell
> OPENSTUDIOLANDSCAPES__CONFIGSTORE_ROOT="~/.config/OpenStudioLandscapes/my-custom-config-store"
> ```

The following settings are available in `OpenStudioLandscapes-Kitsu` and are based on [`OpenStudioLandscapes-Kitsu/tree/main/OpenStudioLandscapes/Kitsu/config/models.py`](https://github.com/michimussato/OpenStudioLandscapes-Kitsu/tree/main/OpenStudioLandscapes/Kitsu/config/models.py).

```yaml
# ===
# env
# ---
#
# Type: typing.Dict
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# =============
# config_engine
# -------------
#
# Type: <class 'OpenStudioLandscapes.engine.config.models.ConfigEngine'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# =============
# config_parent
# -------------
#
# Type: <class 'OpenStudioLandscapes.engine.config.models.FeatureBaseModel'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ============
# distribution
# ------------
#
# Type: <class 'importlib.metadata.Distribution'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ==========
# group_name
# ----------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ============
# key_prefixes
# ------------
#
# Type: typing.List[str]
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# =======
# enabled
# -------
#
# Type: <class 'bool'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         Whether the Feature is enabled or not.
#     Default value:
#         True
# Description:
#     Whether the Feature is enabled or not.
# Required:
#     False
# Examples:
#     None


# =============
# compose_scope
# -------------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         default
# Description:
#     None
# Required:
#     False
# Examples:
#     ['default', 'license_server', 'worker']


# ============
# feature_name
# ------------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         True
#     Description:
#         The name of the feature. It is derived from the `OpenStudioLandscapes.<Feature>.dist` attribute.
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
feature_name: OpenStudioLandscapes-Kitsu


# ==============
# docker_compose
# --------------
#
# Type: <class 'pathlib.Path'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         The path to the `docker-compose.yml` file.
#     Default value:
#         {DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/docker_compose/docker-compose.yml
# Description:
#     The path to the `docker-compose.yml` file.
# Required:
#     False
# Examples:
#     None


# ================
# kitsu_admin_user
# ----------------
#
# Type: <class 'pydantic.networks.EmailStr'>
# Description:
#     Bug Report: https://github.com/cgwire/zou/issues/960); Changing these values does not seem to have an effect Hence, they are locked to the following values for now.
# Required:
#     False
# Examples:
#     None
kitsu_admin_user: admin@example.com


# =================
# kitsu_db_password
# -----------------
#
# Type: <class 'str'>
# Description:
#     The Postgres database password.
# Required:
#     False
# Examples:
#     None
kitsu_db_password: mysecretpassword


# ===================
# kitsu_postgres_conf
# -------------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     The Kitsu Postgres configuration file.
# Required:
#     False
# Examples:
#     None
kitsu_postgres_conf: '{DOT_FEATURES}/{FEATURE}/.payload/config/etc/postgresql/14/main/postgresql.conf'


# ======================
# kitsu_enable_job_queue
# ----------------------
#
# Type: <class 'bool'>
# Description:
#     Enable Kitsu Job Queue?
# Required:
#     False
# Examples:
#     None
kitsu_enable_job_queue: true


# ====================
# kitsu_port_container
# --------------------
#
# Type: <class 'int'>
# Description:
#     The Kitsu container port.
# Required:
#     False
# Examples:
#     None
kitsu_port_container: 80


# ===============
# kitsu_port_host
# ---------------
#
# Type: <class 'int'>
# Description:
#     The Kitsu host port.
# Required:
#     False
# Examples:
#     None
kitsu_port_host: 4545


# ==================================
# kitsu_database_install_destination
# ----------------------------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     The host side Kitsu database installation destination.
# Required:
#     False
# Examples:
#     None
kitsu_database_install_destination: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/data/kitsu'


# =========================
# kitsu_db_inside_container
# -------------------------
#
# Type: <class 'bool'>
# Description:
#     The Kitsu database inside container; the database will not be persistent. Helpful for testing.
# Required:
#     False
# Examples:
#     None
kitsu_db_inside_container: false


# ====================
# kitsu_preview_folder
# --------------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     The Kitsu Preview folder.
# Required:
#     False
# Examples:
#     None
kitsu_preview_folder: /opt/zou/previews


# =============
# kitsu_tmp_dir
# -------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     Kitsu TMP directory.
# Required:
#     False
# Examples:
#     None
kitsu_tmp_dir: /opt/zou/tmp


# ================
# kitsu_secret_key
# ----------------
#
# Type: <class 'str'>
# Description:
#     Kitsu Secret Key.
# Required:
#     False
# Examples:
#     None
kitsu_secret_key: yourrandomsecretkey



```

***

# External Resources

- [https://kitsu.cg-wire.com](https://kitsu.cg-wire.com)

[![Logo Kitsu ](https://camo.githubusercontent.com/023fe0d7cf9dc4bd4258a299a718a8c98d94be4357d72dfda0fcb0217ba1582c/68747470733a2f2f7a6f752e63672d776972652e636f6d2f6b697473752e706e67)](https://github.com/cgwire/zou)

Kitsu is written and maintained by CGWire, a company based in France:

[![Logo CGWire ](https://www.cg-wire.com/_nuxt/logo.4d5a2d7e.png)](https://www.cg-wire.com)

Kitsu itself consists of two modules:

1. [Gazu - Kitsu Python Client](https://gazu.cg-wire.com)
2. [Zou - Kitsu Python API](https://zou.cg-wire.com)

`OpenStudioLandscapes-Kitsu` is based on the Kitsu provided Docker image:

- [https://kitsu.cg-wire.com/installation/#using-docker-image](https://kitsu.cg-wire.com/installation/#using-docker-image)
- [https://hub.docker.com/r/cgwire/cgwire](https://hub.docker.com/r/cgwire/cgwire)

The default credentials are:

- User: `admin@example.com`
- Password: `mysecretpassword`

***

# Community

| Feature                              | GitHub                                                                                                                                       | Discord                                                                 |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| OpenStudioLandscapes                 | [https://github.com/michimussato/OpenStudioLandscapes](https://github.com/michimussato/OpenStudioLandscapes)                                 | [# openstudiolandscapes-general](https://discord.gg/F6bDRWsHac)         |
| OpenStudioLandscapes-Ayon            | [https://github.com/michimussato/OpenStudioLandscapes-Ayon](https://github.com/michimussato/OpenStudioLandscapes-Ayon)                       | [# openstudiolandscapes-ayon](https://discord.gg/gd6etWAF3v)            |
| OpenStudioLandscapes-Dagster         | [https://github.com/michimussato/OpenStudioLandscapes-Dagster](https://github.com/michimussato/OpenStudioLandscapes-Dagster)                 | [# openstudiolandscapes-dagster](https://discord.gg/jwB3DwmKvs)         |
| OpenStudioLandscapes-Flamenco        | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco](https://github.com/michimussato/OpenStudioLandscapes-Flamenco)               | [# openstudiolandscapes-flamenco](https://discord.gg/EPrX5fzBCf)        |
| OpenStudioLandscapes-Flamenco-Worker | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker](https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker) | [# openstudiolandscapes-flamenco-worker](https://discord.gg/Sa2zFqSc4p) |
| OpenStudioLandscapes-Kitsu           | [https://github.com/michimussato/OpenStudioLandscapes-Kitsu](https://github.com/michimussato/OpenStudioLandscapes-Kitsu)                     | [# openstudiolandscapes-kitsu](https://discord.gg/6cc6mkReJ7)           |
| OpenStudioLandscapes-RustDeskServer  | [https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer](https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer)   | [# openstudiolandscapes-rustdeskserver](https://discord.gg/nJ8Ffd2xY3)  |
| OpenStudioLandscapes-Template        | [https://github.com/michimussato/OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template)               | [# openstudiolandscapes-template](https://discord.gg/J59GYp3Wpy)        |
| OpenStudioLandscapes-VERT            | [https://github.com/michimussato/OpenStudioLandscapes-VERT](https://github.com/michimussato/OpenStudioLandscapes-VERT)                       | [# openstudiolandscapes-twingate](https://discord.gg/FYaFRUwbYr)        |

To follow up on the previous LinkedIn publications, visit:

- [OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/company/106731439/).
- [Search for tag #OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/search/results/all/?keywords=%23openstudiolandscapes).

***

# Technical Reference

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

***

Last changed: **2025-12-23 13:35:00 UTC**