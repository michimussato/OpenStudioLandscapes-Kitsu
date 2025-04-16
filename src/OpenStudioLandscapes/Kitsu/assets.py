import copy
import json
import pathlib
import shutil
import textwrap
import time
import urllib.parse
from typing import Generator, MutableMapping

import yaml
from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetKey,
    AssetMaterialization,
    AssetsDefinition,
    MetadataValue,
    Output,
    asset,
)

# from OpenStudioLandscapes.engine.base.assets import KEY_BASE
from OpenStudioLandscapes.engine.base.ops import (
    op_compose,
    op_docker_compose_graph,
    op_group_out,
)
from OpenStudioLandscapes.engine.constants import *
from OpenStudioLandscapes.engine.enums import *
from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.utils.docker.whales import *

from OpenStudioLandscapes.Kitsu.constants import *


@asset(
    **ASSET_HEADER,
    ins={
        "group_in": AssetIn(AssetKey([*KEY_BASE, "group_out"])),
        "constants": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "FEATURE_CONFIGS"])
        ),
        "FEATURE_CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "FEATURE_CONFIG"])
        ),
        "COMPOSE_SCOPE": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "COMPOSE_SCOPE"])
        ),
    },
)
def env(
    context: AssetExecutionContext,
    group_in: dict,  # pylint: disable=redefined-outer-name
    constants: dict,  # pylint: disable=redefined-outer-name
    FEATURE_CONFIG: OpenStudioLandscapesConfig,  # pylint: disable=redefined-outer-name
    COMPOSE_SCOPE: ComposeScope,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:

    env_in = copy.deepcopy(group_in["env"])

    env_in.update(
        expand_dict_vars(
            dict_to_expand=constants[FEATURE_CONFIG],
            kv=env_in,
        )
    )

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
            "ENVIRONMENT": MetadataValue.json(constants[FEATURE_CONFIG]),
        },
    )


