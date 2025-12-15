__all__ = [
    "ASSET_HEADER",
]

from typing import List

from OpenStudioLandscapes.Kitsu import dist

# Todo
#  - [ ] fix this naive replacement logic
GROUP: str = dist.name.replace("-", "_")
KEY: List[str] = [GROUP]

ASSET_HEADER = {
    "group_name": GROUP,
    "key_prefix": KEY,
}
