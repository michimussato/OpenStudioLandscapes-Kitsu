__all__ = [
    "DOCKER_USE_CACHE",
    "KITSUDB_INSIDE_CONTAINER",
    "GROUP",
    "KEY",
    "ASSET_HEADER",
    "FEATURE_CONFIGS",
]

import pathlib

from dagster import (
    AssetsDefinition,
    AssetKey,
    get_dagster_logger,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.base.ops import op_constants
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


constants = AssetsDefinition.from_op(
    op_constants,
    can_subset=False,
    group_name=GROUP,
    keys_by_input_name={
        "group_in": AssetKey([*ASSET_HEADER["key_prefix"], "group_in"]),
    },
    keys_by_output_name={
        "COMPOSE_SCOPE": AssetKey([*ASSET_HEADER["key_prefix"], "COMPOSE_SCOPE"]),
        "FEATURE_CONFIG": AssetKey([*ASSET_HEADER["key_prefix"], "FEATURE_CONFIG"]),
        "FEATURE_CONFIGS": AssetKey([*ASSET_HEADER["key_prefix"], "FEATURE_CONFIGS"]),
        "DOCKER_USE_CACHE": AssetKey([*ASSET_HEADER["key_prefix"], "DOCKER_USE_CACHE"]),
    },
)
