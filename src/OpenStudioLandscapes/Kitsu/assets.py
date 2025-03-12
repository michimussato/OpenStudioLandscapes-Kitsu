import copy
import json
import pathlib
import shutil
import textwrap
import time
import urllib.parse
from collections import ChainMap
from functools import reduce
from typing import Generator, MutableMapping

import yaml
from docker_compose_graph.utils import *
from python_on_whales import docker

from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetKey,
    AssetMaterialization,
    MaterializeResult,
    MetadataValue,
    Output,
    asset,
    AssetsDefinition,
)

from OpenStudioLandscapes.engine.base.assets import KEY_BASE
from OpenStudioLandscapes.engine.constants import *

from OpenStudioLandscapes.engine.enums import *
from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.base.ops import op_docker_compose_graph
from OpenStudioLandscapes.engine.base.ops import op_group_out

from OpenStudioLandscapes.Kitsu.constants import *


@asset(
    **ASSET_HEADER,
    ins={
        "group_in": AssetIn(
            AssetKey([*KEY_BASE, "group_out"])
        ),
    },
    deps=[
        AssetKey([*ASSET_HEADER['key_prefix'], f"constants_{ASSET_HEADER['group_name']}"])
    ],
)
def env(
    context: AssetExecutionContext,
    group_in: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:

    env_in = copy.deepcopy(group_in["env"])

    # expanding variables in OpenStudioLandscapes.Kitsu.constants.ENVIRONMENT
    for k, v in ENVIRONMENT.items():
        if isinstance(v, str):
            ENVIRONMENT[k] = v.format(**env_in)

    env_in.update(ENVIRONMENT)

    env_in.update(
        {
            "COMPOSE_SCOPE": COMPOSE_SCOPE,
        },
    )

    yield Output(env_in)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(env_in),
            "ENVIRONMENT": MetadataValue.json(ENVIRONMENT),
        },
    )


