from dagster import Definitions
from OpenStudioLandscapes.engine.base.assets import group_out_base

from OpenStudioLandscapes.engine.base.configurable_resources.config_engine import config_ConfigEngineConfigurableResource
from OpenStudioLandscapes.engine.base.configurable_resources.env_resource import config_EnvConfigurableResource
from OpenStudioLandscapes.engine.base.configurable_resources.docker_resource import config_DockerConfigurableResource
from OpenStudioLandscapes.engine.base.configurable_resources.docker_registry_resource import config_DockerRegistryConfigurableResource

# from OpenStudioLandscapes.Kitsu import LOGGER

# from OpenStudioLandscapes.Kitsu import dist
from OpenStudioLandscapes.Kitsu.definitions import assets_base
from OpenStudioLandscapes.Kitsu.definitions import resources_base

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
