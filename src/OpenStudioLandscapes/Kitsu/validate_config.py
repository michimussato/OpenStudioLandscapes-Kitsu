import pathlib

from pydantic import BaseModel, field_validator

class Config(BaseModel):
    kitsu_admin_user: str
    kitsu_postgres_conf: pathlib.Path
    kitsu_db_password: str
    kitsu_enable_job_queue: bool
    kitsu_port_container: int
    kitsu_port_host: int
    kitsu_database_install_destination: pathlib.Path
    kitsu_preview_folder: pathlib.Path
    kitsu_secret_key: str
    kitsu_tmp_dir: pathlib.Path

    @field_validator("kitsu_admin_user")
    @classmethod
    def ensure_valid__kitsu_admin_user(cls, value: str):
        if value == "admin@example.com":
            return value
        else:
            raise ValueError("`kitsu_admin_user` (as the initial default) "
                             "must be `admin@example.com` for now. Other "
                             "values will render Kitsu inoperable")

    @field_validator("kitsu_db_password")
    @classmethod
    def ensure_valid__kitsu_db_password(cls, value: str):
        if value == "mysecretpassword":
            return value
        else:
            raise ValueError("`kitsu_db_password` (as the initial default) "
                             "must be `mysecretpassword` for now. Other "
                             "values will render Kitsu inoperable")

    @field_validator("kitsu_port_container")
    @classmethod
    def ensure_valid__kitsu_port_container(cls, value: int):
        if value == 80:
            return value
        else:
            raise ValueError("`kitsu_port_container` must be set "
                             "to 80 for now. Other values will render Kitsu inoperable.")

    @field_validator("kitsu_postgres_conf")
    @classmethod
    def ensure_valid__kitsu_postgres_conf(cls, value: pathlib.PosixPath):
        if value.exists():
            return value
        else:
            raise ValueError(f"`kitsu_postgres_conf` ({value.as_posix()}) "
                             f"does not exist.")