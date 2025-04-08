__all__ = [
    "DOCKER_USE_CACHE",
    "KITSUDB_INSIDE_CONTAINER",
    "GROUP",
    "KEY",
    "ASSET_HEADER",
    "ENVIRONMENT",
    "COMPOSE_SCOPE",
]

import pathlib
from typing import Dict, Generator, MutableMapping

from dagster import (
    AssetExecutionContext,
    AssetMaterialization,
    MetadataValue,
    Output,
    asset,
)
from OpenStudioLandscapes.engine.constants import DOCKER_USE_CACHE_GLOBAL, THIRD_PARTY
from OpenStudioLandscapes.engine.utils import *

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
ENVIRONMENT: Dict = {
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
# @formatter:on

# Todo
#  - [ ] This is a bit hacky
#  - [ ] Externalize
_module = __name__
_parent = ".".join(_module.split(".")[:-1])
_definitions = ".".join([_parent, "definitions"])

COMPOSE_SCOPE = None
for i in THIRD_PARTY:
    if i["module"] == _definitions:
        COMPOSE_SCOPE = i["compose_scope"]
        break

if COMPOSE_SCOPE is None:
    raise Exception(
        "No compose_scope found for module '%s'." "Is the module enabled?" % _module
    )


@asset(
    **ASSET_HEADER,
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
