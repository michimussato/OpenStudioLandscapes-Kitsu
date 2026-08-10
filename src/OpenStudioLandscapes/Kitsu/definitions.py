from dagster import (
    Definitions,
    load_assets_from_modules,
)
from OpenStudioLandscapes.engine.base.assets import group_out_base

from OpenStudioLandscapes.engine.base.configurable_resources.config_engine import config_ConfigEngineConfigurableResource
from OpenStudioLandscapes.engine.base.configurable_resources.env_resource import config_EnvConfigurableResource
from OpenStudioLandscapes.engine.base.configurable_resources.docker_resource import config_DockerConfigurableResource
from OpenStudioLandscapes.engine.base.configurable_resources.docker_registry_resource import config_DockerRegistryConfigurableResource

from OpenStudioLandscapes.Kitsu import (
    LOGGER,
    dist,
)
from OpenStudioLandscapes.Kitsu.configurable_resources.config_feature import config_feature
import OpenStudioLandscapes.Kitsu.assets

LOGGER.info(f"Loading {dist.name} assets...")

# The visualized DAG is cleaner when using `build_docker_image_spec`
# instead of `build_docker_image.specs` - yet they should be
# equivalent. However, `build_docker_image_spec` requires an
# `AssetSpec` object, which, in turn, only works on `multi_asset`.
# Bottom line: `build_docker_image.specs` might not look cleaner,
# it's probably way easier to maintain.

assets_base = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Kitsu.assets],
)
LOGGER.debug(f"{assets_base = }")

resources_base = {
    f"config_feature": config_feature,
}

assets_external = []
assets_external.extend(group_out_base.specs)

resources_external = {
    **resources_base,
    "config_EnvConfigurableResource": config_EnvConfigurableResource,
    "config_ConfigEngineConfigurableResource": config_ConfigEngineConfigurableResource,
    "config_DockerConfigurableResource": config_DockerConfigurableResource,
    "config_DockerRegistryConfigurableResource": config_DockerRegistryConfigurableResource,
}

defs = Definitions(
    assets=[
        *assets_base,
        *assets_external,
    ],
    resources={
        **resources_external,
    },
)
