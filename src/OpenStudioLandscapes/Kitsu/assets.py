import copy
import json
import pathlib
import shutil
import textwrap
import urllib.parse
from typing import Any, Generator, List, MutableMapping

import OpenStudioLandscapes.engine.discovery.discovery as discovery
import yaml
from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetKey,
    AssetMaterialization,
    MetadataValue,
    Output,
    asset,
)
from OpenStudioLandscapes.engine.common_assets.compose import get_compose
from OpenStudioLandscapes.engine.common_assets.docker_compose_graph import (
    get_docker_compose_graph,
)
from OpenStudioLandscapes.engine.common_assets.feature_out import get_feature_out
from OpenStudioLandscapes.engine.common_assets.group_in import get_group_in
from OpenStudioLandscapes.engine.common_assets.group_out import get_group_out
from OpenStudioLandscapes.engine.config.models import ConfigEngine, DockerConfigModel
from OpenStudioLandscapes.engine.constants import *
from OpenStudioLandscapes.engine.discovery.get_feature_base_model import (
    get_feature_base_model,
)
from OpenStudioLandscapes.engine.enums import *
from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.utils.docker.compose_dicts import *

from OpenStudioLandscapes.Kitsu import dist
from OpenStudioLandscapes.Kitsu.config.models import CONFIG_STR, Config
from OpenStudioLandscapes.Kitsu.constants import *

group_in = get_group_in(
    ASSET_HEADER=ASSET_HEADER,
    ASSET_HEADER_PARENT=ASSET_HEADER_BASE,
    input_name=str(GroupIn.BASE_IN),
)


group_out = get_group_out(
    ASSET_HEADER=ASSET_HEADER,
)


docker_compose_graph = get_docker_compose_graph(
    ASSET_HEADER=ASSET_HEADER,
)


compose = get_compose(
    ASSET_HEADER=ASSET_HEADER,
)


feature_out = get_feature_out(
    ASSET_HEADER=ASSET_HEADER,
    feature_out_ins={
        "compose": dict,
        "group_in": dict,
        "CONFIG": discovery.FeatureBaseModel,
    },
)


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
)
def compose_networks(
    context: AssetExecutionContext,
    CONFIG: discovery.FeatureBaseModel,
) -> Generator[
    Output[MutableMapping[str, MutableMapping[str, MutableMapping[str, str]]]]
    | AssetMaterialization,
    None,
    None,
]:

    env: dict = CONFIG.env

    compose_network_mode = DockerComposePolicies.NETWORK_MODE.BRIDGE

    docker_dict = get_network_dicts(
        context=context,
        compose_network_mode=compose_network_mode,
        env=env,
    )

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "compose_network_mode": MetadataValue.text(compose_network_mode.value),
            "docker_yaml": MetadataValue.md(f"```shell\n{docker_yaml}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "group_in": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "group_in"]),
        ),
    },
    description=textwrap.dedent(
        f"""
Reads options from a custom `config.yml`.
If the custom `config.yml` does not exist, it 
will be created locally containing default options.

---

For reference, the default `config.yml` looks as follows:
        
```yaml
{CONFIG_STR}
```
"""
    ),
)
def CONFIG(
    context: AssetExecutionContext,
    group_in: dict,  # pylint: disable=redefined-outer-name
) -> Generator[
    Output[discovery.FeatureBaseModel] | AssetMaterialization,
    None,
    None,
]:

    env: dict = group_in.pop("env")

    config_validated: discovery.FeatureBaseModel = get_feature_base_model(
        context=context,
        discovered_models=discovery.DISCOVERED_MODELS,
        search_instance_type=Config,
    )

    config_validated.env = env

    yield Output(config_validated)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.md(
                f"```yaml\n{yaml.safe_dump(json.loads(config_validated.model_dump_json(fallback=str, indent=2)))}\n```"
            ),
        },
    )


