from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Kitsu.assets

assets_base = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Kitsu.assets],
)


defs = Definitions(
    assets=[
        *assets_base,
    ],
)
