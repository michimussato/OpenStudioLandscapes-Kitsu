__all__ = [
    "DOCKER_USE_CACHE",
    "KITSUDB_INSIDE_CONTAINER",
    "GROUP",
    "KEY",
    "ASSET_HEADER",
    "ENVIRONMENT",
]

import pathlib
from typing import Generator, MutableMapping

from dagster import (
    asset,
    Output,
    AssetMaterialization,
    MetadataValue,
    AssetExecutionContext,
)

from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.constants import DOCKER_USE_CACHE_GLOBAL


DOCKER_USE_CACHE = DOCKER_USE_CACHE_GLOBAL or False
KITSUDB_INSIDE_CONTAINER = False


GROUP = "Kitsu"
KEY = [GROUP]

ASSET_HEADER = {
    "group_name": GROUP,
    "key_prefix": KEY,
    "compute_kind": "python",
}

# @formatter:off
ENVIRONMENT = {
    "DOCKER_USE_CACHE": DOCKER_USE_CACHE,
    # Todo:
    #  - [ ] These have no effect yet
    "KITSU_ADMIN_USER": "michimussato@gmail.com",
    "KITSU_DB_PASSWORD": "myp4ssword",
    "KITSU_SECRET_KEY": "yourrandomsecretkey",
    "KITSU_PREVIEW_FOLDER": "/opt/zou/previews",
    "KITSU_TMP_DIR": "/opt/zou/tmp",
    "KITSU_PORT_HOST": "4545",
    "KITSU_PORT_CONTAINER": "80",
    # /etc/postgresql/14/main/postgresql.conf
    f"KITSU_POSTGRES_CONF": pathlib.Path(
        get_git_root(pathlib.Path(__file__)),
        "configs",
        "__".join(KEY),
        "etc",
        "postgresql",
        "14",
        "main",
        "postgresql.conf",
    )
    .expanduser()
    .as_posix(),
    f"KITSU_TEMPLATE_DB_14": pathlib.Path(
        get_git_root(pathlib.Path(__file__)),
        "data",
        "__".join(KEY),
        "postgres",
        "template_dbs",
        "14",
        "main"
    )
    .expanduser()
    .as_posix(),

    "KITSU_DATABASE_INSTALL_DESTINATION": {
        #################################################################
        # Kitsu Postgresql DB will be created in (hardcoded):
        # "KITSU_DATABASE_INSTALL_DESTINATION" / "postgresql" / "14" / "main"
        # Kitsu Previews folder will be created in (hardcoded):
        # "KITSU_DATABASE_INSTALL_DESTINATION" / "previews"
        #################################################################
        #################################################################
        # Inside Landscape:
        "default": pathlib.Path(
            "{DOT_LANDSCAPES}",
            "{LANDSCAPE}",
            f"{GROUP}__{'__'.join(KEY)}",
            "data",
            "kitsu",
        ).as_posix(),
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
# @formatter:on


@asset(
    name=f"constants_{GROUP}",
    group_name="Constants",
    key_prefix=KEY,
    compute_kind="python",
    description="",
)
def constants(
    context: AssetExecutionContext,
) -> Generator[Output[MutableMapping] | AssetMaterialization, None, None]:
    """ """

    _constants = dict()

    _constants["DOCKER_USE_CACHE"] = DOCKER_USE_CACHE
    _constants["ASSET_HEADER"] = ASSET_HEADER
    _constants["ENVIRONMENT"] = ENVIRONMENT

    yield Output(_constants)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(_constants),
        },
    )
