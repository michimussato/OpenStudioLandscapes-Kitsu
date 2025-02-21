__all__ = [
    "DOCKER_USE_CACHE",
    "KITSUDB_INSIDE_CONTAINER",
    "GROUP",
    "KEY",
    "ASSET_HEADER",
    "ENVIRONMENT",
]

import pathlib
from OpenStudioLandscapes.engine.utils import *


DOCKER_USE_CACHE = False
KITSUDB_INSIDE_CONTAINER = False


GROUP = "Kitsu"
KEY = GROUP

ASSET_HEADER = {
    "group_name": GROUP,
    "key_prefix": [KEY],
    "compute_kind": "python",
}

# @formatter:off
ENVIRONMENT = {
    "CONFIGS_ROOT": pathlib.Path(
        get_git_root(pathlib.Path(__file__)),
        "configs",
        KEY,
    ).as_posix(),
}
# @formatter:on
