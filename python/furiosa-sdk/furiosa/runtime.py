import importlib

_furiosa_sdk_runtime = importlib.util.find_spec("furiosa_sdk_runtime")

if _furiosa_sdk_runtime is not None:
    from furiosa_sdk_runtime import *
    from furiosa_sdk_runtime import __version__
    from furiosa_sdk_runtime import __full_version__