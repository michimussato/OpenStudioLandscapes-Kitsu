import os

from dagster import (
    Definitions,
    load_assets_from_modules,
)
# from OpenStudioLandscapes.engine.logging.loggers import DISCOVERY_LOGGER as LOGGER

import logging as log
from logging.handlers import TimedRotatingFileHandler

try:
    # Place this before the third-party packages are imported!
    import logging.config as log_config

    from OpenStudioLandscapes.engine.logging.logging import LOGGING_SCHEMA

    log_config.dictConfig(LOGGING_SCHEMA)
except ImportError as e:
    # Todo:
    #  - [ ] make fail safe
    #        - [](https://runebook.dev/en/docs/python/library/logging.config/logging.config.dictConfig)
    raise ImportError(f"Could not import OpenStudioLandscapes Loggers: " f"{e}") from e

import OpenStudioLandscapes.Kitsu.assets
from OpenStudioLandscapes.Kitsu import dist, package, namespace
from OpenStudioLandscapes.engine.logging.logging import LOG_ROOT, FORMAT_CONSOLE, FORMAT_FILE, DATE_FMT, STYLE, PROPAGATE

FEATURE_LOGGER = log.getLogger(dist.name)

FEATURE_LOGGER.setLevel(os.environ.get("OPENSTUDIOLANDSCAPES__VERBOSITY"))
FEATURE_LOGGER.propagate = PROPAGATE

console_formatter = log.Formatter(fmt=FORMAT_CONSOLE, datefmt=DATE_FMT, style=STYLE)
file_formatter = log.Formatter(fmt=FORMAT_FILE, datefmt=DATE_FMT, style=STYLE)

file_handler = TimedRotatingFileHandler(
    filename=LOG_ROOT.joinpath(f"{dist.name}.log"),
    # mode='a',
    encoding='utf-8',
    when='midnight',
    interval=1,
    backupCount=7,
)
file_handler.setFormatter(file_formatter)

console_handler = log.StreamHandler()
console_handler.setFormatter(console_formatter)

FEATURE_LOGGER.addHandler(console_handler)
FEATURE_LOGGER.addHandler(file_handler)

FEATURE_LOGGER.critical(f"Loading Kitsu assets {dist.name}...")
FEATURE_LOGGER.critical(f"Loading Kitsu assets {package}...")
FEATURE_LOGGER.critical(f"Loading Kitsu assets {namespace}...")
# LOGGER.critical(f"Loading Kitsu assets...")
FEATURE_LOGGER.critical(f"Loading Kitsu assets...")

assets_base = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Kitsu.assets],
)


defs = Definitions(
    assets=[
        *assets_base,
    ],
)
