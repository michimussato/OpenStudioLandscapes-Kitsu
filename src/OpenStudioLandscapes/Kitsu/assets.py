import copy
import json
import pathlib
import shutil
import textwrap
import time
import urllib.parse
from typing import Generator, MutableMapping, List

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

from OpenStudioLandscapes.engine.constants import *
from OpenStudioLandscapes.engine.enums import *
from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.utils.docker import *

from OpenStudioLandscapes.Kitsu.constants import *

from OpenStudioLandscapes.engine.common_assets.constants import get_constants
from OpenStudioLandscapes.engine.common_assets.docker_config import get_docker_config
from OpenStudioLandscapes.engine.common_assets.env import get_env
from OpenStudioLandscapes.engine.common_assets.group_in import get_group_in
from OpenStudioLandscapes.engine.common_assets.group_out import get_group_out
from OpenStudioLandscapes.engine.common_assets.docker_compose_graph import (
    get_docker_compose_graph,
)
from OpenStudioLandscapes.engine.common_assets.feature_out import get_feature_out
from OpenStudioLandscapes.engine.common_assets.compose import get_compose
from OpenStudioLandscapes.engine.common_assets.docker_config_json import (
    get_docker_config_json,
)


constants = get_constants(
    ASSET_HEADER=ASSET_HEADER,
)


docker_config = get_docker_config(
    ASSET_HEADER=ASSET_HEADER,
)


group_in = get_group_in(
    ASSET_HEADER=ASSET_HEADER,
    ASSET_HEADER_PARENT=ASSET_HEADER_BASE,
    input_name=str(GroupIn.BASE_IN),
)


env = get_env(
    ASSET_HEADER=ASSET_HEADER,
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
        "env": dict,
        "compose": dict,
        "group_in": dict,
    },
)


docker_config_json = get_docker_config_json(
    ASSET_HEADER=ASSET_HEADER,
)


