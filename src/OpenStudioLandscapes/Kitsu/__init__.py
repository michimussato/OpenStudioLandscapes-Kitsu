__all__ = [
    "namespace",
    "dist",
    "LOGGER",
    "__version__",
    "ASSET_HEADER",
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

    fill = 20

    LOGGER.info("%s: %s", "Distribution".ljust(fill), dist.name)
    LOGGER.info("%s: %s", "Namespace".ljust(fill), namespace)
    LOGGER.info("%s: %s", "Package".ljust(fill), package)
    LOGGER.info("%s: %s", "Version".ljust(fill), __version__)

    from OpenStudioLandscapes.engine.utils import (
        get_asset_header,
    )

    ASSET_HEADER = get_asset_header(
        dist=dist,
    )

    LOGGER.info("%s: %s", "ASSET_HEADER".ljust(fill), ASSET_HEADER)

except PackageNotFoundError:  # pragma: no cover
    __version__: str = "unknown"
finally:
    del version, PackageNotFoundError
