from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Kitsu.assets
import OpenStudioLandscapes.Kitsu.constants


assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Kitsu.assets],
)

constants = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Kitsu.constants],
)


defs = Definitions(
    assets=[
        *assets,
        *constants,
    ],
)