@asset(
    **ASSET_HEADER,
)
def compose_networks(
    context: AssetExecutionContext,
) -> Generator[
    Output[MutableMapping[str, MutableMapping[str, MutableMapping[str, str]]]]
    | AssetMaterialization,
    None,
    None,
]:

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
) -> Generator[
    Output[MutableMapping[str, List[str]]] | AssetMaterialization, None, None
]:
    """ """

    _apt_packages = {}

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
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
        ),
        "docker_config_json": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "docker_config_json"]),
        ),
        "docker_image": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "docker_image"])
        ),
        "docker_config": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "docker_config"])
        ),
        "apt_packages": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "apt_packages"]),
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
    env: dict,  # pylint: disable=redefined-outer-name
    docker_config_json: pathlib.Path,  # pylint: disable=redefined-outer-name
    docker_image: dict,  # pylint: disable=redefined-outer-name
    docker_config: DockerConfig,  # pylint: disable=redefined-outer-name
    apt_packages: dict[str, list[str]],  # pylint: disable=redefined-outer-name
    script_init_db: pathlib.Path,  # pylint: disable=redefined-outer-name
    inject_postgres_conf: pathlib.Path,  # pylint: disable=redefined-outer-name
) -> Generator[Output[MutableMapping] | AssetMaterialization, None, None]:
    """ """

    build_base_image_data: dict = docker_image
    build_base_docker_config: DockerConfig = docker_config

    if build_base_docker_config.value["docker_push"]:
        build_base_parent_image_prefix: str = build_base_image_data["image_prefix_full"]
    else:
        build_base_parent_image_prefix: str = build_base_image_data[
            "image_prefix_local"
        ]

    build_base_parent_image_name: str = build_base_image_data["image_name"]
    build_base_parent_image_tags: list = build_base_image_data["image_tags"]

    docker_file = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{ASSET_HEADER['group_name']}__{'__'.join(ASSET_HEADER['key_prefix'])}",
        "__".join(context.asset_key.path),
        "Dockerfiles",
        "Dockerfile",
    )

    docker_file.parent.mkdir(parents=True, exist_ok=True)

    image_name = get_image_name(context=context)
    image_prefix_local = parse_docker_image_path(
        docker_config=build_base_docker_config,
        prepend_registry=False,
    )
    image_prefix_full = parse_docker_image_path(
        docker_config=build_base_docker_config,
        prepend_registry=True,
    )

    tags = [
        env.get("LANDSCAPE", str(time.time())),
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

    image_data = {
        "image_name": image_name,
        "image_prefix_local": image_prefix_local,
        "image_prefix_full": image_prefix_full,
        "image_tags": tags,
        "image_parent": copy.deepcopy(build_base_image_data),
    }

    context.log.info(f"{image_data = }")

    cmds = []

    tags_local = [f"{image_prefix_local}{image_name}:{tag}" for tag in tags]
    tags_full = [f"{image_prefix_full}{image_name}:{tag}" for tag in tags]

    cmd_build = docker_build_cmd(
        context=context,
        docker_config_json=docker_config_json,
        docker_file=docker_file,
        tags_local=tags_local,
        tags_full=tags_full,
    )

    cmds.append(cmd_build)

    cmds_push = docker_push_cmd(
        context=context,
        docker_config_json=docker_config_json,
        tags_full=tags_full,
    )

    cmds.extend(cmds_push)

    context.log.info(f"{cmds = }")

    logs = []

    for logs_ in docker_process_cmds(
        context=context,
        cmds=cmds,
    ):
        logs.append(logs_)

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
        "env": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
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
            "postgres_conf": MetadataValue.md(
                f"```shell\n{postgres_conf_content}\n```"
            ),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
        ),
    },
    description="",
)
def script_init_db(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:
    """ """

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
    init_db[
        "script"
    ] += "zou create-admin --password ${KITSU_ADMIN_PASSWORD} ${KITSU_ADMIN_USER}\n"
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
        f"{ASSET_HEADER['group_name']}__{'__'.join(ASSET_HEADER['key_prefix'])}",
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
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
        ),
        "build": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "build_docker_image"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_networks"]),
        ),
    },
)
def compose_kitsu(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    build: dict,  # pylint: disable=redefined-outer-name
    compose_networks: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    network_dict = {}
    ports_dict = {}

    if "networks" in compose_networks:
        network_dict = {"networks": list(compose_networks.get("networks", {}).keys())}
        ports_dict = {
            "ports": [
                f"{env.get('KITSU_PORT_HOST')}:{env.get('KITSU_PORT_CONTAINER')}",
            ]
        }
    elif "network_mode" in compose_networks:
        network_dict = {"network_mode": compose_networks.get("network_mode")}

    volumes_dict = {
        "volumes": [
            f"{env.get('NFS_ENTRY_POINT')}:{env.get('NFS_ENTRY_POINT')}",
            f"{env.get('NFS_ENTRY_POINT')}:{env.get('NFS_ENTRY_POINT_LNS')}",
        ]
    }

    if not KITSUDB_INSIDE_CONTAINER:

        kitsu_db_dir_host = (
            pathlib.Path(env.get("KITSU_DATABASE_INSTALL_DESTINATION")) / "postgresql"
        )
        kitsu_db_dir_host.mkdir(parents=True, exist_ok=True)
        context.log.info(f"Directory {kitsu_db_dir_host.as_posix()} created.")

        volumes_dict["volumes"].insert(
            0,
            f"{kitsu_db_dir_host.as_posix()}:/var/lib/postgresql",
        )

        kitsu_previews_host = (
            pathlib.Path(env.get("KITSU_DATABASE_INSTALL_DESTINATION")) / "previews"
        )
        kitsu_previews_host.mkdir(parents=True, exist_ok=True)
        context.log.info(f"Directory {kitsu_previews_host.as_posix()} created.")

        volumes_dict["volumes"].insert(
            1,
            f"{kitsu_previews_host}:/opt/zou/previews",
        )

    service_name = "kitsu"
    container_name = "--".join([service_name, env.get("LANDSCAPE", "default")])
    host_name = ".".join([env["KITSU_HOSTNAME"], env["ROOT_DOMAIN"]])

    docker_dict = {
        "services": {
            service_name: {
                "container_name": container_name,
                "hostname": host_name,
                "domainname": env["ROOT_DOMAIN"],
                "restart": "always",
                "environment": {
                    # https://zou.cg-wire.com/
                    # "LC_ALL": "C.UTF-8",
                    # "LANG": "C.UTF-8",
                    "KITSU_ADMIN": env["KITSU_ADMIN_USER"],
                    "DB_PASSWORD": env["KITSU_DB_PASSWORD"],
                    "SECRET_KEY": env["KITSU_SECRET_KEY"],
                    "PREVIEW_FOLDER": env["KITSU_PREVIEW_FOLDER"],
                    "TMP_DIR": env["KITSU_TMP_DIR"],
                    "ENABLE_JOB_QUEUE": env["KITSU_ENABLE_JOB_QUEUE"],
                },
                "image": f"{build['image_prefix_full']}{build['image_name']}:{build['image_tags'][0]}",
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
        "env": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
        ),
        "build": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "build_docker_image"]),
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
    env: dict,  # pylint: disable=redefined-outer-name
    build: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[MutableMapping] | AssetMaterialization, None, None]:
    """ """

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
        pathlib.Path(env.get("KITSU_DATABASE_INSTALL_DESTINATION")) / "postgresql"
    )
    kitsu_db_dir_host.mkdir(parents=True, exist_ok=True)

    volumes_dict = {
        "volumes": [
            f"{kitsu_db_dir_host.as_posix()}:/var/lib/postgresql",
            f"{env.get('NFS_ENTRY_POINT')}:{env.get('NFS_ENTRY_POINT')}",
            f"{env.get('NFS_ENTRY_POINT')}:{env.get('NFS_ENTRY_POINT_LNS')}",
        ]
    }

    service_name = "kitsu-init-db"
    container_name = "--".join([service_name, env.get("LANDSCAPE", "default")])
    host_name = ".".join([service_name, env["ROOT_DOMAIN"]])

    docker_dict = {
        "services": {
            service_name: {
                "container_name": container_name,
                "hostname": host_name,
                "domainname": env["ROOT_DOMAIN"],
                "environment": {
                    # https://zou.cg-wire.com/
                    # "LC_ALL": "C.UTF-8",
                    # "LANG": "C.UTF-8",
                    "KITSU_ADMIN": env["KITSU_ADMIN_USER"],
                    "DB_PASSWORD": env["KITSU_DB_PASSWORD"],
                    "SECRET_KEY": env["KITSU_SECRET_KEY"],
                    "PREVIEW_FOLDER": env["KITSU_PREVIEW_FOLDER"],
                    "TMP_DIR": env["KITSU_TMP_DIR"],
                },
                "restart": "no",
                "image": f"{build['image_prefix_full']}{build['image_name']}:{build['image_tags'][0]}",
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


@asset(
    **ASSET_HEADER,
    ins={
        "features_in": AssetIn(AssetKey([*ASSET_HEADER["key_prefix"], "group_in"])),
    },
)
def docker_image(
    context: AssetExecutionContext,
    features_in: dict,
) -> Generator[Output[dict] | AssetMaterialization, None, None]:

    context.log.info(features_in)

    _docker_image: dict = features_in.pop("docker_image")
    context.log.info(_docker_image)

    yield Output(_docker_image)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "docker_image": MetadataValue.json(_docker_image),
        },
    )
