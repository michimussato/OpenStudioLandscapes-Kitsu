__all__ = [
    "DOCKER_USE_CACHE",
    "KITSUDB_INSIDE_CONTAINER",
    "GROUP",
    "KEY",
    "ASSET_HEADER",
]


DOCKER_USE_CACHE = False
KITSUDB_INSIDE_CONTAINER = False


GROUP = "Kitsu"
KEY = GROUP

ASSET_HEADER = {
    "group_name": GROUP,
    "key_prefix": [KEY],
    "compute_kind": "python",
}
