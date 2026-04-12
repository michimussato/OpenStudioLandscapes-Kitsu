from dagster import Definitions
from OpenStudioLandscapes.engine.base.assets import group_out_base

from OpenStudioLandscapes.Kitsu.definitions import assets_base

assets_external = []
assets_external.extend(group_out_base.specs)


defs = Definitions(
    assets=[
        *assets_base,
        *assets_external,
    ],
)
