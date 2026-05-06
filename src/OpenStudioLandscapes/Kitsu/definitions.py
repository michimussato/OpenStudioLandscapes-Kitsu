import os

from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Kitsu.assets
from OpenStudioLandscapes.Kitsu import LOGGER, dist

LOGGER.info(f"Loading {dist.name} assets...")


assets_base = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Kitsu.assets],
)
LOGGER.debug(f"{assets_base = }")


defs = Definitions(
    assets=[
        *assets_base,
    ],
)
LOGGER.debug(f"{defs = }")