@asset(
    **ASSET_HEADER,
)
def compose_networks(
    context: AssetExecutionContext,
) -> Generator[
    Output[dict[str, dict[str, dict[str, str]]]] | AssetMaterialization, None, None]:

    compose_network_mode = ComposeNetworkMode.DEFAULT

    if compose_network_mode == ComposeNetworkMode.DEFAULT:
        docker_dict = {
            "networks": {
                # "mongodb": {
                #     "name": "network_mongodb-10-2",
                # },
                "kitsu": {
                    "name": "network_kitsu",
                },
                # "ayon": {
                #     "name": "network_ayon-10-2",
                # },
            },
        }

    else:
        docker_dict = {
            "network_mode": compose_network_mode.value,
        }

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "compose_network_mode": MetadataValue.text(compose_network_mode.value),
            "docker_dict": MetadataValue.md(
                f"```json\n{json.dumps(docker_dict, indent=2)}\n```"
            ),
            "docker_yaml": MetadataValue.md(f"```shell\n{docker_yaml}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
)
def apt_packages(
    context: AssetExecutionContext,
) -> Generator[Output[dict[str, list[str]]] | AssetMaterialization, None, None]:
    """ """

    _apt_packages = dict()

    _apt_packages["base"] = [
        "sudo",
        "htop",
        "curl",
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
        "env": AssetIn(
            AssetKey([*KEY, "env"]),
        ),
        "apt_packages": AssetIn(
            AssetKey([*KEY, "apt_packages"]),
        ),
        "script_init_db": AssetIn(
            AssetKey([*KEY, "script_init_db"]),
        ),
        "inject_postgres_conf": AssetIn(
            AssetKey([*KEY, "inject_postgres_conf"]),
        ),
    },
)
def build_docker_image(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    apt_packages: dict[str, list[str]],  # pylint: disable=redefined-outer-name
    script_init_db: pathlib.Path,  # pylint: disable=redefined-outer-name
    inject_postgres_conf: pathlib.Path,  # pylint: disable=redefined-outer-name
) -> Generator[Output[str] | AssetMaterialization, None, None]:
    """ """

    docker_file = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{GROUP}__{'__'.join(KEY)}",
        "__".join(context.asset_key.path),
        "Dockerfiles",
        "Dockerfile",
    )

    shutil.rmtree(docker_file.parent, ignore_errors=True)
    docker_file.parent.mkdir(parents=True, exist_ok=True)

    tags = [
        f"{env.get('IMAGE_PREFIX')}/{'__'.join(context.asset_key.path).lower()}:latest",
        f"{env.get('IMAGE_PREFIX')}/{'__'.join(context.asset_key.path).lower()}:{env.get('LANDSCAPE', str(time.time()))}",
    ]

    apt_install_str_base: str = get_apt_install_str(
        apt_install_packages=apt_packages["base"],
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
        """
        # {auto_generated}
        # {dagster_url}
        # https://hub.docker.com/r/cgwire/cgwire
        FROM cgwire/cgwire:latest AS {image_name}
        LABEL authors="{AUTHOR}"

        SHELL ["/bin/bash", "-c"]

        ARG DEBIAN_FRONTEND=noninteractive

        ENV CONTAINER_TIMEZONE={TIMEZONE}
        ENV SET_CONTAINER_TIMEZONE=true
        
        ENV LC_ALL=C.UTF-8
        ENV LANG=C.UTF-8
        
        RUN apt-get update && apt-get upgrade -y

        {apt_install_str_base}

        RUN apt-get clean
        
        WORKDIR /etc/postgresql/14/main
        
        COPY --chmod=0644 ./scripts/postgresql.conf .
        
        WORKDIR /opt/zou

        COPY --chmod=0755 ./scripts/init_db.sh .

        ENTRYPOINT []
    """
    ).format(
        apt_install_str_base=apt_install_str_base,
        auto_generated=f"AUTO-GENERATED by Dagster Asset {'__'.join(context.asset_key.path)}",
        dagster_url=urllib.parse.quote(
            f"http://localhost:3000/asset-groups/{'%2F'.join(context.asset_key.path)}",
            safe=":/%",
        ),
        image_name="__".join(context.asset_key.path).lower(),
        **env,
    )
    # @formatter:on

    # Todo
    #  - [ ] WARN: StageNameCasing: Stage name 'Kitsu__build' should be lowercase (line 5)

    with open(docker_file, "w") as fw:
        fw.write(docker_file_str)

    with open(docker_file, "r") as fr:
        docker_file_content = fr.read()

    stream = docker.build(
        context_path=docker_file.parent.as_posix(),
        cache=DOCKER_USE_CACHE,
        tags=tags,
        stream_logs=True,
    )

    log: str = ""

    for msg in stream:
        context.log.debug(msg)
        log += msg

    cmds_docker = compile_cmds(
        docker_file=docker_file,
        tag=tags[1],
    )

    yield Output(tags[1])

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(tags[1]),
            "docker_file": MetadataValue.md(f"```shell\n{docker_file_content}\n```"),
            **cmds_docker,
            "build_logs": MetadataValue.md(f"```shell\n{log}\n```"),
            "env": MetadataValue.json(env),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*KEY, "env"]),
        ),
    },
    description="",
)
def inject_postgres_conf(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:
    """ """

    postgres_conf = pathlib.Path(
        env["KITSU_POSTGRES_CONF"],
    )

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
            "postgres_conf": MetadataValue.md(f"```shell\n{postgres_conf_content}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*KEY, "env"]),
        ),
    },
    description="",
)
def script_init_db(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:
    """ """

    init_db = dict()

    init_db["exe"] = shutil.which("bash")
    init_db["script"] = str()

    # https://github.com/michimussato/kitsu-setup/blob/main/README_KITSU.md
    init_db["script"] += "#!/bin/bash\n"
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
    init_db["script"] += "su - postgres -c '/usr/lib/postgresql/14/bin/initdb --pgdata=/var/lib/postgresql/14/main --auth=trust --encoding=UTF8'\n"
    init_db["script"] += "\n"
    init_db["script"] += "service postgresql start\n"
    init_db["script"] += "service redis-server start\n"
    init_db["script"] += "\n"
    init_db["script"] += "sudo -u postgres psql -U postgres -c 'create user root;'\n"
    init_db["script"] += "sudo -u postgres psql -U postgres -c 'create database zoudb;'\n"
    init_db["script"] += "sudo -u postgres psql -U postgres -d postgres -c \"alter user postgres with password '${DB_PASSWORD}';\"\n"
    init_db["script"] += "\n"
    init_db["script"] += "source /opt/zou/env/bin/activate\n"
    init_db["script"] += "\n"
    init_db["script"] += "zou init-db\n"
    init_db["script"] += "zou init-data\n"
    init_db["script"] += "\n"
    init_db["script"] += "mkdir -p ${TMP_DIR}\n"
    init_db["script"] += "chown -R postgres:postgres ${TMP_DIR}\n"
    init_db["script"] += "\n"
    init_db["script"] += "zou create-admin ${KITSU_ADMIN} --password ${DB_PASSWORD}\n"
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
        f"{GROUP}__{'__'.join(KEY)}",
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
        "env": AssetIn(
            AssetKey([*KEY, "env"]),
        ),
        "build": AssetIn(
            AssetKey([*KEY, "build_docker_image"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*KEY, "compose_networks"]),
        ),
    },
)
def compose_kitsu(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    build: str,  # pylint: disable=redefined-outer-name
    compose_networks: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    if "networks" in compose_networks:
        network_dict = {
            "networks": list(compose_networks.get("networks", {}).keys())
        }
        ports_dict = {
            "ports": [
                f"{env.get('KITSU_PORT_HOST')}:{env.get('KITSU_PORT_CONTAINER')}",
            ]
        }
    elif "network_mode" in compose_networks:
        network_dict = {
            "network_mode": compose_networks.get("network_mode")
        }
        ports_dict = {}
    else:
        network_dict = {}
        ports_dict = {}

    cmd_docker_run = [
        shutil.which("docker"),
        "run",
        "--rm",
        "--interactive",
        "--tty",
        build,
        "/bin/bash",
    ]

    volumes = [
        f"{env.get('NFS_ENTRY_POINT')}:{env.get('NFS_ENTRY_POINT')}",
        f"{env.get('NFS_ENTRY_POINT')}:{env.get('NFS_ENTRY_POINT_LNS')}",
    ]

    if not KITSUDB_INSIDE_CONTAINER:

        kitsu_db_dir_host = (
            pathlib.Path(env.get("KITSU_DATABASE_INSTALL_DESTINATION"))
            / "postgresql"
        )
        kitsu_db_dir_host.mkdir(parents=True, exist_ok=True)

        volumes.insert(
            0,
            f"{kitsu_db_dir_host.as_posix()}:/var/lib/postgresql",
        )

        kitsu_previews_host = (
            pathlib.Path(env.get("KITSU_DATABASE_INSTALL_DESTINATION")) / "previews"
        )
        kitsu_previews_host.mkdir(parents=True, exist_ok=True)

        volumes.insert(
            1,
            f"{kitsu_previews_host}:/opt/zou/previews",
        )

    docker_dict = {
        "services": {
            "kitsu": {
                "container_name": "kitsu",
                "hostname": "kitsu",
                "domainname": env.get("ROOT_DOMAIN"),
                "restart": "always",
                "environment": {
                    # https://zou.cg-wire.com/
                    # "LC_ALL": "C.UTF-8",
                    # "LANG": "C.UTF-8",
                    "KITSU_ADMIN": env.get("KITSU_ADMIN_USER", "admin@example.com"),
                    "DB_PASSWORD": env.get("KITSU_DB_PASSWORD", "mysecretpassword"),
                    "SECRET_KEY": env.get("SECRET_KEY", "yourrandomsecretkey"),
                    "PREVIEW_FOLDER": env.get("KITSU_PREVIEW_FOLDER", "/opt/zou/previews"),
                    "TMP_DIR": env.get("KITSU_TMP_DIR", "/opt/zou/tmp"),
                },
                "image": build,
                "volumes": volumes,
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
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
            "cmd_docker_run": MetadataValue.path(cmd_list_to_str(cmd_docker_run)),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "compose_kitsu": AssetIn(
            AssetKey([*KEY, "compose_kitsu"]),
        ),
        "compose_init_db": AssetIn(
            AssetKey([*KEY, "compose_init_db"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*KEY, "compose_networks"]),
        ),
    },
    # tags={
    #     "stage": "third_party/deadline/v10_2",
    #     "step": "docker/compose",
    # },
)
def compose(
    context: AssetExecutionContext,
    compose_kitsu: dict,  # pylint: disable=redefined-outer-name
    compose_init_db: dict,  # pylint: disable=redefined-outer-name
    compose_networks: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[MutableMapping] | AssetMaterialization, None, None]:
    """ """

    if "networks" in compose_networks:
        network_dict = copy.deepcopy(compose_networks)
    else:
        network_dict = {}

    docker_chainmap = ChainMap(
        network_dict,
        compose_kitsu,
        compose_init_db,
    )

    docker_dict = reduce(deep_merge, docker_chainmap.maps)

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
            # Todo: "cmd_docker_run": MetadataValue.path(cmd_list_to_str(cmd_docker_run)),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*KEY, "env"]),
        ),
        "build_docker_image": AssetIn(
            AssetKey([*KEY, "build_docker_image"]),
        ),
        # "compose_networks": AssetIn(
        #     AssetKey([*KEY, "compose_networks"]),
        # ),
    },
    deps=[
        AssetKey([*KEY, "script_init_db"]),
    ],
    description="This executes the OpenStudioLandscapes Repository Installer. "
    "Needs to be done only once.",
    # tags={
    #     "stage": "third_party/deadline/v10_2/repository",
    #     "step": "docker/compose",
    # },
)
def compose_init_db(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    build_docker_image: str,  # pylint: disable=redefined-outer-name
    # compose_networks: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[MutableMapping] | AssetMaterialization, None, None]:
    """ """

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
        pathlib.Path(env.get("KITSU_DATABASE_INSTALL_DESTINATION"))
        / "postgresql"
    )
    kitsu_db_dir_host.mkdir(parents=True, exist_ok=True)

    volumes = [
        f"{kitsu_db_dir_host.as_posix()}:/var/lib/postgresql",
        f"{env.get('NFS_ENTRY_POINT')}:{env.get('NFS_ENTRY_POINT')}",
        f"{env.get('NFS_ENTRY_POINT')}:{env.get('NFS_ENTRY_POINT_LNS')}",
    ]

    docker_dict = {
        "services": {
            "kitsu-init-db": {
                "container_name": "kitsu-init-db",
                "hostname": "kitsu-init-db",
                "domainname": env.get("ROOT_DOMAIN"),
                "environment": {
                    # https://zou.cg-wire.com/
                    # "LC_ALL": "C.UTF-8",
                    # "LANG": "C.UTF-8",
                    "KITSU_ADMIN": env.get("KITSU_ADMIN_USER", "admin@example.com"),
                    "DB_PASSWORD": env.get("KITSU_DB_PASSWORD", "mysecretpassword"),
                    "SECRET_KEY": env.get("SECRET_KEY", "yourrandomsecretkey"),
                    "PREVIEW_FOLDER": env.get("KITSU_PREVIEW_FOLDER", "/opt/zou/previews"),
                    "TMP_DIR": env.get("KITSU_TMP_DIR", "/opt/zou/tmp"),
                },
                "restart": "no",
                "image": build_docker_image,
                "command": [
                    "/usr/bin/bash",
                    "/opt/zou/init_db.sh",
                ],
                "volumes": volumes,
            },
        },
    }

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
        },
    )


group_out = AssetsDefinition.from_op(
    op_group_out,
    group_name=GROUP,
    tags_by_output_name={
        "group_out": {
            "group_out": "third_party",
        },
    },
    key_prefix=KEY,
    keys_by_input_name={
        "compose": AssetKey(
            [*KEY, "compose"]
        ),
        "env": AssetKey(
            [*KEY, "env"]
        ),
    },
)


docker_compose_graph = AssetsDefinition.from_op(
    op_docker_compose_graph,
    group_name=GROUP,
    key_prefix=KEY,
    keys_by_input_name={
        "group_out": AssetKey(
            [*KEY, "group_out"]
        ),
    },
)
