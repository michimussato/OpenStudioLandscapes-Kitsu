from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Kitsu.assets


assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Kitsu.assets],
)


defs = Definitions(
    assets=[
        *assets,
    ],
)
