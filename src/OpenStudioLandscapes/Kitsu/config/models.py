import pathlib
from typing import List

from dagster import get_dagster_logger
from pydantic import (
    EmailStr,
    Field,
    PositiveInt,
    field_validator,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.config.models import FeatureBaseModel

from OpenStudioLandscapes.Kitsu import constants, dist


class Config(FeatureBaseModel):
    feature_name: str = dist.name

    group_name: str = constants.ASSET_HEADER["group_name"]

    key_prefixes: List[str] = constants.ASSET_HEADER["key_prefix"]

    docker_image: str = Field(
        default="docker.io/cgwire/cgwire:1.0.11",
        description="The Docker image to use",
    )

    kitsu_admin_user: EmailStr = Field(
        default="admin@example.com",
        description="Bug Report: https://github.com/cgwire/zou/issues/960); "
        "Changing these values does not seem to have an effect Hence, they are locked to the following values for now.",
        frozen=True,
    )
    # kitsu_db_password: SecretStr
    # The above exception was caused by the following exception:
    # AttributeError: 'str' object has no attribute 'get_secret_value'
    kitsu_db_password: str = Field(
        default="mysecretpassword",
        description="The Postgres database password.",
        frozen=True,
    )
    kitsu_postgres_conf: pathlib.Path = Field(
        description="The Kitsu Postgres configuration file.",
        default=pathlib.Path(
            "{DOT_FEATURES}/{FEATURE}/.payload/config/etc/postgresql/14/main/postgresql.conf"
        ),
    )
    kitsu_enable_job_queue: bool = Field(
        description="Enable Kitsu Job Queue?",
        default=True,
    )
    kitsu_port_container: PositiveInt = Field(
        default=80,
        description="The Kitsu container port.",
        frozen=True,
    )
    kitsu_port_host: PositiveInt = Field(
        default=4545,
        description="The Kitsu host port.",
        frozen=False,
    )
    kitsu_db_inside_container: bool = Field(
        default=False,
        description="The Kitsu database inside container; the database will "
        "not be persistent. Helpful for testing.",
    )
    kitsu_database_install_destination: pathlib.Path = Field(
        description="The host side Kitsu database installation destination.",
        default=pathlib.Path("{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/data/postgresql"),
    )
    kitsu_preview_folder: pathlib.Path = Field(
        description="The Kitsu Preview folder (/opt/zou/previews).",
        default=pathlib.Path("{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/data/previews"),
    )
    kitsu_tmp_dir: pathlib.Path = Field(
        description="Kitsu TMP directory (/opt/zou/tmp).",
        default=pathlib.Path("{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/data/tmp"),
    )
    kitsu_db_dump: pathlib.Path = Field(
        description="Kitsu TMP directory (/opt/zou/db_dump). "
                    "This can be used to "
                    "`bash -c 'cd /opt/zou/db_dump && /opt/zou/env/bin/zou dump-database'` "
                    "to.",
        default=pathlib.Path("{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/data/db_dump"),
    )
    kitsu_secret_key: str = Field(
        description="Kitsu Secret Key.",
        default="yourrandomsecretkey",
    )

    # Todo
    #  - [ ] default equals empty list results in a Pydantic error
    # apt_packages: List = Field(
    #     default=[
    #     ],
    #     frozen=True,
    # )

    pip_packages: List[str] = Field(
        default=[
            "boto3",
        ],
        description="`boto3` is required if `kitsu_enable_job_queue` is `true`. [Reference](https://zou.cg-wire.com/jobs/)",
        frozen=True,
    )

    @field_validator("kitsu_admin_user")
    @classmethod
    def ensure_valid__kitsu_admin_user(cls, value: str):
        if value == "admin@example.com":
            return value
        else:
            raise ValueError(
                "`kitsu_admin_user` (as the initial default) "
                "must be `admin@example.com` for now. Other "
                "values will render Kitsu inoperable"
            )

    @field_validator("kitsu_db_password")
    @classmethod
    def ensure_valid__kitsu_db_password(cls, value: str):
        if value == "mysecretpassword":
            return value
        else:
            raise ValueError(
                "`kitsu_db_password` (as the initial default) "
                "must be `mysecretpassword` for now. Other "
                "values will render Kitsu inoperable"
            )

    @field_validator("kitsu_port_container")
    @classmethod
    def ensure_valid__kitsu_port_container(cls, value: int):
        if value == 80:
            return value
        else:
            raise ValueError(
                "`kitsu_port_container` must be set "
                "to 80 for now. Other values will render Kitsu inoperable."
            )

    # EXPANDABLE PATHS
    @property
    def kitsu_postgres_conf_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")

        LOGGER.debug(f"Expanding {self.kitsu_postgres_conf}...")
        ret = pathlib.Path(
            self.kitsu_postgres_conf.expanduser()  # pylint: disable=E1101
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret

    @property
    def kitsu_database_install_destination_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")

        LOGGER.debug(f"Expanding {self.kitsu_database_install_destination}...")
        ret = pathlib.Path(
            self.kitsu_database_install_destination.expanduser()  # pylint: disable=E1101
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret

    @property
    def kitsu_preview_folder_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")

        LOGGER.debug(f"Expanding {self.kitsu_preview_folder}...")
        ret = pathlib.Path(
            self.kitsu_preview_folder.expanduser()  # pylint: disable=E1101
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret

    @property
    def kitsu_tmp_dir_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")

        LOGGER.debug(f"Expanding {self.kitsu_tmp_dir}...")
        ret = pathlib.Path(
            self.kitsu_tmp_dir.expanduser()  # pylint: disable=E1101
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret

    @property
    def kitsu_db_dump_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")

        LOGGER.debug(f"Expanding {self.kitsu_db_dump}...")
        ret = pathlib.Path(
            self.kitsu_db_dump.expanduser()  # pylint: disable=E1101
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret


CONFIG_STR = Config.get_docs()
