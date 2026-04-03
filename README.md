[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

***

1. [Feature: OpenStudioLandscapes-Kitsu](#feature-openstudiolandscapes-kitsu)
   1. [Brief](#brief)
   2. [Clone](#clone)
      1. [Clone and Install](#clone-and-install)
   3. [Configure](#configure)
      1. [Default Configuration](#default-configuration)
2. [External Resources](#external-resources)
   1. [Inofficial Resources](#inofficial-resources)
3. [Community](#community)

***

This `README.md` was dynamically created with [OpenStudioLandscapesUtil-ReadmeGenerator](https://github.com/michimussato/OpenStudioLandscapesUtil-ReadmeGenerator).

***

# Feature: OpenStudioLandscapes-Kitsu

## Brief

This is an extension to the OpenStudioLandscapes ecosystem. The full documentation of OpenStudioLandscapes is available [here](https://github.com/michimussato/OpenStudioLandscapes).

> [!NOTE]
> 
> You feel like writing your own Feature? Go and check out the 
> [OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template).

## Clone

Clone this repository into `OpenStudioLandscapes/.features` (assuming the current working directory to be the Git repository root `./OpenStudioLandscapes`):

```shell
# cd OpenStudioLandscapes
source .venv/bin/activate
openstudiolandscapes clone-feature --repo=https://github.com/michimussato/OpenStudioLandscapes-Kitsu.git
deactivate
# Check the resulting console output for installation instructions

```

### Clone and Install

```shell
# cd OpenStudioLandscapes
source .venv/bin/activate
openstudiolandscapes clone-feature --repo=https://github.com/michimussato/OpenStudioLandscapes-Kitsu.git \
    && pip install --editable ./.features/OpenStudioLandscapes-Kitsu
deactivate

```

For more info on `pip` see [VCS Support of `pip`](https://pip.pypa.io/en/stable/topics/vcs-support/).

## Configure

OpenStudioLandscapes will search for a local config store. The default location is `~/.config/OpenStudioLandscapes/config-store/` but you can specify a different location if you need to.

> [!TIP]
> 
> To specify a config store location different from
> the default location, check out the OpenStudioLandscapes 
> [CLI Section](https://github.com/michimussato/OpenStudioLandscapes#cli)
> to find out how to do that.

A local config store location will be created if it doesn't exist, together with the `config.yml` files for each individual Feature.

> [!TIP]
> 
> The config store root will be initialized as a local Git
> controlled repository. This makes it easy to track changes
> you made to the `config.yml`.

The following settings are available in `OpenStudioLandscapes-Kitsu` and are based on [`OpenStudioLandscapes-Kitsu/tree/main/OpenStudioLandscapes/Kitsu/config/models.py`](https://github.com/michimussato/OpenStudioLandscapes-Kitsu/tree/main/OpenStudioLandscapes/Kitsu/config/models.py).

### Default Configuration


<details open>
<summary><code>config.yml</code></summary>


```yaml
# ===
# env
# ---
#
# Type: typing.Dict
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ==================
# local_bind_volumes
# ------------------
#
# Type: typing.List[str]
# Base Class Info:
#     Required:
#         False
#     Description:
#         Here you can define Feature specific, arbitrary, absolute bind volume mappings.
#     Default value:
#         PydanticUndefined
# Description:
#     Here you can define Feature specific, arbitrary, absolute bind volume mappings.
# Required:
#     False
# Examples:
#     None


# ===========================
# local_environment_variables
# ---------------------------
#
# Type: typing.Dict[str, str]
# Base Class Info:
#     Required:
#         False
#     Description:
#         Here you can define Feature specific, arbitrary environment variables.
#     Default value:
#         PydanticUndefined
# Description:
#     Here you can define Feature specific, arbitrary environment variables.
# Required:
#     False
# Examples:
#     None


# =============
# config_engine
# -------------
#
# Type: <class 'OpenStudioLandscapes.engine.config.models.ConfigEngine'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ============
# distribution
# ------------
#
# Type: <class 'importlib.metadata.Distribution'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ==========
# group_name
# ----------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         True
#     Description:
#         Dagster Group name. This will represent the group node name. See https://docs.dagster.io/api/dagster/assets for more information
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
group_name: OpenStudioLandscapes_Kitsu


# ============
# key_prefixes
# ------------
#
# Type: typing.List[str]
# Base Class Info:
#     Required:
#         True
#     Description:
#         Dagster Asset key prefixes. This will be reflected in the nesting (directory structure) of the Asset. See https://docs.dagster.io/api/dagster/assets for more information
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
key_prefixes:
- OpenStudioLandscapes_Kitsu


# =======
# enabled
# -------
#
# Type: <class 'bool'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         Whether the Feature is enabled or not.
#     Default value:
#         True
# Description:
#     Whether the Feature is enabled or not.
# Required:
#     False
# Examples:
#     None


# =============
# compose_scope
# -------------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         default
# Description:
#     None
# Required:
#     False
# Examples:
#     ['default', 'license_server', 'worker']


# ============
# feature_name
# ------------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         True
#     Description:
#         The name of the feature. It is derived from the `OpenStudioLandscapes.<Feature>.dist` attribute.
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
feature_name: OpenStudioLandscapes-Kitsu


# ==============
# docker_compose
# --------------
#
# Type: <class 'pathlib.Path'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         The path to the `docker-compose.yml` file.
#     Default value:
#         {DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/docker_compose/docker-compose.yml
# Description:
#     The path to the `docker-compose.yml` file.
# Required:
#     False
# Examples:
#     None


# ============
# docker_image
# ------------
#
# Type: <class 'str'>
# Description:
#     The Docker image to use
# Required:
#     False
# Examples:
#     None
docker_image: docker.io/cgwire/cgwire:1.0.11


# ================
# kitsu_admin_user
# ----------------
#
# Type: <class 'pydantic.networks.EmailStr'>
# Description:
#     Bug Report: https://github.com/cgwire/zou/issues/960); Changing these values does not seem to have an effect Hence, they are locked to the following values for now.
# Required:
#     False
# Examples:
#     None
kitsu_admin_user: admin@example.com


# =================
# kitsu_db_password
# -----------------
#
# Type: <class 'str'>
# Description:
#     The Postgres database password.
# Required:
#     False
# Examples:
#     None
kitsu_db_password: mysecretpassword


# =======================
# kitsu_postgres_conf_str
# -----------------------
#
# Type: <class 'str'>
# Description:
#     The Kitsu Postgres configuration file.
# Required:
#     False
# Examples:
#     None
kitsu_postgres_conf_str: "\n# /etc/postgresql/14/main/postgresql.conf\n# -----------------------------\n\
  # PostgreSQL configuration file\n# -----------------------------\n#\n# This file\
  \ consists of lines of the form:\n#\n#   name = value\n#\n# (The \"=\" is optional.)\
  \  Whitespace may be used.  Comments are introduced with\n# \"#\" anywhere on a\
  \ line.  The complete list of parameter names and allowed\n# values can be found\
  \ in the PostgreSQL documentation.\n#\n# The commented-out settings shown in this\
  \ file represent the default values.\n# Re-commenting a setting is NOT sufficient\
  \ to revert it to the default value;\n# you need to reload the server.\n#\n# This\
  \ file is read on server startup and when the server receives a SIGHUP\n# signal.\
  \  If you edit the file on a running system, you have to SIGHUP the\n# server for\
  \ the changes to take effect, run \"pg_ctl reload\", or execute\n# \"SELECT pg_reload_conf()\"\
  .  Some parameters, which are marked below,\n# require a server shutdown and restart\
  \ to take effect.\n#\n# Any parameter can also be given as a command-line option\
  \ to the server, e.g.,\n# \"postgres -c log_connections=on\".  Some parameters can\
  \ be changed at run time\n# with the \"SET\" SQL command.\n#\n# Memory units:  B\
  \  = bytes            Time units:  us  = microseconds\n#                kB = kilobytes\
  \                     ms  = milliseconds\n#                MB = megabytes      \
  \               s   = seconds\n#                GB = gigabytes                 \
  \    min = minutes\n#                TB = terabytes                     h   = hours\n\
  #                                                   d   = days\n\n\n#------------------------------------------------------------------------------\n\
  # FILE LOCATIONS\n#------------------------------------------------------------------------------\n\
  \n# The default values of these variables are driven from the -D command-line\n\
  # option or PGDATA environment variable, represented here as ConfigDir.\n\ndata_directory\
  \ = '/var/lib/postgresql/14/main'          # use data in another directory\n   \
  \                                     # (change requires restart)\nhba_file = '/etc/postgresql/14/main/pg_hba.conf'\
  \        # host-based authentication file\n                                    \
  \    # (change requires restart)\nident_file = '/etc/postgresql/14/main/pg_ident.conf'\
  \    # ident configuration file\n                                        # (change\
  \ requires restart)\n\n# If external_pid_file is not explicitly set, no extra PID\
  \ file is written.\nexternal_pid_file = '/var/run/postgresql/14-main.pid'      \
  \             # write an extra PID file\n                                      \
  \  # (change requires restart)\n\n\n#------------------------------------------------------------------------------\n\
  # CONNECTIONS AND AUTHENTICATION\n#------------------------------------------------------------------------------\n\
  \n# - Connection Settings -\n\n#listen_addresses = 'localhost'         # what IP\
  \ address(es) to listen on;\n                                        # comma-separated\
  \ list of addresses;\n                                        # defaults to 'localhost';\
  \ use '*' for all\n                                        # (change requires restart)\n\
  # port = 5433                             # (change requires restart)\nport = 5432\
  \                             # (change requires restart)\nmax_connections = 100\
  \                   # (change requires restart)\n#superuser_reserved_connections\
  \ = 3     # (change requires restart)\nunix_socket_directories = '/var/run/postgresql'\
  \ # comma-separated list of directories\n                                      \
  \  # (change requires restart)\n#unix_socket_group = ''                 # (change\
  \ requires restart)\n#unix_socket_permissions = 0777         # begin with 0 to use\
  \ octal notation\n                                        # (change requires restart)\n\
  #bonjour = off                          # advertise server via Bonjour\n       \
  \                                 # (change requires restart)\n#bonjour_name = ''\
  \                      # defaults to the computer name\n                       \
  \                 # (change requires restart)\n\n# - TCP settings -\n# see \"man\
  \ tcp\" for details\n\n#tcp_keepalives_idle = 0                # TCP_KEEPIDLE, in\
  \ seconds;\n                                        # 0 selects the system default\n\
  #tcp_keepalives_interval = 0            # TCP_KEEPINTVL, in seconds;\n         \
  \                               # 0 selects the system default\n#tcp_keepalives_count\
  \ = 0               # TCP_KEEPCNT;\n                                        # 0\
  \ selects the system default\n#tcp_user_timeout = 0                   # TCP_USER_TIMEOUT,\
  \ in milliseconds;\n                                        # 0 selects the system\
  \ default\n\n#client_connection_check_interval = 0   # time between checks for client\n\
  \                                        # disconnection while running queries;\n\
  \                                        # 0 for never\n\n# - Authentication -\n\
  \n#authentication_timeout = 1min          # 1s-600s\n#password_encryption = scram-sha-256\
  \    # scram-sha-256 or md5\n#db_user_namespace = off\n\n# GSSAPI using Kerberos\n\
  #krb_server_keyfile = 'FILE:${sysconfdir}/krb5.keytab'\n#krb_caseins_users = off\n\
  \n# - SSL -\n\nssl = on\n#ssl_ca_file = ''\nssl_cert_file = '/etc/ssl/certs/ssl-cert-snakeoil.pem'\n\
  #ssl_crl_file = ''\n#ssl_crl_dir = ''\nssl_key_file = '/etc/ssl/private/ssl-cert-snakeoil.key'\n\
  #ssl_ciphers = 'HIGH:MEDIUM:+3DES:!aNULL' # allowed SSL ciphers\n#ssl_prefer_server_ciphers\
  \ = on\n#ssl_ecdh_curve = 'prime256v1'\n#ssl_min_protocol_version = 'TLSv1.2'\n\
  #ssl_max_protocol_version = ''\n#ssl_dh_params_file = ''\n#ssl_passphrase_command\
  \ = ''\n#ssl_passphrase_command_supports_reload = off\n\n\n#------------------------------------------------------------------------------\n\
  # RESOURCE USAGE (except WAL)\n#------------------------------------------------------------------------------\n\
  \n# - Memory -\n\nshared_buffers = 128MB                  # min 128kB\n        \
  \                                # (change requires restart)\n#huge_pages = try\
  \                       # on, off, or try\n                                    \
  \    # (change requires restart)\n#huge_page_size = 0                     # zero\
  \ for system default\n                                        # (change requires\
  \ restart)\n#temp_buffers = 8MB                     # min 800kB\n#max_prepared_transactions\
  \ = 0          # zero disables the feature\n                                   \
  \     # (change requires restart)\n# Caution: it is not advisable to set max_prepared_transactions\
  \ nonzero unless\n# you actively intend to use prepared transactions.\n#work_mem\
  \ = 4MB                         # min 64kB\n#hash_mem_multiplier = 1.0         \
  \     # 1-1000.0 multiplier on hash table work_mem\n#maintenance_work_mem = 64MB\
  \            # min 1MB\n#autovacuum_work_mem = -1               # min 1MB, or -1\
  \ to use maintenance_work_mem\n#logical_decoding_work_mem = 64MB       # min 64kB\n\
  #max_stack_depth = 2MB                  # min 100kB\n#shared_memory_type = mmap\
  \              # the default is the first option\n                             \
  \           # supported by the operating system:\n                             \
  \           #   mmap\n                                        #   sysv\n       \
  \                                 #   windows\n                                \
  \        # (change requires restart)\ndynamic_shared_memory_type = posix      #\
  \ the default is the first option\n                                        # supported\
  \ by the operating system:\n                                        #   posix\n\
  \                                        #   sysv\n                            \
  \            #   windows\n                                        #   mmap\n   \
  \                                     # (change requires restart)\n#min_dynamic_shared_memory\
  \ = 0MB        # (change requires restart)\n\n# - Disk -\n\n#temp_file_limit = -1\
  \                   # limits per-process temp file space\n                     \
  \                   # in kilobytes, or -1 for no limit\n\n# - Kernel Resources -\n\
  \n#max_files_per_process = 1000           # min 64\n                           \
  \             # (change requires restart)\n\n# - Cost-Based Vacuum Delay -\n\n#vacuum_cost_delay\
  \ = 0                  # 0-100 milliseconds (0 disables)\n#vacuum_cost_page_hit\
  \ = 1               # 0-10000 credits\n#vacuum_cost_page_miss = 2              #\
  \ 0-10000 credits\n#vacuum_cost_page_dirty = 20            # 0-10000 credits\n#vacuum_cost_limit\
  \ = 200                # 1-10000 credits\n\n# - Background Writer -\n\n#bgwriter_delay\
  \ = 200ms                 # 10-10000ms between rounds\n#bgwriter_lru_maxpages =\
  \ 100            # max buffers written/round, 0 disables\n#bgwriter_lru_multiplier\
  \ = 2.0          # 0-10.0 multiplier on buffers scanned/round\n#bgwriter_flush_after\
  \ = 512kB           # measured in pages, 0 disables\n\n# - Asynchronous Behavior\
  \ -\n\n#backend_flush_after = 0                # measured in pages, 0 disables\n\
  #effective_io_concurrency = 1           # 1-1000; 0 disables prefetching\n#maintenance_io_concurrency\
  \ = 10        # 1-1000; 0 disables prefetching\n#max_worker_processes = 8      \
  \         # (change requires restart)\n#max_parallel_workers_per_gather = 2    #\
  \ limited by max_parallel_workers\n#max_parallel_maintenance_workers = 2   # limited\
  \ by max_parallel_workers\n#max_parallel_workers = 8               # number of max_worker_processes\
  \ that\n                                        # can be used in parallel operations\n\
  #parallel_leader_participation = on\n#old_snapshot_threshold = -1            # 1min-60d;\
  \ -1 disables; 0 is immediate\n                                        # (change\
  \ requires restart)\n\n\n#------------------------------------------------------------------------------\n\
  # WRITE-AHEAD LOG\n#------------------------------------------------------------------------------\n\
  \n# - Settings -\n\n#wal_level = replica                    # minimal, replica,\
  \ or logical\n                                        # (change requires restart)\n\
  #fsync = on                             # flush data to disk for crash safety\n\
  \                                        # (turning this off can cause\n       \
  \                                 # unrecoverable data corruption)\n#synchronous_commit\
  \ = on                # synchronization level;\n                               \
  \         # off, local, remote_write, remote_apply, or on\n#wal_sync_method = fsync\
  \                # the default is the first option\n                           \
  \             # supported by the operating system:\n                           \
  \             #   open_datasync\n                                        #   fdatasync\
  \ (default on Linux and FreeBSD)\n                                        #   fsync\n\
  \                                        #   fsync_writethrough\n              \
  \                          #   open_sync\n#full_page_writes = on               \
  \   # recover from partial page writes\n#wal_log_hints = off                   \
  \ # also do full page writes of non-critical updates\n                         \
  \               # (change requires restart)\n#wal_compression = off            \
  \      # enable compression of full-page writes\n#wal_init_zero = on           \
  \          # zero-fill new WAL files\n#wal_recycle = on                       #\
  \ recycle WAL files\n#wal_buffers = -1                       # min 32kB, -1 sets\
  \ based on shared_buffers\n                                        # (change requires\
  \ restart)\n#wal_writer_delay = 200ms               # 1-10000 milliseconds\n#wal_writer_flush_after\
  \ = 1MB           # measured in pages, 0 disables\n#wal_skip_threshold = 2MB\n\n\
  #commit_delay = 0                       # range 0-100000, in microseconds\n#commit_siblings\
  \ = 5                    # range 1-1000\n\n# - Checkpoints -\n\n#checkpoint_timeout\
  \ = 5min              # range 30s-1d\n#checkpoint_completion_target = 0.9     #\
  \ checkpoint target duration, 0.0 - 1.0\n#checkpoint_flush_after = 256kB       \
  \  # measured in pages, 0 disables\n#checkpoint_warning = 30s               # 0\
  \ disables\nmax_wal_size = 1GB\nmin_wal_size = 80MB\n\n# - Archiving -\n\n#archive_mode\
  \ = off             # enables archiving; off, on, or always\n                  \
  \              # (change requires restart)\n#archive_command = ''           # command\
  \ to use to archive a logfile segment\n                                # placeholders:\
  \ %p = path of file to archive\n                                #              \
  \ %f = file name only\n                                # e.g. 'test ! -f /mnt/server/archivedir/%f\
  \ && cp %p /mnt/server/archivedir/%f'\n#archive_timeout = 0            # force a\
  \ logfile segment switch after this\n                                # number of\
  \ seconds; 0 disables\n\n# - Archive Recovery -\n\n# These are only used in recovery\
  \ mode.\n\n#restore_command = ''           # command to use to restore an archived\
  \ logfile segment\n                                # placeholders: %p = path of\
  \ file to restore\n                                #               %f = file name\
  \ only\n                                # e.g. 'cp /mnt/server/archivedir/%f %p'\n\
  #archive_cleanup_command = ''   # command to execute at every restartpoint\n#recovery_end_command\
  \ = ''      # command to execute at completion of recovery\n\n# - Recovery Target\
  \ -\n\n# Set these only when performing a targeted recovery.\n\n#recovery_target\
  \ = ''           # 'immediate' to end recovery as soon as a\n                  \
  \              # consistent state is reached\n                                #\
  \ (change requires restart)\n#recovery_target_name = ''      # the named restore\
  \ point to which recovery will proceed\n                                # (change\
  \ requires restart)\n#recovery_target_time = ''      # the time stamp up to which\
  \ recovery will proceed\n                                # (change requires restart)\n\
  #recovery_target_xid = ''       # the transaction ID up to which recovery will proceed\n\
  \                                # (change requires restart)\n#recovery_target_lsn\
  \ = ''       # the WAL LSN up to which recovery will proceed\n                 \
  \               # (change requires restart)\n#recovery_target_inclusive = on # Specifies\
  \ whether to stop:\n                                # just after the specified recovery\
  \ target (on)\n                                # just before the recovery target\
  \ (off)\n                                # (change requires restart)\n#recovery_target_timeline\
  \ = 'latest'    # 'current', 'latest', or timeline ID\n                        \
  \        # (change requires restart)\n#recovery_target_action = 'pause'       #\
  \ 'pause', 'promote', 'shutdown'\n                                # (change requires\
  \ restart)\n\n\n#------------------------------------------------------------------------------\n\
  # REPLICATION\n#------------------------------------------------------------------------------\n\
  \n# - Sending Servers -\n\n# Set these on the primary and on any standby that will\
  \ send replication data.\n\n#max_wal_senders = 10           # max number of walsender\
  \ processes\n                                # (change requires restart)\n#max_replication_slots\
  \ = 10     # max number of replication slots\n                                #\
  \ (change requires restart)\n#wal_keep_size = 0              # in megabytes; 0 disables\n\
  #max_slot_wal_keep_size = -1    # in megabytes; -1 disables\n#wal_sender_timeout\
  \ = 60s       # in milliseconds; 0 disables\n#track_commit_timestamp = off   # collect\
  \ timestamp of transaction commit\n                                # (change requires\
  \ restart)\n\n# - Primary Server -\n\n# These settings are ignored on a standby\
  \ server.\n\n#synchronous_standby_names = '' # standby servers that provide sync\
  \ rep\n                                # method to choose sync standbys, number\
  \ of sync standbys,\n                                # and comma-separated list\
  \ of application_name\n                                # from standby(s); '*' =\
  \ all\n#vacuum_defer_cleanup_age = 0   # number of xacts by which cleanup is delayed\n\
  \n# - Standby Servers -\n\n# These settings are ignored on a primary server.\n\n\
  #primary_conninfo = ''                  # connection string to sending server\n\
  #primary_slot_name = ''                 # replication slot on sending server\n#promote_trigger_file\
  \ = ''              # file name whose presence ends recovery\n#hot_standby = on\
  \                       # \"off\" disallows queries during recovery\n          \
  \                              # (change requires restart)\n#max_standby_archive_delay\
  \ = 30s        # max delay before canceling queries\n                          \
  \              # when reading WAL from archive;\n                              \
  \          # -1 allows indefinite delay\n#max_standby_streaming_delay = 30s    \
  \  # max delay before canceling queries\n                                      \
  \  # when reading streaming WAL;\n                                        # -1 allows\
  \ indefinite delay\n#wal_receiver_create_temp_slot = off    # create temp slot if\
  \ primary_slot_name\n                                        # is not set\n#wal_receiver_status_interval\
  \ = 10s     # send replies at least this often\n                               \
  \         # 0 disables\n#hot_standby_feedback = off             # send info from\
  \ standby to prevent\n                                        # query conflicts\n\
  #wal_receiver_timeout = 60s             # time that receiver waits for\n       \
  \                                 # communication from primary\n               \
  \                         # in milliseconds; 0 disables\n#wal_retrieve_retry_interval\
  \ = 5s       # time to wait before retrying to\n                               \
  \         # retrieve WAL after a failed attempt\n#recovery_min_apply_delay = 0 \
  \          # minimum delay for applying changes during recovery\n\n# - Subscribers\
  \ -\n\n# These settings are ignored on a publisher.\n\n#max_logical_replication_workers\
  \ = 4    # taken from max_worker_processes\n                                   \
  \     # (change requires restart)\n#max_sync_workers_per_subscription = 2  # taken\
  \ from max_logical_replication_workers\n\n\n#------------------------------------------------------------------------------\n\
  # QUERY TUNING\n#------------------------------------------------------------------------------\n\
  \n# - Planner Method Configuration -\n\n#enable_async_append = on\n#enable_bitmapscan\
  \ = on\n#enable_gathermerge = on\n#enable_hashagg = on\n#enable_hashjoin = on\n\
  #enable_incremental_sort = on\n#enable_indexscan = on\n#enable_indexonlyscan = on\n\
  #enable_material = on\n#enable_memoize = on\n#enable_mergejoin = on\n#enable_nestloop\
  \ = on\n#enable_parallel_append = on\n#enable_parallel_hash = on\n#enable_partition_pruning\
  \ = on\n#enable_partitionwise_join = off\n#enable_partitionwise_aggregate = off\n\
  #enable_seqscan = on\n#enable_sort = on\n#enable_tidscan = on\n\n# - Planner Cost\
  \ Constants -\n\n#seq_page_cost = 1.0                    # measured on an arbitrary\
  \ scale\n#random_page_cost = 4.0                 # same scale as above\n#cpu_tuple_cost\
  \ = 0.01                  # same scale as above\n#cpu_index_tuple_cost = 0.005 \
  \          # same scale as above\n#cpu_operator_cost = 0.0025             # same\
  \ scale as above\n#parallel_setup_cost = 1000.0   # same scale as above\n#parallel_tuple_cost\
  \ = 0.1              # same scale as above\n#min_parallel_table_scan_size = 8MB\n\
  #min_parallel_index_scan_size = 512kB\n#effective_cache_size = 4GB\n\n#jit_above_cost\
  \ = 100000                # perform JIT compilation if available\n             \
  \                           # and query more expensive than this;\n            \
  \                            # -1 disables\n#jit_inline_above_cost = 500000    \
  \     # inline small functions if query is\n                                   \
  \     # more expensive than this; -1 disables\n#jit_optimize_above_cost = 500000\
  \       # use expensive JIT optimizations if\n                                 \
  \       # query is more expensive than this;\n                                 \
  \       # -1 disables\n\n# - Genetic Query Optimizer -\n\n#geqo = on\n#geqo_threshold\
  \ = 12\n#geqo_effort = 5                        # range 1-10\n#geqo_pool_size =\
  \ 0                     # selects default based on effort\n#geqo_generations = 0\
  \                   # selects default based on effort\n#geqo_selection_bias = 2.0\
  \              # range 1.5-2.0\n#geqo_seed = 0.0                        # range\
  \ 0.0-1.0\n\n# - Other Planner Options -\n\n#default_statistics_target = 100   \
  \     # range 1-10000\n#constraint_exclusion = partition       # on, off, or partition\n\
  #cursor_tuple_fraction = 0.1            # range 0.0-1.0\n#from_collapse_limit =\
  \ 8\n#jit = on                               # allow JIT compilation\n#join_collapse_limit\
  \ = 8                # 1 disables collapsing of explicit\n                     \
  \                   # JOIN clauses\n#plan_cache_mode = auto                 # auto,\
  \ force_generic_plan or\n                                        # force_custom_plan\n\
  \n\n#------------------------------------------------------------------------------\n\
  # REPORTING AND LOGGING\n#------------------------------------------------------------------------------\n\
  \n# - Where to Log -\n\n#log_destination = 'stderr'             # Valid values are\
  \ combinations of\n                                        # stderr, csvlog, syslog,\
  \ and eventlog,\n                                        # depending on platform.\
  \  csvlog\n                                        # requires logging_collector\
  \ to be on.\n\n# This is used when logging to stderr:\n#logging_collector = off\
  \                # Enable capturing of stderr and csvlog\n                     \
  \                   # into log files. Required to be on for\n                  \
  \                      # csvlogs.\n                                        # (change\
  \ requires restart)\n\n# These are only used if logging_collector is on:\n#log_directory\
  \ = 'log'                  # directory where log files are written,\n          \
  \                              # can be absolute or relative to PGDATA\n#log_filename\
  \ = 'postgresql-%Y-%m-%d_%H%M%S.log'        # log file name pattern,\n         \
  \                               # can include strftime() escapes\n#log_file_mode\
  \ = 0600                   # creation mode for log files,\n                    \
  \                    # begin with 0 to use octal notation\n#log_rotation_age = 1d\
  \                  # Automatic rotation of logfiles will\n                     \
  \                   # happen after that time.  0 disables.\n#log_rotation_size =\
  \ 10MB               # Automatic rotation of logfiles will\n                   \
  \                     # happen after that much log output.\n                   \
  \                     # 0 disables.\n#log_truncate_on_rotation = off         # If\
  \ on, an existing log file with the\n                                        # same\
  \ name as the new log file will be\n                                        # truncated\
  \ rather than appended to.\n                                        # But such truncation\
  \ only occurs on\n                                        # time-driven rotation,\
  \ not on restarts\n                                        # or size-driven rotation.\
  \  Default is\n                                        # off, meaning append to\
  \ existing files\n                                        # in all cases.\n\n# These\
  \ are relevant when logging to syslog:\n#syslog_facility = 'LOCAL0'\n#syslog_ident\
  \ = 'postgres'\n#syslog_sequence_numbers = on\n#syslog_split_messages = on\n\n#\
  \ This is only relevant when logging to eventlog (Windows):\n# (change requires\
  \ restart)\n#event_source = 'PostgreSQL'\n\n# - When to Log -\n\n#log_min_messages\
  \ = warning             # values in order of decreasing detail:\n              \
  \                          #   debug5\n                                        #\
  \   debug4\n                                        #   debug3\n               \
  \                         #   debug2\n                                        #\
  \   debug1\n                                        #   info\n                 \
  \                       #   notice\n                                        #  \
  \ warning\n                                        #   error\n                 \
  \                       #   log\n                                        #   fatal\n\
  \                                        #   panic\n\n#log_min_error_statement =\
  \ error        # values in order of decreasing detail:\n                       \
  \                 #   debug5\n                                        #   debug4\n\
  \                                        #   debug3\n                          \
  \              #   debug2\n                                        #   debug1\n\
  \                                        #   info\n                            \
  \            #   notice\n                                        #   warning\n \
  \                                       #   error\n                            \
  \            #   log\n                                        #   fatal\n      \
  \                                  #   panic (effectively off)\n\n#log_min_duration_statement\
  \ = -1        # -1 is disabled, 0 logs all statements\n                        \
  \                # and their durations, > 0 logs only\n                        \
  \                # statements running at least this number\n                   \
  \                     # of milliseconds\n\n#log_min_duration_sample = -1       \
  \    # -1 is disabled, 0 logs a sample of statements\n                         \
  \               # and their durations, > 0 logs only a sample of\n             \
  \                           # statements running at least this number\n        \
  \                                # of milliseconds;\n                          \
  \              # sample fraction is determined by log_statement_sample_rate\n\n\
  #log_statement_sample_rate = 1.0        # fraction of logged statements exceeding\n\
  \                                        # log_min_duration_sample to be logged;\n\
  \                                        # 1.0 logs all such statements, 0.0 never\
  \ logs\n\n\n#log_transaction_sample_rate = 0.0      # fraction of transactions whose\
  \ statements\n                                        # are logged regardless of\
  \ their duration; 1.0 logs all\n                                        # statements\
  \ from all transactions, 0.0 never logs\n\n# - What to Log -\n\n#debug_print_parse\
  \ = off\n#debug_print_rewritten = off\n#debug_print_plan = off\n#debug_pretty_print\
  \ = on\n#log_autovacuum_min_duration = -1       # log autovacuum activity;\n   \
  \                                     # -1 disables, 0 logs all actions and\n  \
  \                                      # their durations, > 0 logs only\n      \
  \                                  # actions running at least this number\n    \
  \                                    # of milliseconds.\n#log_checkpoints = off\n\
  #log_connections = off\n#log_disconnections = off\n#log_duration = off\n#log_error_verbosity\
  \ = default          # terse, default, or verbose messages\n#log_hostname = off\n\
  log_line_prefix = '%m [%p] %q%u@%d '            # special values:\n            \
  \                            #   %a = application name\n                       \
  \                 #   %u = user name\n                                        #\
  \   %d = database name\n                                        #   %r = remote\
  \ host and port\n                                        #   %h = remote host\n\
  \                                        #   %b = backend type\n               \
  \                         #   %p = process ID\n                                \
  \        #   %P = process ID of parallel group leader\n                        \
  \                #   %t = timestamp without milliseconds\n                     \
  \                   #   %m = timestamp with milliseconds\n                     \
  \                   #   %n = timestamp with milliseconds (as a Unix epoch)\n   \
  \                                     #   %Q = query ID (0 if none or not computed)\n\
  \                                        #   %i = command tag\n                \
  \                        #   %e = SQL state\n                                  \
  \      #   %c = session ID\n                                        #   %l = session\
  \ line number\n                                        #   %s = session start timestamp\n\
  \                                        #   %v = virtual transaction ID\n     \
  \                                   #   %x = transaction ID (0 if none)\n      \
  \                                  #   %q = stop here in non-session\n         \
  \                               #        processes\n                           \
  \             #   %% = '%'\n                                        # e.g. '<%u%%%d>\
  \ '\n#log_lock_waits = off                   # log lock waits >= deadlock_timeout\n\
  #log_recovery_conflict_waits = off      # log standby recovery conflict waits\n\
  \                                        # >= deadlock_timeout\n#log_parameter_max_length\
  \ = -1          # when logging statements, limit logged\n                      \
  \                  # bind-parameter values to N bytes;\n                       \
  \                 # -1 means print in full, 0 disables\n#log_parameter_max_length_on_error\
  \ = 0  # when logging an error, limit logged\n                                 \
  \       # bind-parameter values to N bytes;\n                                  \
  \      # -1 means print in full, 0 disables\n#log_statement = 'none'           \
  \      # none, ddl, mod, all\n#log_replication_commands = off\n#log_temp_files =\
  \ -1                    # log temporary files equal or larger\n                \
  \                        # than the specified size in kilobytes;\n             \
  \                           # -1 disables, 0 logs all temp files\nlog_timezone =\
  \ 'Etc/UTC'\n\n\n#------------------------------------------------------------------------------\n\
  # PROCESS TITLE\n#------------------------------------------------------------------------------\n\
  \ncluster_name = '14/main'                        # added to process titles if nonempty\n\
  \                                        # (change requires restart)\n#update_process_title\
  \ = on\n\n\n#------------------------------------------------------------------------------\n\
  # STATISTICS\n#------------------------------------------------------------------------------\n\
  \n# - Query and Index Statistics Collector -\n\n#track_activities = on\n#track_activity_query_size\
  \ = 1024       # (change requires restart)\n#track_counts = on\n#track_io_timing\
  \ = off\n#track_wal_io_timing = off\n#track_functions = none                 # none,\
  \ pl, all\nstats_temp_directory = '/var/run/postgresql/14-main.pg_stat_tmp'\n\n\n\
  # - Monitoring -\n\n#compute_query_id = auto\n#log_statement_stats = off\n#log_parser_stats\
  \ = off\n#log_planner_stats = off\n#log_executor_stats = off\n\n\n#------------------------------------------------------------------------------\n\
  # AUTOVACUUM\n#------------------------------------------------------------------------------\n\
  \n#autovacuum = on                        # Enable autovacuum subprocess?  'on'\n\
  \                                        # requires track_counts to also be on.\n\
  #autovacuum_max_workers = 3             # max number of autovacuum subprocesses\n\
  \                                        # (change requires restart)\n#autovacuum_naptime\
  \ = 1min              # time between autovacuum runs\n#autovacuum_vacuum_threshold\
  \ = 50       # min number of row updates before\n                              \
  \          # vacuum\n#autovacuum_vacuum_insert_threshold = 1000      # min number\
  \ of row inserts\n                                        # before vacuum; -1 disables\
  \ insert\n                                        # vacuums\n#autovacuum_analyze_threshold\
  \ = 50      # min number of row updates before\n                               \
  \         # analyze\n#autovacuum_vacuum_scale_factor = 0.2   # fraction of table\
  \ size before vacuum\n#autovacuum_vacuum_insert_scale_factor = 0.2    # fraction\
  \ of inserts over table\n                                        # size before insert\
  \ vacuum\n#autovacuum_analyze_scale_factor = 0.1  # fraction of table size before\
  \ analyze\n#autovacuum_freeze_max_age = 200000000  # maximum XID age before forced\
  \ vacuum\n                                        # (change requires restart)\n\
  #autovacuum_multixact_freeze_max_age = 400000000        # maximum multixact age\n\
  \                                        # before forced vacuum\n              \
  \                          # (change requires restart)\n#autovacuum_vacuum_cost_delay\
  \ = 2ms     # default vacuum cost delay for\n                                  \
  \      # autovacuum, in milliseconds;\n                                        #\
  \ -1 means use vacuum_cost_delay\n#autovacuum_vacuum_cost_limit = -1      # default\
  \ vacuum cost limit for\n                                        # autovacuum, -1\
  \ means use\n                                        # vacuum_cost_limit\n\n\n#------------------------------------------------------------------------------\n\
  # CLIENT CONNECTION DEFAULTS\n#------------------------------------------------------------------------------\n\
  \n# - Statement Behavior -\n\n#client_min_messages = notice           # values in\
  \ order of decreasing detail:\n                                        #   debug5\n\
  \                                        #   debug4\n                          \
  \              #   debug3\n                                        #   debug2\n\
  \                                        #   debug1\n                          \
  \              #   log\n                                        #   notice\n   \
  \                                     #   warning\n                            \
  \            #   error\n#search_path = '\"$user\", public'        # schema names\n\
  #row_security = on\n#default_table_access_method = 'heap'\n#default_tablespace =\
  \ ''                # a tablespace name, '' uses the default\n#default_toast_compression\
  \ = 'pglz'     # 'pglz' or 'lz4'\n#temp_tablespaces = ''                  # a list\
  \ of tablespace names, '' uses\n                                        # only default\
  \ tablespace\n#check_function_bodies = on\n#default_transaction_isolation = 'read\
  \ committed'\n#default_transaction_read_only = off\n#default_transaction_deferrable\
  \ = off\n#session_replication_role = 'origin'\n#statement_timeout = 0          \
  \        # in milliseconds, 0 is disabled\n#lock_timeout = 0                   \
  \    # in milliseconds, 0 is disabled\n#idle_in_transaction_session_timeout = 0\
  \        # in milliseconds, 0 is disabled\n#idle_session_timeout = 0           \
  \    # in milliseconds, 0 is disabled\n#vacuum_freeze_table_age = 150000000\n#vacuum_freeze_min_age\
  \ = 50000000\n#vacuum_failsafe_age = 1600000000\n#vacuum_multixact_freeze_table_age\
  \ = 150000000\n#vacuum_multixact_freeze_min_age = 5000000\n#vacuum_multixact_failsafe_age\
  \ = 1600000000\n#bytea_output = 'hex'                   # hex, escape\n#xmlbinary\
  \ = 'base64'\n#xmloption = 'content'\n#gin_pending_list_limit = 4MB\n\n# - Locale\
  \ and Formatting -\n\ndatestyle = 'iso, mdy'\n#intervalstyle = 'postgres'\ntimezone\
  \ = 'Etc/UTC'\n#timezone_abbreviations = 'Default'     # Select the set of available\
  \ time zone\n                                        # abbreviations.  Currently,\
  \ there are\n                                        #   Default\n             \
  \                           #   Australia (historical usage)\n                 \
  \                       #   India\n                                        # You\
  \ can create your own file in\n                                        # share/timezonesets/.\n\
  #extra_float_digits = 1                 # min -15, max 3; any value >0 actually\n\
  \                                        # selects precise output mode\n#client_encoding\
  \ = sql_ascii            # actually, defaults to database\n                    \
  \                    # encoding\n\n# These settings are initialized by initdb, but\
  \ they can be changed.\nlc_messages = 'C.UTF-8'                 # locale for system\
  \ error message\n                                        # strings\nlc_monetary\
  \ = 'C.UTF-8'                 # locale for monetary formatting\nlc_numeric = 'C.UTF-8'\
  \                  # locale for number formatting\nlc_time = 'C.UTF-8'         \
  \                    # locale for time formatting\n\n# default configuration for\
  \ text search\ndefault_text_search_config = 'pg_catalog.english'\n\n# - Shared Library\
  \ Preloading -\n\n#local_preload_libraries = ''\n#session_preload_libraries = ''\n\
  #shared_preload_libraries = ''  # (change requires restart)\n#jit_provider = 'llvmjit'\
  \               # JIT library to use\n\n# - Other Defaults -\n\n#dynamic_library_path\
  \ = '$libdir'\n#extension_destdir = ''                 # prepend path when loading\
  \ extensions\n                                        # and shared objects (added\
  \ by Debian)\n#gin_fuzzy_search_limit = 0\n\n\n#------------------------------------------------------------------------------\n\
  # LOCK MANAGEMENT\n#------------------------------------------------------------------------------\n\
  \n#deadlock_timeout = 1s\n#max_locks_per_transaction = 64         # min 10\n   \
  \                                     # (change requires restart)\n#max_pred_locks_per_transaction\
  \ = 64    # min 10\n                                        # (change requires restart)\n\
  #max_pred_locks_per_relation = -2       # negative values mean\n               \
  \                         # (max_pred_locks_per_transaction\n                  \
  \                      #  / -max_pred_locks_per_relation) - 1\n#max_pred_locks_per_page\
  \ = 2            # min 0\n\n\n#------------------------------------------------------------------------------\n\
  # VERSION AND PLATFORM COMPATIBILITY\n#------------------------------------------------------------------------------\n\
  \n# - Previous PostgreSQL Versions -\n\n#array_nulls = on\n#backslash_quote = safe_encoding\
  \        # on, off, or safe_encoding\n#escape_string_warning = on\n#lo_compat_privileges\
  \ = off\n#quote_all_identifiers = off\n#standard_conforming_strings = on\n#synchronize_seqscans\
  \ = on\n\n# - Other Platforms and Clients -\n\n#transform_null_equals = off\n\n\n\
  #------------------------------------------------------------------------------\n\
  # ERROR HANDLING\n#------------------------------------------------------------------------------\n\
  \n#exit_on_error = off                    # terminate session on any error?\n#restart_after_crash\
  \ = on               # reinitialize after backend crash?\n#data_sync_retry = off\
  \                  # retry or panic on failure to fsync\n                      \
  \                  # data?\n                                        # (change requires\
  \ restart)\n#recovery_init_sync_method = fsync      # fsync, syncfs (Linux 5.8+)\n\
  \n\n#------------------------------------------------------------------------------\n\
  # CONFIG FILE INCLUDES\n#------------------------------------------------------------------------------\n\
  \n# These options allow settings to be loaded from files other than the\n# default\
  \ postgresql.conf.  Note that these are directives, not variable\n# assignments,\
  \ so they can usefully be given more than once.\n\ninclude_dir = 'conf.d'      \
  \            # include files ending in '.conf' from\n                          \
  \              # a directory, e.g., 'conf.d'\n#include_if_exists = '...'       \
  \       # include file only if it exists\n#include = '...'                     \
  \   # include file\n\n\n#------------------------------------------------------------------------------\n\
  # CUSTOMIZED OPTIONS\n#------------------------------------------------------------------------------\n\
  \n# Add settings for extensions here\n"


# ======================
# kitsu_enable_job_queue
# ----------------------
#
# Type: <class 'bool'>
# Description:
#     Enable Kitsu Job Queue?
# Required:
#     False
# Examples:
#     None
kitsu_enable_job_queue: true


# ====================
# kitsu_port_container
# --------------------
#
# Type: <class 'int'>
# Description:
#     The Kitsu container port.
# Required:
#     False
# Examples:
#     None
kitsu_port_container: 80


# ===============
# kitsu_port_host
# ---------------
#
# Type: <class 'int'>
# Description:
#     The Kitsu host port.
# Required:
#     False
# Examples:
#     None
kitsu_port_host: 4545


# =========================
# kitsu_db_inside_container
# -------------------------
#
# Type: <class 'bool'>
# Description:
#     The Kitsu database inside container; the database will not be persistent. Helpful for testing.
# Required:
#     False
# Examples:
#     None
kitsu_db_inside_container: false


# ==================================
# kitsu_database_install_destination
# ----------------------------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     The host side Kitsu database installation destination.
# Required:
#     False
# Examples:
#     None
kitsu_database_install_destination: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/data/postgresql'


# ====================
# kitsu_preview_folder
# --------------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     The Kitsu Preview folder (/opt/zou/previews).
# Required:
#     False
# Examples:
#     None
kitsu_preview_folder: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/data/previews'


# =============
# kitsu_tmp_dir
# -------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     Kitsu TMP directory (/opt/zou/tmp).
# Required:
#     False
# Examples:
#     None
kitsu_tmp_dir: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/data/tmp'


# ================
# kitsu_secret_key
# ----------------
#
# Type: <class 'str'>
# Description:
#     Kitsu Secret Key.
# Required:
#     False
# Examples:
#     None
kitsu_secret_key: yourrandomsecretkey


# ============
# pip_packages
# ------------
#
# Type: typing.List[str]
# Description:
#     `boto3` is required if `kitsu_enable_job_queue` is `true`. [Reference](https://zou.cg-wire.com/jobs/)
# Required:
#     False
# Examples:
#     None
pip_packages:
- boto3
```


</details>


***

# External Resources

- [https://kitsu.cg-wire.com](https://kitsu.cg-wire.com)

[![Logo Kitsu ](https://zou.cg-wire.com/kitsu.png)](https://github.com/cgwire/zou)

Kitsu is written and maintained by CGWire, a company based in France:

[![Logo CGWire ](https://www.cg-wire.com/_nuxt/logo.4d5a2d7e.png)](https://www.cg-wire.com)

Kitsu itself consists of two modules:

1. [Gazu - Kitsu Python Client](https://gazu.cg-wire.com)
2. [Zou - Kitsu Python API](https://zou.cg-wire.com)

`OpenStudioLandscapes-Kitsu` is based on the Kitsu provided Docker image:

- [https://kitsu.cg-wire.com/installation/#using-docker-image](https://kitsu.cg-wire.com/installation/#using-docker-image)
- [https://hub.docker.com/r/cgwire/cgwire](https://hub.docker.com/r/cgwire/cgwire)

The default credentials are:

- User: `admin@example.com`
- Password: `mysecretpassword`

## Inofficial Resources

An interesting Docker Compose project for Kitsu worth following can be found below. OpenStudioLandscapes-Kitsu, however, is not based on this project but may one day leverage it:

1. [Mathieu BOUZARD/docker-cgwire](https://gitlab.com/mathbou/docker-cgwire)

***

# Community

| Feature                                   | GitHub                                                                                                                                                 | Discord                                                                      |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| OpenStudioLandscapes                      | [https://github.com/michimussato/OpenStudioLandscapes](https://github.com/michimussato/OpenStudioLandscapes)                                           | [# openstudiolandscapes-general](https://discord.gg/F6bDRWsHac)              |
| OpenStudioLandscapes-Ayon                 | [https://github.com/michimussato/OpenStudioLandscapes-Ayon](https://github.com/michimussato/OpenStudioLandscapes-Ayon)                                 | [# openstudiolandscapes-ayon](https://discord.gg/gd6etWAF3v)                 |
| OpenStudioLandscapes-Dagster              | [https://github.com/michimussato/OpenStudioLandscapes-Dagster](https://github.com/michimussato/OpenStudioLandscapes-Dagster)                           | [# openstudiolandscapes-dagster](https://discord.gg/jwB3DwmKvs)              |
| OpenStudioLandscapes-Deadline-10-2        | [https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2)               | [# openstudiolandscapes-deadline-10-2](https://discord.gg/p2UjxHk4Y3)        |
| OpenStudioLandscapes-Deadline-10-2-Worker | [https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2-Worker](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2-Worker) | [# openstudiolandscapes-deadline-10-2-worker](https://discord.gg/ttkbfkzUmf) |
| OpenStudioLandscapes-Flamenco             | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco](https://github.com/michimussato/OpenStudioLandscapes-Flamenco)                         | [# openstudiolandscapes-flamenco](https://discord.gg/EPrX5fzBCf)             |
| OpenStudioLandscapes-Flamenco-Worker      | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker](https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker)           | [# openstudiolandscapes-flamenco-worker](https://discord.gg/Sa2zFqSc4p)      |
| OpenStudioLandscapes-Grafana              | [https://github.com/michimussato/OpenStudioLandscapes-Grafana](https://github.com/michimussato/OpenStudioLandscapes-Grafana)                           | [# openstudiolandscapes-grafana](https://discord.gg/gEDQ8vJWDb)              |
| OpenStudioLandscapes-Kitsu                | [https://github.com/michimussato/OpenStudioLandscapes-Kitsu](https://github.com/michimussato/OpenStudioLandscapes-Kitsu)                               | [# openstudiolandscapes-kitsu](https://discord.gg/6cc6mkReJ7)                |
| OpenStudioLandscapes-LikeC4               | [https://github.com/michimussato/OpenStudioLandscapes-LikeC4](https://github.com/michimussato/OpenStudioLandscapes-LikeC4)                             | [# openstudiolandscapes-likec4](https://discord.gg/qAYYsKYF6V)               |
| OpenStudioLandscapes-OpenCue              | [https://github.com/michimussato/OpenStudioLandscapes-OpenCue](https://github.com/michimussato/OpenStudioLandscapes-OpenCue)                           | [# openstudiolandscapes-opencue](https://discord.gg/3DdCZKkVyZ)              |
| OpenStudioLandscapes-OpenCue-Worker       | [https://github.com/michimussato/OpenStudioLandscapes-OpenCue-Worker](https://github.com/michimussato/OpenStudioLandscapes-OpenCue-Worker)             | [# openstudiolandscapes-opencue-worker](https://discord.gg/n9fxxhHa3V)       |
| OpenStudioLandscapes-RustDeskServer       | [https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer](https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer)             | [# openstudiolandscapes-rustdeskserver](https://discord.gg/nJ8Ffd2xY3)       |
| OpenStudioLandscapes-Syncthing            | [https://github.com/michimussato/OpenStudioLandscapes-Syncthing](https://github.com/michimussato/OpenStudioLandscapes-Syncthing)                       | [# openstudiolandscapes-syncthing](https://discord.gg/upb9MCqb3X)            |
| OpenStudioLandscapes-Template             | [https://github.com/michimussato/OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template)                         | [# openstudiolandscapes-template](https://discord.gg/J59GYp3Wpy)             |
| OpenStudioLandscapes-VERT                 | [https://github.com/michimussato/OpenStudioLandscapes-VERT](https://github.com/michimussato/OpenStudioLandscapes-VERT)                                 | [# openstudiolandscapes-vert](https://discord.gg/EPrX5fzBCf)                 |
| OpenStudioLandscapes-filebrowser          | [https://github.com/michimussato/OpenStudioLandscapes-filebrowser](https://github.com/michimussato/OpenStudioLandscapes-filebrowser)                   | [# openstudiolandscapes-filebrowser](https://discord.gg/stzNsZBmwk)          |
| OpenStudioLandscapes-n8n                  | [https://github.com/michimussato/OpenStudioLandscapes-n8n](https://github.com/michimussato/OpenStudioLandscapes-n8n)                                   | [# openstudiolandscapes-n8n](https://discord.gg/yFYrG999wE)                  |

To follow up on the previous LinkedIn publications, visit:

- [OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/company/106731439/).
- [Search for tag #OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/search/results/all/?keywords=%23openstudiolandscapes).

***

Last changed: **2026-04-03 02:45:13 UTC**