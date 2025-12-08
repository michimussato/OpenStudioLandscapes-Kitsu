import pathlib

from pydantic import (
    Field,
    EmailStr,
    # SecretStr,
    field_validator, PositiveInt,
)

from OpenStudioLandscapes.engine.config.models import FeatureBaseModel
from OpenStudioLandscapes.Kitsu.config import dist


class Config(FeatureBaseModel):
    feature_name: str = dist.name
    compose_scope: str = "default"
    definitions: str = "OpenStudioLandscapes.Kitsu.definitions"

    kitsu_admin_user: EmailStr = Field(
        default="admin@example.com",
        description="The Kitsu Admin Email.",
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
    kitsu_postgres_conf: pathlib.Path = Field(description="The Kitsu Postgres configuration file.")
    kitsu_enable_job_queue: bool = Field(description="Enable Kitsu Job Queue?")
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
    kitsu_database_install_destination: pathlib.Path = Field()
    kitsu_db_inside_container: bool = Field(
        default=False,
        description="The Kitsu database inside container; the database will not be persistent. "
                    "Helpful for testing.",
    )
    kitsu_preview_folder: pathlib.Path = Field(description="The Kitsu Preview folder.")
    kitsu_secret_key: str = Field(description="Kitsu Secret Key.")
    kitsu_tmp_dir: pathlib.Path = Field(description="Kitsu TMP directory.")

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

    # @field_validator("kitsu_postgres_conf")
    # @classmethod
    # def ensure_valid__kitsu_postgres_conf(cls, value: pathlib.PosixPath):
    #     if value.exists():
    #         return value
    #     else:
    #         raise ValueError(f"`kitsu_postgres_conf` ({value.as_posix()}) "
    #                          f"does not exist.")
