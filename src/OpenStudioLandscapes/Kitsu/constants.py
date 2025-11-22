__all__ = [
    "DOCKER_USE_CACHE",
    "KITSUDB_INSIDE_CONTAINER",
    "ASSET_HEADER",
    "FEATURE_CONFIGS",
]

import pathlib
from pathlib import Path
from typing import Any, Generator, MutableMapping

from dagster import (
    AssetExecutionContext,
    AssetMaterialization,
    AssetOut,
    MetadataValue,
    Output,
    get_dagster_logger,
    multi_asset,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.constants import DOCKER_USE_CACHE_GLOBAL
from OpenStudioLandscapes.engine.enums import (
    FeatureVolumeType,
    OpenStudioLandscapesConfig,
)

DOCKER_USE_CACHE = DOCKER_USE_CACHE_GLOBAL or False
KITSUDB_INSIDE_CONTAINER = False


GROUP = "Kitsu"
KEY = [GROUP]
FEATURE = f"OpenStudioLandscapes-{GROUP}".replace("_", "-")

ASSET_HEADER = {
    "group_name": GROUP,
    "key_prefix": KEY,
}

# Todo:
#  - [ ] Integrate into readme_generator
DOCUMENTATION = [
    "https://github.com/cgwire/kitsu-docker",
]

# @formatter:off
FEATURE_CONFIGS = {
    OpenStudioLandscapesConfig.DEFAULT: {
        "DOCKER_USE_CACHE": DOCKER_USE_CACHE,
        # https://zou.cg-wire.com/
        # "LC_ALL": "C.UTF-8",
        # "LANG": "C.UTF-8",
        "OPENSTUDIOLANDSCAPES_KITSU__HOSTNAME": "kitsu",
        # https://zou.cg-wire.com/jobs/#enabling-job-queue
        "OPENSTUDIOLANDSCAPES_KITSU__ENABLE_JOB_QUEUE": True,
        # Todo:
        #  - [x] Report Kitsu bug:
        #        https://github.com/cgwire/zou/issues/960
        #        Not OK:
        #        (env) root@kitsu:/opt/zou# zou create-admin --password openstudiolandscapes kitsu@openstudiolandscapes.com
        #        Email is not valid.
        #        OK:
        #        (env) root@kitsu:/opt/zou# zou create-admin --password openstudiolandscapes kitsu@openstudio.com
        #        Admin successfully created.
        "OPENSTUDIOLANDSCAPES_KITSU__ADMIN_USER": "admin@example.com",
        "OPENSTUDIOLANDSCAPES_KITSU__DB_PASSWORD": "mysecretpassword",
        "OPENSTUDIOLANDSCAPES_KITSU__SECRET_KEY": "yourrandomsecretkey",
        "OPENSTUDIOLANDSCAPES_KITSU__PREVIEW_FOLDER": "/opt/zou/previews",  # Default: "/opt/zou/previews"
        "OPENSTUDIOLANDSCAPES_KITSU__TMP_DIR": "/opt/zou/tmp",  # Default: "/opt/zou/tmp"
        "OPENSTUDIOLANDSCAPES_KITSU__PORT_HOST": "4545",
        "OPENSTUDIOLANDSCAPES_KITSU__PORT_CONTAINER": "80",
        f"OPENSTUDIOLANDSCAPES_KITSU__POSTGRES_CONF": pathlib.Path(
            # /etc/postgresql/14/main/postgresql.conf
            "{DOT_FEATURES}",
            FEATURE,
            ".payload",
            "config",
            "etc",
            "postgresql",
            "14",
            "main",
            "postgresql.conf",
        )
        .expanduser()
        .as_posix(),
        "OPENSTUDIOLANDSCAPES_KITSU__DATABASE_INSTALL_DESTINATION": {
            #################################################################
            # Kitsu Postgresql DB will be created in (hardcoded):
            #################################################################
            #################################################################
            # Inside Landscape:
            FeatureVolumeType.CONTAINED: pathlib.Path(
                "{DOT_LANDSCAPES}",
                "{LANDSCAPE}",
                f"{GROUP}__{'__'.join(KEY)}",
                "data",
                "kitsu",
            )
            .expanduser()
            .as_posix(),
            #################################################################
            # In Landscapes root:
            FeatureVolumeType.SHARED: pathlib.Path(
                "{DOT_LANDSCAPES}",
                "{DOT_SHARED_VOLUMES}",
                f"{GROUP}__{'__'.join(KEY)}",
                "data",
                "kitsu",
            )
            .expanduser()
            .as_posix(),
        }[FeatureVolumeType.CONTAINED],
    }
}
# @formatter:on


# Todo:
#  - [ ] move to common_assets
@multi_asset(
    name=f"constants_{GROUP}",
    outs={
        "NAME": AssetOut(
            **ASSET_HEADER,
            dagster_type=str,
            description="",
        ),
        "FEATURE_CONFIGS": AssetOut(
            **ASSET_HEADER,
            dagster_type=dict,
            description="",
        ),
        "DOCKER_COMPOSE": AssetOut(
            **ASSET_HEADER,
            dagster_type=pathlib.Path,
            description="",
        ),
    },
)
def constants_multi_asset(
    context: AssetExecutionContext,
) -> Generator[
    Output[
        MutableMapping[
            OpenStudioLandscapesConfig, MutableMapping[str | Any, bool | str | Any]
        ]
    ]
    | AssetMaterialization
    | Output[Any]
    | Output[Path]
    | Any,
    None,
    None,
]:
    """ """

    yield Output(
        output_name="FEATURE_CONFIGS",
        value=FEATURE_CONFIGS,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("FEATURE_CONFIGS"),
        metadata={
            "__".join(
                context.asset_key_for_output("FEATURE_CONFIGS").path
            ): MetadataValue.json(FEATURE_CONFIGS),
        },
    )

    yield Output(
        output_name="NAME",
        value=__name__,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("NAME"),
        metadata={
            "__".join(context.asset_key_for_output("NAME").path): MetadataValue.path(
                __name__
            ),
        },
    )

    docker_compose = pathlib.Path(
        "{DOT_LANDSCAPES}",
        "{LANDSCAPE}",
        f"{ASSET_HEADER['group_name']}__{'_'.join(ASSET_HEADER['key_prefix'])}",
        "__".join(context.asset_key_for_output("DOCKER_COMPOSE").path),
        "docker_compose",
        "docker-compose.yml",
    )

    yield Output(
        output_name="DOCKER_COMPOSE",
        value=docker_compose,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("DOCKER_COMPOSE"),
        metadata={
            "__".join(
                context.asset_key_for_output("DOCKER_COMPOSE").path
            ): MetadataValue.path(docker_compose),
        },
    )
