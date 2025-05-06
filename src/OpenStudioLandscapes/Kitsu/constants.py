__all__ = [
    "DOCKER_USE_CACHE",
    "KITSUDB_INSIDE_CONTAINER",
    "ASSET_HEADER",
    "FEATURE_CONFIGS",
]

import pathlib
from pathlib import Path
from typing import Generator, MutableMapping, Any

from dagster import (
    multi_asset,
    AssetOut,
    AssetMaterialization,
    AssetExecutionContext,
    Output,
    MetadataValue,
    get_dagster_logger,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.constants import DOCKER_USE_CACHE_GLOBAL
from OpenStudioLandscapes.engine.enums import OpenStudioLandscapesConfig

DOCKER_USE_CACHE = DOCKER_USE_CACHE_GLOBAL or False
KITSUDB_INSIDE_CONTAINER = False


GROUP = "Kitsu"
KEY = [GROUP]
FEATURE = f"OpenStudioLandscapes-{GROUP}"

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
        # https://zou.cg-wire.com/jobs/#enabling-job-queue
        # Todo:
        #  - [ ] Job Queue
        #        https://github.com/michimussato/kitsu-setup/blob/main/README_KITSU.md#zou-job-queue
        "KITSU_ENABLE_JOB_QUEUE": False,
        "KITSU_HOSTNAME": "kitsu",
        # Todo:
        #  - [ ] Report Kitsu bug:
        #        Not OK:
        #        (env) root@kitsu:/opt/zou# zou create-admin --password openstudiolandscapes kitsu@openstudiolandscapes.com
        #        Email is not valid.
        #        OK:
        #        (env) root@kitsu:/opt/zou# zou create-admin --password openstudiolandscapes kitsu@openstudio.com
        #        Admin successfully created.
        "KITSU_ADMIN_USER": "admin@example.com",
        "KITSU_DB_PASSWORD": "mysecretpassword",
        "KITSU_SECRET_KEY": "yourrandomsecretkey",
        "KITSU_PREVIEW_FOLDER": "/opt/zou/previews",  # Default: "/opt/zou/previews"
        "KITSU_TMP_DIR": "/opt/zou/tmp",  # Default: "/opt/zou/tmp"
        "KITSU_PORT_HOST": "4545",
        "KITSU_PORT_CONTAINER": "80",
        f"KITSU_POSTGRES_CONF": pathlib.Path(
            # /etc/postgresql/14/main/postgresql.conf
            # get_configs_root(pathlib.Path(__file__)),
            pathlib.Path(__file__).parent.parent.parent.parent / ".payload" / "config",
            "etc",
            "postgresql",
            "14",
            "main",
            "postgresql.conf",
        )
        .expanduser()
        .as_posix(),
        "KITSU_DATABASE_INSTALL_DESTINATION": {
            #################################################################
            # Kitsu Postgresql DB will be created in (hardcoded):
            #################################################################
            #################################################################
            # Inside Landscape:
            "default": pathlib.Path(
                "{DOT_LANDSCAPES}",
                "{LANDSCAPE}",
                f"{GROUP}__{'__'.join(KEY)}",
                "data",
                "kitsu",
            )
            .expanduser()
            .as_posix(),
            #################################################################
            # # Prod DB:
            # "prod_db": pathlib.Path(
            #     "{NFS_ENTRY_POINT}",
            #     "services",
            #     "kitsu",
            # ).as_posix(),
            # #################################################################
            # # Test DB:
            # "test_db": pathlib.Path(
            #     "{NFS_ENTRY_POINT}",
            #     "test_data",
            #     "10.2",
            #     "kitsu",
            # ).as_posix(),
        }["default"],
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
