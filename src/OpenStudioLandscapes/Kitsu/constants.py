__all__ = [
    "DOCKER_USE_CACHE",
    "KITSUDB_INSIDE_CONTAINER",
    "GROUP",
    "KEY",
    "ASSET_HEADER",
    "FEATURE_CONFIGS",
]

import pathlib
from typing import Generator, MutableMapping

from dagster import (
    AssetExecutionContext,
    AssetMaterialization,
    MetadataValue,
    Output,
    AssetOut,
    AssetIn,
    AssetKey,
    multi_asset,
    get_dagster_logger,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.constants import DOCKER_USE_CACHE_GLOBAL
from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.enums import OpenStudioLandscapesConfig, ComposeScope
from OpenStudioLandscapes.engine.base.assets import KEY_BASE

DOCKER_USE_CACHE = DOCKER_USE_CACHE_GLOBAL or False
KITSUDB_INSIDE_CONTAINER = False


GROUP = "Kitsu"
KEY = [GROUP]
FEATURE = f"OpenStudioLandscapes-{GROUP}"

ASSET_HEADER = {
    "group_name": GROUP,
    "key_prefix": KEY,
}

# @formatter:off
FEATURE_CONFIGS = {
    OpenStudioLandscapesConfig.DEFAULT: {
        "DOCKER_USE_CACHE": DOCKER_USE_CACHE,
        # "CONFIGS_ROOT": pathlib.Path(
        #     get_git_root(pathlib.Path(__file__)),
        #     ".payload",
        #     "config",
        # )
        # .expanduser()
        # .as_posix(),
        # Todo:
        #  - [ ] These have no effect yet
        "KITSU_HOSTNAME": "kitsu",
        "KITSU_ADMIN_USER": "michimussato@gmail.com",
        "KITSU_DB_PASSWORD": "myp4ssword",
        "KITSU_SECRET_KEY": "yourrandomsecretkey",
        "KITSU_PREVIEW_FOLDER": "/opt/zou/previews",
        "KITSU_TMP_DIR": "/opt/zou/tmp",
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


@multi_asset(
    name=f"constants_{GROUP}",
    ins={"group_in": AssetIn(AssetKey([*KEY_BASE, "group_out"]))},
    outs={
        "COMPOSE_SCOPE": AssetOut(
            **ASSET_HEADER,
            dagster_type=ComposeScope,
            description="",
        ),
        "FEATURE_CONFIG": AssetOut(
            **ASSET_HEADER,
            dagster_type=OpenStudioLandscapesConfig,
            description="",
        ),
        "FEATURE_CONFIGS": AssetOut(
            **ASSET_HEADER,
            dagster_type=dict,
            description="",
        ),
        "DOCKER_USE_CACHE": AssetOut(
            **ASSET_HEADER,
            dagster_type=bool,
            description="",
        ),
    },
)
def constants(
    context: AssetExecutionContext,
    group_in: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[MutableMapping] | AssetMaterialization, None, None]:
    """ """

    features = group_in["features"]

    # COMPOSE_SCOPE
    COMPOSE_SCOPE = get_compose_scope(
        context=context,
        features=features,
        name=__name__,
    )

    # FEATURE_CONFIG
    FEATURE_CONFIG = get_feature_config(
        context=context,
        features=features,
        name=__name__,
    )

    yield Output(
        output_name="COMPOSE_SCOPE",
        value=COMPOSE_SCOPE,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("COMPOSE_SCOPE"),
        metadata={
            "__".join(
                context.asset_key_for_output("COMPOSE_SCOPE").path
            ): MetadataValue.json(COMPOSE_SCOPE),
        },
    )

    yield Output(
        output_name="FEATURE_CONFIG",
        value=FEATURE_CONFIG,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("FEATURE_CONFIG"),
        metadata={
            "__".join(
                context.asset_key_for_output("FEATURE_CONFIG").path
            ): MetadataValue.json(FEATURE_CONFIG),
        },
    )

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
        output_name="DOCKER_USE_CACHE",
        value=DOCKER_USE_CACHE,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("DOCKER_USE_CACHE"),
        metadata={
            "__".join(
                context.asset_key_for_output("DOCKER_USE_CACHE").path
            ): MetadataValue.bool(DOCKER_USE_CACHE),
        },
    )