@asset(
    **ASSET_HEADER,
)
def compose_networks(
    context: AssetExecutionContext,
) -> Generator[
    Output[dict[str, dict[str, dict[str, str]]]] | AssetMaterialization, None, None
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
        "group_in": AssetIn(AssetKey([*KEY_BASE, "group_out"])),
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
    group_in: dict,  # pylint: disable=redefined-outer-name
    apt_packages: dict[str, list[str]],  # pylint: disable=redefined-outer-name
    script_init_db: pathlib.Path,  # pylint: disable=redefined-outer-name
    inject_postgres_conf: pathlib.Path,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    # Todo:
    """
dagster._core.errors.DagsterExecutionStepExecutionError: Error occurred while executing op "Kitsu__build_docker_image":
  File "/home/michael/git/repos/OpenStudioLandscapes/.venv/lib/python3.11/site-packages/dagster/_core/execution/plan/execute_plan.py", line 245, in dagster_event_sequence_for_step
    yield from check.generator(step_events)
  File "/home/michael/git/repos/OpenStudioLandscapes/.venv/lib/python3.11/site-packages/dagster/_core/execution/plan/execute_step.py", line 501, in core_dagster_event_sequence_for_step
    for user_event in _step_output_error_checked_user_event_sequence(
  File "/home/michael/git/repos/OpenStudioLandscapes/.venv/lib/python3.11/site-packages/dagster/_core/execution/plan/execute_step.py", line 184, in _step_output_error_checked_user_event_sequence
    for user_event in user_event_sequence:
  File "/home/michael/git/repos/OpenStudioLandscapes/.venv/lib/python3.11/site-packages/dagster/_core/execution/plan/execute_step.py", line 88, in _process_asset_results_to_events
    for user_event in user_event_sequence:
  File "/home/michael/git/repos/OpenStudioLandscapes/.venv/lib/python3.11/site-packages/dagster/_core/execution/plan/compute.py", line 190, in execute_core_compute
    for step_output in _yield_compute_results(step_context, inputs, compute_fn, compute_context):
  File "/home/michael/git/repos/OpenStudioLandscapes/.venv/lib/python3.11/site-packages/dagster/_core/execution/plan/compute.py", line 159, in _yield_compute_results
    for event in iterate_with_context(
  File "/home/michael/git/repos/OpenStudioLandscapes/.venv/lib/python3.11/site-packages/dagster/_utils/__init__.py", line 478, in iterate_with_context
    with context_fn():
  File "/usr/lib/python3.11/contextlib.py", line 158, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/home/michael/git/repos/OpenStudioLandscapes/.venv/lib/python3.11/site-packages/dagster/_core/execution/plan/utils.py", line 86, in op_execution_error_boundary
    raise error_cls(
The above exception was caused by the following exception:
python_on_whales.exceptions.DockerException: The command executed was `/usr/bin/docker build --quiet --pull --file /home/michael/git/repos/OpenStudioLandscapes/.landscapes/2025-04-02-01-43-52-f91bf05993fa4bbc86eeebcf293e84bd/Kitsu__Kitsu/Kitsu__build_docker_image/Dockerfiles/Dockerfile --tag openstudiolandscapes/kitsu_build_docker_image:2025-04-02-01-43-52-f91bf05993fa4bbc86eeebcf293e84bd --tag harbor.farm.evil:80/openstudiolandscapes/kitsu_build_docker_image:2025-04-02-01-43-52-f91bf05993fa4bbc86eeebcf293e84bd /home/michael/git/repos/OpenStudioLandscapes/.landscapes/2025-04-02-01-43-52-f91bf05993fa4bbc86eeebcf293e84bd/Kitsu__Kitsu/Kitsu__build_docker_image/Dockerfiles`.
It returned with code 1
The content of stdout is ''
The content of stderr is 'Dockerfile:5
--------------------
   3 |     # http://localhost:3000/asset-groups/Kitsu%2Fbuild_docker_image
   4 |     # https://hub.docker.com/r/cgwire/cgwire
   5 | >>> FROM cgwire/cgwire:latest AS kitsu_build_docker_image
   6 |     LABEL authors="michimussato@gmail.com"
   7 |
--------------------
ERROR: failed to solve: cgwire/cgwire:latest: failed to resolve source metadata for docker.io/cgwire/cgwire:latest: failed to authorize: failed to fetch anonymous token: Get "https://auth.docker.io/token?scope=repository%3Acgwire%2Fcgwire%3Apull&service=registry.docker.io": net/http: TLS handshake timeout
'

  File "/home/michael/git/repos/OpenStudioLandscapes/.venv/lib/python3.11/site-packages/dagster/_core/execution/plan/utils.py", line 56, in op_execution_error_boundary
    yield
  File "/home/michael/git/repos/OpenStudioLandscapes/.venv/lib/python3.11/site-packages/dagster/_utils/__init__.py", line 480, in iterate_with_context
    next_output = next(iterator)
                  ^^^^^^^^^^^^^^
  File "/home/michael/git/repos/OpenStudioLandscapes-Kitsu/src/OpenStudioLandscapes/Kitsu/assets.py", line 309, in build_docker_image
    tags_list: list = docker_build(
                      ^^^^^^^^^^^^^
  File "/home/michael/git/repos/OpenStudioLandscapes/src/OpenStudioLandscapes/engine/utils/docker/whales.py", line 133, in docker_build
    raise e
  File "/home/michael/git/repos/OpenStudioLandscapes/src/OpenStudioLandscapes/engine/utils/docker/whales.py", line 109, in docker_build
    image: Image = docker_client.legacy_build(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/michael/git/repos/OpenStudioLandscapes/.venv/lib/python3.11/site-packages/python_on_whales/components/image/cli_wrapper.py", line 279, in legacy_build
    image_id = run(full_cmd).splitlines()[-1].strip()
               ^^^^^^^^^^^^^
  File "/home/michael/git/repos/OpenStudioLandscapes/.venv/lib/python3.11/site-packages/python_on_whales/utils.py", line 220, in run
    raise DockerException(
    """

    build_base_image_data: dict = group_in["docker_image"]
    build_base_docker_config: DockerConfig = group_in["docker_config"]

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
        f"{GROUP}__{'__'.join(KEY)}",
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

    context.log.debug(image_data)

    tags_list: list = docker_build(
        context=context,
        docker_config=build_base_docker_config,
        docker_file=docker_file,
        context_path=docker_file.parent,
        docker_use_cache=DOCKER_USE_CACHE,
        image_data=image_data,
    )

    yield Output(image_data)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(image_data),
            "tags_list": MetadataValue.json(tags_list),
            "docker_file": MetadataValue.md(f"```shell\n{docker_file_content}\n```"),
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
            "postgres_conf": MetadataValue.md(
                f"```shell\n{postgres_conf_content}\n```"
            ),
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
                "domainname": env.get("ROOT_DOMAIN"),
                "restart": "always",
                "environment": {
                    # https://zou.cg-wire.com/
                    # "LC_ALL": "C.UTF-8",
                    # "LANG": "C.UTF-8",
                    "KITSU_ADMIN": env.get("KITSU_ADMIN_USER", "admin@example.com"),
                    "DB_PASSWORD": env.get("KITSU_DB_PASSWORD", "mysecretpassword"),
                    "SECRET_KEY": env.get("SECRET_KEY", "yourrandomsecretkey"),
                    "PREVIEW_FOLDER": env.get(
                        "KITSU_PREVIEW_FOLDER", "/opt/zou/previews"
                    ),
                    "TMP_DIR": env.get("KITSU_TMP_DIR", "/opt/zou/tmp"),
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
            AssetKey([*KEY, "env"]),
        ),
        "build": AssetIn(
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
    build: dict,  # pylint: disable=redefined-outer-name
    # compose_networks: dict,  # pylint: disable=redefined-outer-name
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
                "domainname": env.get("ROOT_DOMAIN"),
                "environment": {
                    # https://zou.cg-wire.com/
                    # "LC_ALL": "C.UTF-8",
                    # "LANG": "C.UTF-8",
                    "KITSU_ADMIN": env.get("KITSU_ADMIN_USER", "admin@example.com"),
                    "DB_PASSWORD": env.get("KITSU_DB_PASSWORD", "mysecretpassword"),
                    "SECRET_KEY": env.get("SECRET_KEY", "yourrandomsecretkey"),
                    "PREVIEW_FOLDER": env.get(
                        "KITSU_PREVIEW_FOLDER", "/opt/zou/previews"
                    ),
                    "TMP_DIR": env.get("KITSU_TMP_DIR", "/opt/zou/tmp"),
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
            AssetKey([*KEY, "compose_kitsu"]),
        ),
        "compose_init_db": AssetIn(
            AssetKey([*KEY, "compose_init_db"]),
        ),
    },
)
def compose_maps(
    context: AssetExecutionContext,
    **kwargs,  # pylint: disable=redefined-outer-name
) -> Generator[Output[list[dict]] | AssetMaterialization, None, None]:

    ret = list(kwargs.values())

    context.log.info(ret)

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )


compose = AssetsDefinition.from_op(
    op_compose,
    tags_by_output_name={
        "compose": {
            "compose": "third_party",
        },
    },
    group_name=GROUP,
    key_prefix=KEY,
    keys_by_input_name={
        "compose_networks": AssetKey([*KEY, "compose_networks"]),
        "compose_maps": AssetKey([*KEY, "compose_maps"]),
    },
)


group_out = AssetsDefinition.from_op(
    op_group_out,
    can_subset=True,
    group_name=GROUP,
    tags_by_output_name={
        "group_out": {
            "group_out": "third_party",
        },
    },
    key_prefix=KEY,
    keys_by_input_name={
        "compose": AssetKey([*KEY, "compose"]),
        "env": AssetKey([*KEY, "env"]),
        "group_in": AssetKey([*KEY_BASE, "group_out"]),
    },
)


docker_compose_graph = AssetsDefinition.from_op(
    op_docker_compose_graph,
    group_name=GROUP,
    key_prefix=KEY,
    keys_by_input_name={
        "group_out": AssetKey([*KEY, "group_out"]),
        "compose_project_name": AssetKey([*KEY, "compose_project_name"]),
    },
)
