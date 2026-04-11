<!-- TOC -->
* [OpenStudioLandscapes-Kitsu](#openstudiolandscapes-kitsu)
<!-- TOC -->

---

# OpenStudioLandscapes-Kitsu

This is for isolated development, unit testing and debugging.
Instead of the [`definitions.py`](src/OpenStudioLandscapes/Kitsu/definitions.py), 
the accompanying [`workspace.yaml`](workspace.yaml) loads 
the [`_definitions_with_upstream_specs.py`](src/OpenStudioLandscapes/Kitsu/_definitions_with_upstream_specs.py) 
which also contains 
[`AssetSpec`](https://release-1-9-13.archive.dagster-docs.io/api/dagster/assets#dagster.AssetSpec)
definitions for upstream dependencies as 
[external assets](https://release-1-9-13.archive.dagster-docs.io/guides/build/assets/external-assets).

```shell
dagster dev --workspace workspace.yaml
```

```
dagster._core.errors.DagsterImportError: Encountered ImportError: `No module named 'OpenStudioLandscapes.engine.common_assets.cmd'` while importing module OpenStudioLandscapes.Kitsu._definitions_with_upstream_specs. Local modules were resolved using the working directory `/home/michael/git/repos/OpenStudioLandscapes/.features/OpenStudioLandscapes-Kitsu`. If another working directory should be used, please explicitly specify the appropriate path using the `-d` or `--working-directory` for CLI based targets or the `working_directory` configuration option for workspace targets. 

  File "/home/michael/git/repos/OpenStudioLandscapes/.features/OpenStudioLandscapes-Kitsu/.venv/lib/python3.11/site-packages/dagster/_grpc/server.py", line 417, in __init__
    self._loaded_repositories: Optional[LoadedRepositories] = LoadedRepositories(
                                                              ^^^^^^^^^^^^^^^^^^^
  File "/home/michael/git/repos/OpenStudioLandscapes/.features/OpenStudioLandscapes-Kitsu/.venv/lib/python3.11/site-packages/dagster/_grpc/server.py", line 250, in __init__
    loadable_targets = get_loadable_targets(
                       ^^^^^^^^^^^^^^^^^^^^^
  File "/home/michael/git/repos/OpenStudioLandscapes/.features/OpenStudioLandscapes-Kitsu/.venv/lib/python3.11/site-packages/dagster/_grpc/utils.py", line 51, in get_loadable_targets
    else loadable_targets_from_python_module(module_name, working_directory)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/michael/git/repos/OpenStudioLandscapes/.features/OpenStudioLandscapes-Kitsu/.venv/lib/python3.11/site-packages/dagster/_core/workspace/autodiscovery.py", line 33, in loadable_targets_from_python_module
    module = load_python_module(
             ^^^^^^^^^^^^^^^^^^^
  File "/home/michael/git/repos/OpenStudioLandscapes/.features/OpenStudioLandscapes-Kitsu/.venv/lib/python3.11/site-packages/dagster/_core/code_pointer.py", line 140, in load_python_module
    raise DagsterImportError(

The above exception was caused by the following exception:
ModuleNotFoundError: No module named 'OpenStudioLandscapes.engine.common_assets.cmd'

  File "/home/michael/git/repos/OpenStudioLandscapes/.features/OpenStudioLandscapes-Kitsu/.venv/lib/python3.11/site-packages/dagster/_core/code_pointer.py", line 135, in load_python_module
    return importlib.import_module(module_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/michael/git/repos/OpenStudioLandscapes/.features/OpenStudioLandscapes-Kitsu/src/OpenStudioLandscapes/Kitsu/_definitions_with_upstream_specs.py", line 3, in <module>
    from OpenStudioLandscapes.Kitsu.definitions import assets_base
  File "/home/michael/git/repos/OpenStudioLandscapes/.features/OpenStudioLandscapes-Kitsu/src/OpenStudioLandscapes/Kitsu/definitions.py", line 6, in <module>
    import OpenStudioLandscapes.Kitsu.assets
  File "/home/michael/git/repos/OpenStudioLandscapes/.features/OpenStudioLandscapes-Kitsu/src/OpenStudioLandscapes/Kitsu/assets.py", line 20, in <module>
    from OpenStudioLandscapes.engine.common_assets.cmd import get_feature__cmd
```