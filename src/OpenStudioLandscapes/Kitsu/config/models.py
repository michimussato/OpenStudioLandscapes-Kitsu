import pathlib
import textwrap

from pydantic import (
    Field,
    EmailStr,
    field_validator, PositiveInt,
)

from dagster import get_dagster_logger

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.config.models import FeatureBaseModel
from OpenStudioLandscapes.Kitsu import dist


CONFIG_STR = textwrap.dedent(
    """
    # Base Information
    group_name: "Kitsu"
    key_prefixes:
      - "Kitsu"
    #    "__".join(context.asset_key_for_output("DOCKER_COMPOSE").path),
    #    "docker_compose",
    #    "docker-compose.yml",
    
    # The default Admin user name
    # Todo:
    #  - [x] Report Kitsu bug:
    #        https://github.com/cgwire/zou/issues/960
    #        Not OK:
    #        (env) root@kitsu:/opt/zou# zou create-admin --password openstudiolandscapes kitsu@openstudiolandscapes.com
    #        Email is not valid.
    #        OK:
    #        (env) root@kitsu:/opt/zou# zou create-admin --password openstudiolandscapes kitsu@openstudio.com
    #        Admin successfully created.
    ## Changing this value does not seem to have an effect
    #kitsu_admin_user: admin@example.com
    ## Changing this value does not seem to have an effect
    #kitsu_db_password: mysecretpassword
    kitsu_postgres_conf: "{DOT_FEATURES}/{FEATURE}/.payload/config/etc/postgresql/14/main/postgresql.conf"
    
    # https://zou.cg-wire.com/jobs/#enabling-job-queue
    kitsu_enable_job_queue: true
    kitsu_port_container: 80
    kitsu_port_host: 4545
    
    # Inside Landscape (ephemeral):
    kitsu_database_install_destination: "{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/data/kitsu"
    # In Landscapes root:
    #kitsu_database_install_destination: "{DOT_LANDSCAPES}/{DOT_SHARED_VOLUMES}/{GROUP}__{KEY}/data/kitsu"
    kitsu_preview_folder: /opt/zou/previews
    kitsu_secret_key: yourrandomsecretkey
    kitsu_tmp_dir: /opt/zou/tmp
    # these options will be dropped as they don't match the BaseModel
    illegal_option: "i will be ignored"
    ignored_option: "i will be ignored"
    
    # Todo
    #  - [ ] define arbitrary compose_scope here
    #compose_scope: default
    """
)


class Config(FeatureBaseModel):
    # config_str: str = CONFIG_STR

    feature_name: str = dist.name
    # compose_scope: str = "default"
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

    # EXPANDABLE PATHS
    @property
    def kitsu_postgres_conf_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")
            # return un-expanded path if `self.env` is None
            return self.kitsu_postgres_conf
        LOGGER.debug(f"Expanding {self.kitsu_postgres_conf}...")
        ret = pathlib.Path(
            self.kitsu_postgres_conf
            .expanduser()
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
            # return un-expanded path if `self.env` is None
            return self.kitsu_postgres_conf
        LOGGER.debug(f"Expanding {self.kitsu_database_install_destination}...")
        ret = pathlib.Path(
            self.kitsu_database_install_destination
            .expanduser()
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret

    # def export(self, destination: pathlib.Path):
    #
    #     with destination.open("w") as f:
    #         f.write(self.yaml(indent=2))
    #     return {
    #         "feature_name": self.feature_name,
    #     }

    # @field_validator("kitsu_postgres_conf")
    # @classmethod
    # def ensure_valid__kitsu_postgres_conf(cls, value: pathlib.PosixPath):
    #     if value.exists():
    #         return value
    #     else:
    #         raise ValueError(f"`kitsu_postgres_conf` ({value.as_posix()}) "
    #                          f"does not exist.")