@asset(
    **ASSET_HEADER,
)
def apt_packages(
    context: AssetExecutionContext,
) -> Generator[
    Output[MutableMapping[str, List[str]]] | AssetMaterialization, None, None
]:
    """ """

    _apt_packages = {}

    _apt_packages["base"] = [
        "sudo",
        "htop",
        "curl",
        "ffmpeg",
    ]

    yield Output(_apt_packages)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(_apt_packages),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
    description=textwrap.dedent(
        """
        `boto3` is required if `kitsu_enable_job_queue` is `true`.
        
        Reference:
        - [https://zou.cg-wire.com/jobs/]()
        """
    ),
)
def pip_packages(
    context: AssetExecutionContext,
    CONFIG: discovery.FeatureBaseModel,  # pylint: disable=redefined-outer-name
) -> Generator[Output[list] | AssetMaterialization, None, None]:

    _pip_packages: list = []

    if CONFIG.kitsu_enable_job_queue:

        _pip_packages.extend(
            [
                "boto3",
            ]
        )

    yield Output(_pip_packages)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(_pip_packages),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "group_in": AssetIn(AssetKey([*ASSET_HEADER["key_prefix"], "group_in"])),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
        "apt_packages": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "apt_packages"]),
        ),
        "pip_packages": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "pip_packages"]),
        ),
        "script_init_db": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "script_init_db"]),
        ),
        "inject_postgres_conf": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "inject_postgres_conf"]),
        ),
    },
)
def build_docker_image(
    context: AssetExecutionContext,
    group_in: dict,  # pylint: disable=redefined-outer-name
    CONFIG: discovery.FeatureBaseModel,  # pylint: disable=redefined-outer-name
    apt_packages: dict[str, list[str]],  # pylint: disable=redefined-outer-name
    pip_packages: list,  # pylint: disable=redefined-outer-name
    script_init_db: pathlib.Path,  # pylint: disable=redefined-outer-name
    inject_postgres_conf: pathlib.Path,  # pylint: disable=redefined-outer-name
) -> Generator[Output[MutableMapping] | AssetMaterialization, None, None]:
    """ """

    # Todo
    #  - [ ] Can we integrate into CONFIG?
    #        - group_in.pop("docker_config_json")
    #        - group_in["docker_image"]

    env: dict = CONFIG.env
    docker_config_json: pathlib.Path = group_in.pop("docker_config_json")

    config_engine: ConfigEngine = CONFIG.config_engine

    docker_config: DockerConfigModel = config_engine.openstudiolandscapes__docker_config

    docker_image: dict = group_in["docker_image"]

    docker_file = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{dist.name}",
        "__".join(context.asset_key.path),
        "Dockerfiles",
        "Dockerfile",
    )

    docker_file.parent.mkdir(parents=True, exist_ok=True)

    #################################################

    (
        image_name,
        image_prefixes,
        tags,
        build_base_parent_image_prefix,
        build_base_parent_image_name,
        build_base_parent_image_tags,
    ) = get_image_metadata(
        context=context,
        docker_image=docker_image,
        docker_config=docker_config,
        env=env,
    )

    #################################################

    apt_install_str_base: str = get_apt_install_str(
        apt_install_packages=apt_packages["base"],
    )

    # We override the default `python_str` because
    # the Python interpreter for the Kitsu Docker image is nothing
    # we are in charge of
    pip_install_str: str = get_pip_install_str(
        pip_install_packages=pip_packages, python_str="/opt/zou/env/bin/python"
    )

    script_init_db_dir = docker_file.parent / "scripts"
    script_init_db_dir.mkdir(parents=True, exist_ok=True)

    for script in [
        script_init_db,
        inject_postgres_conf,
    ]:

        shutil.copy(
            src=script,
            dst=script_init_db_dir,
        )

    # @formatter:off
    docker_file_str = textwrap.dedent(
        """\
        # {auto_generated}
        # {dagster_url}
        # https://hub.docker.com/r/cgwire/cgwire
        FROM {parent_image} AS {image_name}
        LABEL authors="{AUTHOR}"

        SHELL ["/bin/bash", "-c"]

        ARG DEBIAN_FRONTEND=noninteractive

        ENV CONTAINER_TIMEZONE={TIMEZONE}
        ENV SET_CONTAINER_TIMEZONE=true

        ENV LC_ALL=C.UTF-8
        ENV LANG=C.UTF-8

        RUN apt-get update && apt-get upgrade -y

        {apt_install_str_base}

        {pip_install_str}

        RUN apt-get clean

        WORKDIR /etc/postgresql/14/main

        COPY ./scripts/postgresql.conf .
        RUN chmod 0755 postgresql.conf

        WORKDIR /opt/zou

        COPY ./scripts/init_db.sh .
        RUN chmod 0755 init_db.sh

        ENTRYPOINT []
        """
    ).format(
        apt_install_str_base=apt_install_str_base,
        pip_install_str=pip_install_str.format(
            **env,
        ),
        auto_generated=f"AUTO-GENERATED by Dagster Asset {'__'.join(context.asset_key.path)}",
        dagster_url=urllib.parse.quote(
            f"http://localhost:3000/asset-groups/{'%2F'.join(context.asset_key.path)}",
            safe=":/%",
        ),
        image_name=image_name,
        # # Todo: this won't work as expected if len(tags) > 1
        # parent_image=f"{build_base_parent_image_prefix}{build_base_parent_image_name}:{build_base_parent_image_tags[0]}",
        parent_image="cgwire/cgwire:latest",
        **env,
    )
    # @formatter:on

    # Todo
    #  - [ ] WARN: StageNameCasing: Stage name 'Kitsu__build' should be lowercase (line 5)

    with open(docker_file, "w") as fw:
        fw.write(docker_file_str)

    with open(docker_file, "r") as fr:
        docker_file_content = fr.read()

    #################################################

    image_data, logs = create_image(
        context=context,
        image_name=image_name,
        image_prefixes=image_prefixes,
        tags=tags,
        docker_image=docker_image,
        docker_config=docker_config,
        docker_config_json=docker_config_json,
        docker_file=docker_file,
    )

    yield Output(image_data)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(image_data),
            "docker_file": MetadataValue.md(f"```shell\n{docker_file_content}\n```"),
            "env": MetadataValue.json(env),
            "logs": MetadataValue.json(logs),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
    description="",
)
def inject_postgres_conf(
    context: AssetExecutionContext,
    CONFIG: discovery.FeatureBaseModel,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:
    """ """

    postgres_conf = CONFIG.kitsu_postgres_conf_expanded

    with open(
        file=postgres_conf,
        mode="r",
    ) as fr:
        postgres_conf_content = fr.read()

    yield Output(postgres_conf)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(postgres_conf),
            "postgres_conf": MetadataValue.md(
                f"```shell\n{postgres_conf_content}\n```"
            ),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
    description="",
)
def script_init_db(
    context: AssetExecutionContext,
    CONFIG: discovery.FeatureBaseModel,
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:
    """ """

    env: dict = CONFIG.env

    init_db = {}

    init_db["exe"] = shutil.which("bash")
    init_db["script"] = str()

    # https://github.com/michimussato/kitsu-setup/blob/main/README_KITSU.md
    init_db["script"] += "#!/bin/bash\n"
    init_db["script"] += "# Documentation:\n"
    init_db["script"] += "# https://zou.cg-wire.com/\n"
    init_db["script"] += "\n"
    init_db["script"] += "if [[ ! -z \"$( ls -A '/var/lib/postgresql')\" ]]; then\n"
    init_db["script"] += "    echo /var/lib/postgresql is not empty.\n"
    init_db["script"] += "    echo Using existing DB.\n"
    init_db["script"] += "    echo Quit.\n"
    init_db["script"] += "    exit 0;\n"
    init_db["script"] += "fi\n"
    init_db["script"] += "\n"
    init_db["script"] += "echo /var/lib/postgresql empty.\n"
    init_db["script"] += "echo Initializing DB...\n"
    init_db["script"] += "\n"
    init_db["script"] += "mkdir -p /var/lib/postgresql/14/main\n"
    init_db["script"] += "chown -R postgres:postgres /var/lib/postgresql/14\n"
    init_db["script"] += "\n"
    init_db["script"] += "# Default encoding without specifying it is SQL_ASCII\n"
    init_db["script"] += "# psql zoudb -c 'SHOW SERVER_ENCODING'\n"
    init_db[
        "script"
    ] += "su - postgres -c '/usr/lib/postgresql/14/bin/initdb --pgdata=/var/lib/postgresql/14/main --auth=trust --encoding=UTF8'\n"
    init_db["script"] += "\n"
    init_db["script"] += "service postgresql start\n"
    init_db["script"] += "service redis-server start\n"
    init_db["script"] += "\n"
    init_db["script"] += "sudo -u postgres psql -U postgres -c 'create user root;'\n"
    init_db[
        "script"
    ] += "sudo -u postgres psql -U postgres -c 'create database zoudb;'\n"
    init_db[
        "script"
    ] += "sudo -u postgres psql -U postgres -d postgres -c \"alter user postgres with password '${DB_PASSWORD}';\"\n"
    init_db["script"] += "\n"
    init_db["script"] += "source /opt/zou/env/bin/activate\n"
    init_db["script"] += "\n"
    init_db["script"] += "zou init-db\n"
    init_db["script"] += "zou init-data\n"
    init_db["script"] += "\n"
    init_db["script"] += "mkdir -p ${TMP_DIR}\n"
    init_db["script"] += "chown -R postgres:postgres ${TMP_DIR}\n"
    init_db["script"] += "\n"
    init_db["script"] += "zou create-admin --password ${DB_PASSWORD} ${KITSU_ADMIN}\n"
    init_db["script"] += "\n"
    init_db["script"] += "service postgresql stop\n"
    init_db["script"] += "service redis-server stop\n"
    init_db["script"] += "\n"
    init_db["script"] += "# service redis-server is down but process seems to persist\n"
    init_db["script"] += "# for some reason\n"
    init_db["script"] += "pkill redis\n"
    init_db["script"] += "\n"
    init_db["script"] += "exit 0\n"

    init_db_script = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{dist.name}",
        "__".join(context.asset_key.path),
        "init_db.sh",
    )

    init_db_script.parent.mkdir(parents=True, exist_ok=True)

    with open(
        file=init_db_script,
        mode="w",
    ) as sh_init_zou:
        sh_init_zou.write(init_db["script"])

    yield Output(init_db_script)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(init_db_script),
            "dict_init_db": MetadataValue.json(init_db),
            "script_init_db": MetadataValue.md(f"```shell\n{init_db['script']}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
    description="",
)
def supervisord_conf(
    context: AssetExecutionContext,
    CONFIG: discovery.FeatureBaseModel,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:
    """
    We create a custom `/etc/supervisord.conf` file that launches `rq worker` if
    `KITSU_ENABLE_JOB_QUEUE` is set to `True`.

    Information about the default file:
    ```shell
    root@kitsu:/opt/zou# stat /etc/supervisord.conf
      File: /etc/supervisord.conf
      Size: 1933            Blocks: 8          IO Block: 4096   regular file
    Device: 53h/83d Inode: 21506964    Links: 1
    Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
    Access: 2023-10-04 06:30:12.000000000 +0000
    Modify: 2023-10-04 06:30:12.000000000 +0000
    Change: 2025-05-21 19:10:33.080676825 +0000
     Birth: 2025-05-21 19:10:33.080676825 +0000
    ```
    """

    supervisord_conf_str = textwrap.dedent(
        """\
        [supervisord]
        nodaemon = True
        umask = 022

        [program:sendria]
        command=/usr/local/bin/sendria --smtp-ip 0.0.0.0 --smtp-port 25 --http-ip 0.0.0.0 --foreground --no-quit --no-clear --db /var/lib/sendria.sqlite
        user=root
        autostart=true
        autorestart=true
        stdout_logfile=/var/log/redis/sendria.log
        redirect_stderr=true
        priority=100

        [program:redis]
        # let supervisord handle logs, don't daemonize
        command=/usr/bin/redis-server /etc/redis/redis.conf --logfile '' --daemonize no
        user=root
        autostart=true
        autorestart=true
        stdout_logfile=/var/log/redis/redis-server.log
        redirect_stderr=true
        priority=100

        [program:postgresql]
        command=/usr/lib/postgresql/%(ENV_PG_VERSION)s/bin/postmaster --config-file=/etc/postgresql/%(ENV_PG_VERSION)s/main/postgresql.conf
        user=postgres
        autostart=true
        autorestart=true
        # forcefully disconnect all clients
        stopsignal=SIGINT
        stdout_logfile=/var/log/supervisor/postgresql.log
        redirect_stderr=true
        priority=100

        [program:nginx]
        command = nginx -g "daemon off;"
        autostart = true
        autorestart = true
        stopwaitsecs = 5
        stdout_logfile=/var/log/supervisor/nginx.log
        redirect_stderr=true

        [program:gunicorn]
        environment=PREVIEW_FOLDER=/opt/zou/previews,DB_USERNAME=root,DB_PASSWORD=''
        command=/opt/zou/env/bin/gunicorn -c /etc/zou/gunicorn.py -b 127.0.0.1:5000 --chdir /opt/zou/zou zou.app:app
        directory=/opt/zou
        autostart=true
        autorestart=true
        stdout_logfile=NONE
        stderr_logfile=NONE

        [program:gunicorn-events]
        command=/opt/zou/env/bin/gunicorn -c /etc/zou/gunicorn-events.py -b 127.0.0.1:5001 zou.event_stream:app
        directory=/opt/zou
        autostart=true
        autorestart=true
        stdout_logfile=NONE
        stderr_logfile=NONE
        """
    )

    if CONFIG.kitsu_enable_job_queue:
        supervisord_conf_str += textwrap.dedent(
            """
            [program:kitsu-job-queue]
            command=/opt/zou/env/bin/rq worker -c zou.job_settings
            directory=/opt/zou
            # user=zou
            # group=www-data
            autostart=true
            autorestart=true
            stdout_logfile=/var/log/kitsu-job-queue.log
            redirect_stderr=true

            [group:zou-processes]
            programs=gunicorn,gunicorn-events,kitsu-job-queue
            priority=5
            """
        )

    else:
        supervisord_conf_str += textwrap.dedent(
            """
            [group:zou-processes]
            programs=gunicorn,gunicorn-events
            priority=5
            """
        )

    supervisord_conf_str += textwrap.dedent(
        """
        [unix_http_server]
        file=/tmp/supervisor.sock

        [supervisorctl]
        serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket

        [rpcinterface:supervisor]
        supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface
        """
    )

    supervisord_conf_script = pathlib.Path(
        CONFIG.env["DOT_LANDSCAPES"],
        CONFIG.env.get("LANDSCAPE", "default"),
        CONFIG.feature_name,
        "__".join(context.asset_key.path),
        "supervisord.conf",
    )

    supervisord_conf_script.parent.mkdir(parents=True, exist_ok=True)

    with open(
        file=supervisord_conf_script,
        mode="w",
    ) as fo:
        fo.write(supervisord_conf_str)

    yield Output(supervisord_conf_script)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(
                supervisord_conf_script
            ),
            "supervisord_conf_str": MetadataValue.md(
                f"```shell\n{supervisord_conf_str}\n```"
            ),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "build": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "build_docker_image"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_networks"]),
        ),
        "supervisord_conf": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "supervisord_conf"]),
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
)
def compose_kitsu(
    context: AssetExecutionContext,
    build: dict,  # pylint: disable=redefined-outer-name
    compose_networks: dict,  # pylint: disable=redefined-outer-name
    supervisord_conf: pathlib.Path,  # pylint: disable=redefined-outer-name
    CONFIG: discovery.FeatureBaseModel,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    env: dict = CONFIG.env

    config_engine: ConfigEngine = CONFIG.config_engine

    network_dict = {}
    ports_dict = {}

    if "networks" in compose_networks:
        network_dict = {"networks": list(compose_networks.get("networks", {}).keys())}
        ports_dict = {
            "ports": [
                f"{CONFIG.kitsu_port_host}:{CONFIG.kitsu_port_container}",
            ]
        }
    elif "network_mode" in compose_networks:
        network_dict = {"network_mode": compose_networks["network_mode"]}

    volumes_dict = {
        "volumes": [
            f"{supervisord_conf.as_posix()}:/etc/supervisord.conf:ro",
        ]
    }

    if not CONFIG.kitsu_db_inside_container:

        kitsu_db_dir_host = (
            CONFIG.kitsu_database_install_destination_expanded / "postgresql"
        )
        kitsu_db_dir_host.mkdir(parents=True, exist_ok=True)
        context.log.info(f"Directory {kitsu_db_dir_host.as_posix()} created.")

        volumes_dict["volumes"].insert(
            0,
            f"{kitsu_db_dir_host.as_posix()}:/var/lib/postgresql:rw",
        )

        kitsu_previews_host = (
            CONFIG.kitsu_database_install_destination_expanded / "previews"
        )
        kitsu_previews_host.mkdir(parents=True, exist_ok=True)
        context.log.info(f"Directory {kitsu_previews_host.as_posix()} created.")

        volumes_dict["volumes"].insert(
            1,
            f"{kitsu_previews_host}:/opt/zou/previews:rw",
        )

    # For portability, convert absolute volume paths to relative paths

    _volume_relative = []

    for v in volumes_dict["volumes"]:

        host, container = v.split(":", maxsplit=1)

        # docker_compose = pathlib.Path(
        #     CONFIG
        #     .docker_compose
        #     .as_posix()
        #     .format(
        #         **{
        #             "FEATURE": dist.name,
        #             **env,
        #         }
        #     )
        # )
        #
        # context.log.error(f"{CONFIG.docker_compose}")
        # context.log.error(f"{docker_compose}")

        volume_dir_host_rel_path = get_relative_path_via_common_root(
            context=context,
            path_src=CONFIG.docker_compose_expanded,
            path_dst=pathlib.Path(host),
            path_common_root=pathlib.Path(env["DOT_LANDSCAPES"]),
        )

        _volume_relative.append(
            f"{volume_dir_host_rel_path.as_posix()}:{container}",
        )

    volumes_dict = {
        "volumes": [
            *_volume_relative,
        ]
    }

    service_name = "kitsu"
    container_name, host_name = get_docker_compose_names(
        context=context,
        service_name=service_name,
        landscape_id=env.get("LANDSCAPE", "default"),
        domain_lan=config_engine.openstudiolandscapes__domain_lan,
    )

    docker_dict = {
        "services": {
            service_name: {
                "container_name": container_name,
                "hostname": host_name,
                "domainname": config_engine.openstudiolandscapes__domain_lan,
                "restart": DockerComposePolicies.RESTART_POLICY.ALWAYS.value,
                "environment": {
                    # https://zou.cg-wire.com/
                    # "LC_ALL": "C.UTF-8",
                    # "LANG": "C.UTF-8",
                    "KITSU_ADMIN": CONFIG.kitsu_admin_user,
                    "DB_PASSWORD": CONFIG.kitsu_db_password,
                    "SECRET_KEY": CONFIG.kitsu_secret_key,
                    "PREVIEW_FOLDER": CONFIG.kitsu_preview_folder.as_posix(),
                    "TMP_DIR": CONFIG.kitsu_tmp_dir.as_posix(),
                    "ENABLE_JOB_QUEUE": CONFIG.kitsu_enable_job_queue,
                },
                # "image": "${DOT_OVERRIDES_REGISTRY_NAMESPACE:-docker.io/openstudiolandscapes}/%s:%s"
                # % (build["image_name"], build["image_tags"][0]),
                "image": "%s%s:%s"
                % (
                    build["image_prefixes"],
                    build["image_name"],
                    build["image_tags"][0],
                ),
                **copy.deepcopy(volumes_dict),
                **copy.deepcopy(network_dict),
                "depends_on": {
                    "kitsu-init-db": {
                        "condition": "service_completed_successfully",
                    },
                },
                # "healthcheck": {
                #     # Todo:
                #     #  - [ ] fix: test succeeds even if Postgres is down
                #     #  "test": ["CMD-SHELL", "psql -U ${DB_USER} -d ${DB_MAIN} -c 'SELECT 1' || exit 1"],
                #     "test": ["CMD", "curl", "-f", f"http://localhost:{env.get('KITSU_PORT_CONTAINER')}"],
                #     "interval": "10s",
                #     "timeout": "2s",
                #     "retries": "3",
                # },
                "command": [
                    "bash",
                    "/opt/zou/start_zou.sh",
                ],
                **copy.deepcopy(ports_dict),
            },
        },
    }

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "docker_dict": MetadataValue.md(
                f"```json\n{json.dumps(docker_dict, indent=2)}\n```"
            ),
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
            "env": MetadataValue.json(env),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "build": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "build_docker_image"]),
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
    deps=[
        AssetKey([*ASSET_HEADER["key_prefix"], "script_init_db"]),
    ],
    description="This executes the OpenStudioLandscapes Repository Installer. "
    "Needs to be done only once.",
)
def compose_init_db(
    context: AssetExecutionContext,
    build: dict,  # pylint: disable=redefined-outer-name
    CONFIG: discovery.FeatureBaseModel,  # pylint: disable=redefined-outer-name
) -> Generator[Output[MutableMapping] | AssetMaterialization, None, None]:
    """ """

    env: dict = CONFIG.env

    config_engine: ConfigEngine = CONFIG.config_engine

    # network_dict = {}
    # ports_dict = {}
    #
    # if "networks" in compose_networks:
    #     network_dict = {
    #         "networks": list(compose_networks.get("networks", {}).keys())
    #     }
    #     ports_dict = {
    #         "ports": [
    #         ]
    #     }
    # elif "network_mode" in compose_networks:
    #     network_dict = {
    #         "network_mode": compose_networks.get("network_mode")
    #     }
    #     ports_dict = {}
    # else:
    #     network_dict = {}
    #     ports_dict = {}

    kitsu_db_dir_host = (
        CONFIG.kitsu_database_install_destination_expanded / "postgresql"
    )
    kitsu_db_dir_host.mkdir(parents=True, exist_ok=True)

    # Is:
    # - /home/michael/git/repos/OpenStudioLandscapes/.landscapes/2025-07-12-15-44-28-d7511d9a293d496daed627176a026b43/Kitsu__Kitsu/data/kitsu/postgresql:/var/lib/postgresql
    #
    # Want:
    # - ../../../../2025-07-10-22-36-50-47cd6c0a7dd141429707ab6d91190a27/Kitsu__Kitsu/data/kitsu/postgresql:/var/lib/postgresql
    #
    # Get:
    # - ../../../../2025-07-12-15-44-28-d7511d9a293d496daed627176a026b43/Kitsu__Kitsu/data/kitsu/postgresql:/var/lib/postgresql

    # For portability, convert absolute volume paths to relative paths
    volumes_paths_to_convert = [f"{kitsu_db_dir_host.as_posix()}:/var/lib/postgresql"]

    _volume_relative = []

    for v in volumes_paths_to_convert:

        host, container = v.split(":", maxsplit=1)

        volume_dir_host_rel_path = get_relative_path_via_common_root(
            context=context,
            path_src=CONFIG.docker_compose_expanded,
            path_dst=pathlib.Path(host),
            path_common_root=pathlib.Path(env["DOT_LANDSCAPES"]),
        )

        _volume_relative.append(
            f"{volume_dir_host_rel_path.as_posix()}:{container}",
        )

    volumes_dict = {
        "volumes": [
            *_volume_relative,
        ]
    }

    service_name = "kitsu-init-db"
    container_name, host_name = get_docker_compose_names(
        context=context,
        service_name=service_name,
        landscape_id=env.get("LANDSCAPE", "default"),
        domain_lan=config_engine.openstudiolandscapes__domain_lan,
    )

    docker_dict = {
        "services": {
            service_name: {
                "container_name": container_name,
                "hostname": host_name,
                "domainname": config_engine.openstudiolandscapes__domain_lan,
                "environment": {
                    # https://zou.cg-wire.com/
                    # "LC_ALL": "C.UTF-8",
                    # "LANG": "C.UTF-8",
                    "KITSU_ADMIN": CONFIG.kitsu_admin_user,
                    "DB_PASSWORD": CONFIG.kitsu_db_password,
                    "SECRET_KEY": CONFIG.kitsu_secret_key,
                    "PREVIEW_FOLDER": CONFIG.kitsu_preview_folder.as_posix(),
                    "TMP_DIR": CONFIG.kitsu_tmp_dir.as_posix(),
                },
                "restart": DockerComposePolicies.RESTART_POLICY.NO.value,
                # "image": "${DOT_OVERRIDES_REGISTRY_NAMESPACE:-docker.io/openstudiolandscapes}/%s:%s"
                # % (build["image_name"], build["image_tags"][0]),
                "image": "%s%s:%s"
                % (
                    build["image_prefixes"],
                    build["image_name"],
                    build["image_tags"][0],
                ),
                "command": [
                    "/usr/bin/bash",
                    "/opt/zou/init_db.sh",
                ],
                **copy.deepcopy(volumes_dict),
            },
        },
    }

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "docker_dict": MetadataValue.md(
                f"```json\n{json.dumps(docker_dict, indent=2)}\n```"
            ),
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
            "env": MetadataValue.json(env),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "compose_kitsu": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_kitsu"]),
        ),
        "compose_init_db": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_init_db"]),
        ),
    },
)
def compose_maps(
    context: AssetExecutionContext,
    **kwargs,  # pylint: disable=redefined-outer-name
) -> Generator[Output[List[MutableMapping]] | AssetMaterialization, None, None]:

    ret = list(kwargs.values())

    context.log.info(ret)

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )


# @asset(
#     **ASSET_HEADER,
#     ins={
#         "features_in": AssetIn(AssetKey([*ASSET_HEADER["key_prefix"], "group_in"])),
#     },
# )
# def docker_image(
#     context: AssetExecutionContext,
#     features_in: dict,
# ) -> Generator[Output[dict] | AssetMaterialization, None, None]:
#
#     context.log.info(features_in)
#
#     _docker_image: dict = features_in.pop("docker_image")
#     context.log.info(_docker_image)
#
#     yield Output(_docker_image)
#
#     yield AssetMaterialization(
#         asset_key=context.asset_key,
#         metadata={
#             "docker_image": MetadataValue.json(_docker_image),
#         },
#     )


@asset(
    **ASSET_HEADER,
    ins={},
)
def cmd_extend(
    context: AssetExecutionContext,
) -> Generator[Output[list[Any]] | AssetMaterialization | Any, Any, None]:

    ret = []

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={},
)
def cmd_append(
    context: AssetExecutionContext,
) -> Generator[Output[dict[str, list[Any]]] | AssetMaterialization | Any, Any, None]:

    ret = {"cmd": [], "exclude_from_quote": []}

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )
