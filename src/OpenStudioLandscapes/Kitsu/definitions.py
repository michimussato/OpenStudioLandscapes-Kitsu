import os

from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Kitsu.assets
from OpenStudioLandscapes.Kitsu import (
    LOGGER,
    dist,
)

from OpenStudioLandscapes.Kitsu.configurable_resources.config_feature import config_feature

LOGGER.info(f"Loading {dist.name} assets...")


assets_base = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Kitsu.assets],
)
LOGGER.debug(f"{assets_base = }")


resources_base = {
    f"config_feature": config_feature,
}


defs = Definitions(
    assets=[
        *assets_base,
    ],
    resources={
        **resources_base,
    },
)
LOGGER.debug(f"{defs = }")
