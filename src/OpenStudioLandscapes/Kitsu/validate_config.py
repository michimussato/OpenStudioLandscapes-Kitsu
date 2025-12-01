import pathlib

from pydantic import BaseModel

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
