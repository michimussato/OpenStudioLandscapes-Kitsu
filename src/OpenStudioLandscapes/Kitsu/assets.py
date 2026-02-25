import copy
import enum
import pathlib
import shutil
import textwrap
import urllib.parse
from typing import Dict, Generator, List, Union

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
from OpenStudioLandscapes.engine.common_assets.cmd import get_feature__cmd
from OpenStudioLandscapes.engine.common_assets.compose import get_compose

# from OpenStudioLandscapes.engine.common_assets.compose_scope import (
#     get_compose_scope_group__cmd,
# )
from OpenStudioLandscapes.engine.common_assets.docker_compose_graph import (
    get_docker_compose_graph,
)
from OpenStudioLandscapes.engine.common_assets.feature import get_feature__CONFIG
from OpenStudioLandscapes.engine.common_assets.feature_out import get_feature_out_v2
from OpenStudioLandscapes.engine.common_assets.group_in import (
    get_feature_in,
    get_feature_in_parent,
)
from OpenStudioLandscapes.engine.common_assets.group_out import get_group_out
from OpenStudioLandscapes.engine.config.models import ConfigEngine, DockerConfigModel
from OpenStudioLandscapes.engine.constants import *
from OpenStudioLandscapes.engine.enums import *
from OpenStudioLandscapes.engine.link.models import OpenStudioLandscapesFeatureIn
from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.utils.docker.compose_dicts import *

from OpenStudioLandscapes.Kitsu import dist
from OpenStudioLandscapes.Kitsu.config.models import CONFIG_STR, Config
from OpenStudioLandscapes.Kitsu.constants import *

# https://github.com/yaml/pyyaml/issues/722#issuecomment-1969292770
yaml.SafeDumper.add_multi_representer(
    data_type=enum.Enum,
    representer=yaml.representer.SafeRepresenter.represent_str,
)


cmd: AssetsDefinition = get_feature__cmd(
    ASSET_HEADER=ASSET_HEADER,
)

CONFIG: AssetsDefinition = get_feature__CONFIG(
    ASSET_HEADER=ASSET_HEADER,
    CONFIG_STR=CONFIG_STR,
    search_model_of_type=Config,
)

feature_in: AssetsDefinition = get_feature_in(
    ASSET_HEADER=ASSET_HEADER,
    ASSET_HEADER_BASE=ASSET_HEADER_BASE,
    ASSET_HEADER_FEATURE_IN={},
)

group_out: AssetsDefinition = get_group_out(
    ASSET_HEADER=ASSET_HEADER,
)


docker_compose_graph: AssetsDefinition = get_docker_compose_graph(
    ASSET_HEADER=ASSET_HEADER,
)


compose: AssetsDefinition = get_compose(
    ASSET_HEADER=ASSET_HEADER,
)


feature_out_v2: AssetsDefinition = get_feature_out_v2(
    ASSET_HEADER=ASSET_HEADER,
)


