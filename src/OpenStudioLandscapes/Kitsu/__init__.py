__all__ = [
    "namespace",
    "dist",
    "LOGGER",
    "__version__",
    "constants",
    "config",
]

import sys
from importlib import metadata
from pathlib import Path

if sys.version_info[:2] >= (3, 11):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import (  # pragma: no cover
        Distribution,
        PackageNotFoundError,
        version,
    )
else:
    raise RuntimeError("Python version >= 3.11 required.")

try:
    # Change here if project is renamed and does not equal the package name
    namespace: str = Path(__file__).parent.parent.name
    # OpenStudioLandscapes
    package: str = Path(__file__).parent.name
    # NukeRLM_8
    dist: Distribution = metadata.distribution(".".join((namespace, package)))

    # difference to dist.version?
    __version__: str = version(dist.name)

    from OpenStudioLandscapes.engine.logging.loggers import get_feature_logger

    LOGGER = get_feature_logger(dist=dist)

    LOGGER.info("Distribution: %s", dist.name)
    LOGGER.info("Namespace:    %s", namespace)
    LOGGER.info("Package:      %s", package)
    LOGGER.info("Version:      %s", __version__)

except PackageNotFoundError:  # pragma: no cover
    __version__: str = "unknown"
finally:
    del version, PackageNotFoundError