# Produces
# - feature_in_parent
# - CONFIG_PARENT
# if ConfigParent is or type FeatureBaseModel
feature_in_parent: Union[AssetsDefinition, None] = get_feature_in_parent(
    ASSET_HEADER=ASSET_HEADER,
    config_parent=ConfigParent,
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
    CONFIG: Config,  # pylint: disable=redefined-outer-name
) -> Generator[
    Output[Dict[str, Dict[str, Dict[str, str]]]] | AssetMaterialization,
    None,
    None,
]:

    env: Dict = CONFIG.env

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
            "compose_network_mode": MetadataValue.text(compose_network_mode.value),
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "feature_in": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "feature_in"]),
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
)
def build_docker_image(
    context: AssetExecutionContext,
    feature_in: OpenStudioLandscapesFeatureIn,  # pylint: disable=redefined-outer-name
    CONFIG: Config,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Dict] | AssetMaterialization, None, None]:
    """ """

    env: Dict = CONFIG.env

    docker_config_json: pathlib.Path = (
        feature_in.openstudiolandscapes_base.docker_config_json
    )

    config_engine: ConfigEngine = CONFIG.config_engine

    docker_config: DockerConfigModel = config_engine.openstudiolandscapes__docker_config

    docker_image: Dict = feature_in.openstudiolandscapes_base.docker_image_base

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

    # apt_install_str_base: str = get_apt_install_str(
    #     apt_install_packages=CONFIG.apt_packages,
    # )

    # We override the default `python_str` because
    # the Python interpreter for the Kitsu Docker image is nothing
    # we are in charge of
    pip_install_str: str = get_pip_install_str(
        pip_install_packages=CONFIG.pip_packages, python_str="/opt/zou/env/bin/python"
    )

    # @formatter:off
    docker_file_str = textwrap.dedent("""\
        # {auto_generated}
        # {dagster_url}
        # https://hub.docker.com/r/cgwire/cgwire
        FROM {parent_image} AS {image_name}
        LABEL authors="{AUTHOR}"

        {pip_install_str}

        WORKDIR /opt/zou

        ENTRYPOINT []
        """).format(
        # apt_install_str_base=apt_install_str_base,
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
        parent_image=CONFIG.docker_image,
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
            "docker_file": MetadataValue.md(f"```yaml\n{docker_file_content}\n```"),
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
def postgres_conf(
    context: AssetExecutionContext,
    CONFIG: Config,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:
    """ """

    env: Dict = CONFIG.env

    postgres_conf_script = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{dist.name}",
        "__".join(context.asset_key.path),
        "postgresql.conf",
    )

    postgres_conf_script.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(
            file=postgres_conf_script,
            mode="w",
        ) as fw:
            fw.write(CONFIG.kitsu_postgres_conf_str)
    except PermissionError as e:
        context.log.warning(f"File permissions have already been assigned to `postgres:postgres`, "
                            f"can't write content to file: {e}")
        # Todo
        #  - [ ] Maybe have some logic to compare the two strings

    yield Output(postgres_conf_script)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(postgres_conf_script),
            "postgres_conf": MetadataValue.md(
                f"```markdown\n{CONFIG.kitsu_postgres_conf_str}\n```"
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
    CONFIG: Config,  # pylint: disable=redefined-outer-name
) -> Generator[Output[pathlib.Path] | AssetMaterialization, None, None]:
    """ """

    env: Dict = CONFIG.env

    init_db = {}

    """
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
        self.__connect()
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
        with util.safe_reraise():
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
        raise exc_value.with_traceback(exc_tb)
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
        self.dbapi_connection = connection = pool._invoke_creator(self)
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 661, in connect
        return dialect.connect(*cargs, **cparams)
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 630, in connect
        return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
      File "/opt/zou/env/lib/python3.10/site-packages/psycopg/connection.py", line 122, in connect
        raise last_ex.with_traceback(None)
    psycopg.OperationalError: connection failed: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  role "root" does not exist
    The above exception was the direct cause of the following exception:
    Traceback (most recent call last):
      File "/opt/zou/env/bin/zou", line 6, in <module>
        sys.exit(cli())
      File "/opt/zou/env/lib/python3.10/site-packages/click/core.py", line 1485, in __call__
        return self.main(*args, **kwargs)
      File "/opt/zou/env/lib/python3.10/site-packages/click/core.py", line 1406, in main
        rv = self.invoke(ctx)
      File "/opt/zou/env/lib/python3.10/site-packages/click/core.py", line 1873, in invoke
        return _process_result(sub_ctx.command.invoke(sub_ctx))
      File "/opt/zou/env/lib/python3.10/site-packages/click/core.py", line 1269, in invoke
        return ctx.invoke(self.callback, **ctx.params)
      File "/opt/zou/env/lib/python3.10/site-packages/click/core.py", line 824, in invoke
        return callback(*args, **kwargs)
      File "/opt/zou/env/lib/python3.10/site-packages/zou/cli.py", line 224, in init_data
        commands.init_data()
      File "/opt/zou/env/lib/python3.10/site-packages/zou/app/utils/commands.py", line 68, in init_data
        projects_service.get_open_status()
      File "/opt/zou/env/lib/python3.10/site-packages/flask_caching/__init__.py", line 899, in decorated_function
        rv = self._call_fn(f, *args, **kwargs)
      File "/opt/zou/env/lib/python3.10/site-packages/flask_caching/__init__.py", line 185, in _call_fn
        return ensure_sync(fn)(*args, **kwargs)
      File "/opt/zou/env/lib/python3.10/site-packages/zou/app/services/projects_service.py", line 203, in get_open_status
        return get_or_create_status("Open")
      File "/opt/zou/env/lib/python3.10/site-packages/zou/app/services/projects_service.py", line 218, in get_or_create_status
        project_status = ProjectStatus.get_by(name=name)
      File "/opt/zou/env/lib/python3.10/site-packages/zou/app/models/base.py", line 50, in get_by
        return cls.query.filter(*criterions).filter_by(**kw).first()
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/orm/query.py", line 2759, in first
        return self.limit(1)._iter().first()  # type: ignore
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/orm/query.py", line 2857, in _iter
        result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
        return self._execute_internal(
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2239, in _execute_internal
        conn = self._connection_for_bind(bind)
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2108, in _connection_for_bind
        return trans._connection_for_bind(engine, execution_options)
      File "<string>", line 2, in _connection_for_bind
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
        ret_value = fn(self, *arg, **kw)
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 1187, in _connection_for_bind
        conn = bind.connect()
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3285, in connect
        return self._connection_cls(self)
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
        Connection._handle_dbapi_exception_noconnection(
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 2448, in _handle_dbapi_exception_noconnection
        raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
        self._dbapi_connection = engine.raw_connection()
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3309, in raw_connection
        return self.pool.connect()
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 447, in connect
        return _ConnectionFairy._checkout(self)
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
        fairy = _ConnectionRecord.checkout(pool)
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
        rec = pool._do_get()
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
        with util.safe_reraise():
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
        raise exc_value.with_traceback(exc_tb)
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
        return self._create_connection()
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
        return _ConnectionRecord(self)
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
        self.__connect()
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
        with util.safe_reraise():
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
        raise exc_value.with_traceback(exc_tb)
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
        self.dbapi_connection = connection = pool._invoke_creator(self)
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 661, in connect
        return dialect.connect(*cargs, **cparams)
      File "/opt/zou/env/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 630, in connect
        return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
      File "/opt/zou/env/lib/python3.10/site-packages/psycopg/connection.py", line 122, in connect
        raise last_ex.with_traceback(None)
    sqlalchemy.exc.OperationalError: (psycopg.OperationalError) connection failed: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  role "root" does not exist
    (Background on this error at: https://sqlalche.me/e/20/e3q8)
    """

    """
    # v1.0.11
    $ cat init_zou.sh
    #!/bin/bash
    export LC_ALL=C.UTF-8
    export LANG=C.UTF-8
    
    service postgresql start
    service redis-server start
    
    . /opt/zou/env/bin/activate
    
    zou upgrade-db
    zou init-data
    zou create-admin admin@example.com --password mysecretpassword
    
    service postgresql stop
    service redis-server stop
    """

    """
    # v1.0.11
    $ cat start_zou.sh 
    #!/bin/bash
    
    # create /var/run/postgresql
    . /usr/share/postgresql-common/init.d-functions
    create_socket_directory
    
    echo Running Zou...
    supervisord -c /etc/supervisord.conf
    """

    # Todo:
    #  - [ ] Make sure the database gets updated if a newer image version is pulled
    #        - https://hub.docker.com/r/cgwire/cgwire#usage
    #          - $ docker exec -ti cgwire sh -c "zou upgrade-db"
    #            - [x] Bug report: https://github.com/cgwire/zou/issues/1019
    #          - docker run --init -ti --rm -p 80:80 --name cgwire -v zou-storage:/var/lib/postgresql -v zou-storage:/opt/zou/previews cgwire/cgwire bash

    init_db["exe"] = shutil.which("bash")

    # https://github.com/michimussato/kitsu-setup/blob/main/README_KITSU.md
    init_db["script"] = textwrap.dedent("""\
        #!/bin/bash
        # Documentation:
        # https://zou.cg-wire.com/
    
        whoami

        function init_postgres_db() {
            # This initializes PostgreSQL in case we are bind mounting
            # an empty directory: /var/lib/postgresql
            if [[ -z "$( ls -A '/var/lib/postgresql')" ]]; then
        
                echo "/var/lib/postgresql empty."
                echo "Initializing DB..."
        
                mkdir -p /var/lib/postgresql/14/main
                chown -R postgres:postgres /var/lib/postgresql/14
                # data ownership and conf ownership have to match
                # user id of `postgres` is 105
                chown postgres:postgres /etc/postgresql/14/main/postgresql.conf
        
                # Default encoding without specifying it is SQL_ASCII
                # psql zoudb -c 'SHOW SERVER_ENCODING'
                su - postgres -c '/usr/lib/postgresql/14/bin/initdb --pgdata=/var/lib/postgresql/14/main --auth=trust --encoding=UTF8'
        
                # USER postgres
                echo "Starting postresql..."
                service postgresql start
                echo "Starting redis-server..."
                service redis-server start
        
                # set user password as specified in the config.yml
                su - postgres -c "psql -U postgres -d postgres -c \\\"alter user postgres with password '${DB_PASSWORD}';\\\""
        
                # as of v1.0.11, `sudo` seems no longer available
                #
                # https://hub.docker.com/layers/cgwire/cgwire/1.0.11/images/sha256-9917b49236c23c8f5e700ad2d33ec2edb294b373533759c9bba3d9780a0a9648
                # RUN |2 ZOU_VERSION=1.0.8 KITSU_VERSION=1.0.11 /bin/sh -c service postgresql start &&
                # createuser root
                # && createdb -T template0 -E UTF8 --owner root root
                # &&     createdb -T template0 -E UTF8 --owner root zoudb
                # &&     service postgresql stop
                su - postgres -c "createuser root"
                su - postgres -c "createdb -T template0 -E UTF8 --owner root root"
                su - postgres -c "createdb -T template0 -E UTF8 --owner root zoudb"
                # su - postgres -c "psql -U postgres -c 'create database zoudb;'"
        
                echo "Stopping postresql..."
                service postgresql stop
                echo "Stopping redis-server..."
                service redis-server stop
        
                # service redis-server is down but process seems to persist
                # for some reason
                echo "Killing redis..."
                pkill redis
        
                echo "Postgres DB successfully initialized."
        
            else
        
                echo "/var/lib/postgresql is not empty."
                echo "Nothing to initialize."
        
            fi
        }
        
        function init_kitsu_db() {
        
            # USER postgres
            echo "Starting postresql..."
            service postgresql start
            echo "Starting redis-server..."
            service redis-server start
        
            . /opt/zou/env/bin/activate
        
            echo "zou is-db-ready..."
            IS_DB_READY=$(zou is-db-ready)
            echo ${IS_DB_READY}
        
            if [ "${IS_DB_READY}" == "Database is not initialized. Run 'zou init-db' and 'zou init-data'." ]; then
        
                echo "zou init-db..."
                zou init-db
                # echo "zou upgrade-db..."
                # zou upgrade-db
                echo "zou init-data..."
                zou init-data
        
                mkdir -p ${TMP_DIR}
                chown -R postgres:postgres ${TMP_DIR}
        
                echo "zou create-admin..."
                zou create-admin --password ${DB_PASSWORD} ${KITSU_ADMIN}
        
            fi;
        
            echo "Stopping postresql..."
            service postgresql stop
            echo "Stopping redis-server..."
            service redis-server stop
        
            # service redis-server is down but process seems to persist
            # for some reason
            echo "Killing redis..."
            pkill redis
        
            echo "DB successfully initialized."
        
            echo "Exitting as planned."
            exit 0
        }
        
        init_postgres_db
        init_kitsu_db
        """)

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
    CONFIG: Config,  # pylint: disable=redefined-outer-name
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

    # Compatible with:
    # - [x] 0.9.x
    # - [ ] 1.0.11
    supervisord_conf_str = textwrap.dedent("""\
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
        """)

    if CONFIG.kitsu_enable_job_queue:
        supervisord_conf_str += textwrap.dedent("""
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
            """)

    else:
        supervisord_conf_str += textwrap.dedent("""
            [group:zou-processes]
            programs=gunicorn,gunicorn-events
            priority=5
            """)

    supervisord_conf_str += textwrap.dedent("""
        [unix_http_server]
        file=/tmp/supervisor.sock

        [supervisorctl]
        serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket

        [rpcinterface:supervisor]
        supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface
        """)

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
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
        "build": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "build_docker_image"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_networks"]),
        ),
        "supervisord_conf": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "supervisord_conf"]),
        ),
        "postgres_conf": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "postgres_conf"]),
        ),
    },
)
def compose_kitsu(
    context: AssetExecutionContext,
    CONFIG: Config,  # pylint: disable=redefined-outer-name
    build: Dict,  # pylint: disable=redefined-outer-name
    compose_networks: Dict,  # pylint: disable=redefined-outer-name
    supervisord_conf: pathlib.Path,  # pylint: disable=redefined-outer-name
    postgres_conf: pathlib.Path,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Dict] | AssetMaterialization, None, None]:
    """ """

    env: Dict = CONFIG.env

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

        kitsu_db_dir_host = CONFIG.kitsu_database_install_destination_expanded
        kitsu_db_dir_host.mkdir(parents=True, exist_ok=True)
        context.log.info(f"Directory {kitsu_db_dir_host.as_posix()} created.")

        kitsu_preview_dir_host = CONFIG.kitsu_preview_folder_expanded
        kitsu_preview_dir_host.mkdir(parents=True, exist_ok=True)
        context.log.info(f"Directory {kitsu_preview_dir_host.as_posix()} created.")

        kitsu_tmp_dir_host = CONFIG.kitsu_tmp_dir_expanded
        kitsu_tmp_dir_host.mkdir(parents=True, exist_ok=True)
        context.log.info(f"Directory {kitsu_tmp_dir_host.as_posix()} created.")

        # maybe use collections.deque()?
        volumes_dict["volumes"] = [
            f"{kitsu_db_dir_host.as_posix()}:/var/lib/postgresql:rw",
            f"{kitsu_preview_dir_host.as_posix()}:/opt/zou/previews:rw",
            f"{kitsu_tmp_dir_host.as_posix()}:/opt/zou/tmp:rw",
            # f"{script_init_db.as_posix()}:/opt/zou/init_db.sh",
            f"{postgres_conf.as_posix()}:/etc/postgresql/14/main/postgresql.conf:ro",
            *volumes_dict["volumes"],
        ]

    # For portability, convert absolute volume paths to relative paths

    _volume_relative = []

    for v in volumes_dict["volumes"]:

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
        "volumes": list(
            {
                *_volume_relative,
                *config_engine.global_bind_volumes,
                *CONFIG.local_bind_volumes,
            }
        )
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
                    "TZ": config_engine.tz,
                    # https://zou.cg-wire.com/
                    # "LC_ALL": "C.UTF-8",
                    # "LANG": "C.UTF-8",
                    "KITSU_ADMIN": CONFIG.kitsu_admin_user,
                    "DB_PASSWORD": CONFIG.kitsu_db_password,
                    "SECRET_KEY": CONFIG.kitsu_secret_key,
                    "PREVIEW_FOLDER": "/opt/zou/previews",
                    "TMP_DIR": "/opt/zou/tmp",
                    "ENABLE_JOB_QUEUE": CONFIG.kitsu_enable_job_queue,
                    **config_engine.global_environment_variables,
                    **CONFIG.local_environment_variables,
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
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "build": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "build_docker_image"]),
        ),
        "script_init_db": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "script_init_db"]),
        ),
        "postgres_conf": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "postgres_conf"]),
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
    build: Dict,  # pylint: disable=redefined-outer-name
    script_init_db: pathlib.Path,  # pylint: disable=redefined-outer-name
    postgres_conf: pathlib.Path,  # pylint: disable=redefined-outer-name
    CONFIG: Config,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Dict] | AssetMaterialization, None, None]:
    """ """

    env: Dict = CONFIG.env

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

    kitsu_db_dir_host = CONFIG.kitsu_database_install_destination_expanded
    kitsu_db_dir_host.mkdir(parents=True, exist_ok=True)
    context.log.info(f"Directory {kitsu_db_dir_host.as_posix()} created.")

    # Is:
    # - /home/michael/git/repos/OpenStudioLandscapes/.landscapes/2025-07-12-15-44-28-d7511d9a293d496daed627176a026b43/Kitsu__Kitsu/data/kitsu/postgresql:/var/lib/postgresql
    #
    # Want:
    # - ../../../../2025-07-10-22-36-50-47cd6c0a7dd141429707ab6d91190a27/Kitsu__Kitsu/data/kitsu/postgresql:/var/lib/postgresql
    #
    # Get:
    # - ../../../../2025-07-12-15-44-28-d7511d9a293d496daed627176a026b43/Kitsu__Kitsu/data/kitsu/postgresql:/var/lib/postgresql

    # For portability, convert absolute volume paths to relative paths
    volumes_paths_to_convert = [
        f"{kitsu_db_dir_host.as_posix()}:/var/lib/postgresql",
        f"{script_init_db.as_posix()}:/opt/zou/init_db.sh:ro",
        f"{postgres_conf.as_posix()}:/etc/postgresql/14/main/postgresql.conf:rw",
    ]

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
        "volumes": list(
            {
                *_volume_relative,
                *config_engine.global_bind_volumes,
                *CONFIG.local_bind_volumes,
            }
        )
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
                    "TZ": config_engine.tz,
                    # https://zou.cg-wire.com/
                    # "LC_ALL": "C.UTF-8",
                    # "LANG": "C.UTF-8",
                    "KITSU_ADMIN": CONFIG.kitsu_admin_user,
                    "DB_PASSWORD": CONFIG.kitsu_db_password,
                    "SECRET_KEY": CONFIG.kitsu_secret_key,
                    "PREVIEW_FOLDER": "/opt/zou/previews",
                    "TMP_DIR": "/opt/zou/tmp",
                    **config_engine.global_environment_variables,
                    **CONFIG.local_environment_variables,
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
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
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
) -> Generator[Output[List[Dict]] | AssetMaterialization, None, None]:

    ret = list(kwargs.values())

    context.log.info(ret)

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )
