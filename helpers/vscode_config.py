from json5 import load
from os.path import join, isfile
from os import environ
from .pathvars import PROJECT_ROOT
from .output import debug, die

loaded = None


def request_config(name):
    global loaded
    if loaded is None:
        configfile = join(PROJECT_ROOT, '.vscode/settings.json')
        if isfile(configfile):
            with open(configfile, 'rt') as f:
                loaded = load(f)
            # print(loaded)
        else:
            debug("missing vscode config file:", configfile)
            loaded = False
    if loaded == False:
        return None

    if name in loaded:
        return loaded[name]
    else:
        return None


def require_argument(env, cfg_name, arg=None):
    if env in environ:
        return environ[env]
    cfg = request_config(cfg_name)
    if cfg is None:
        arg_msg = f' argument {arg} or ' if arg is not None else ' '
        die(f"missing{arg_msg}config '{cfg_name}'' (or environment variable '{env}')")
    return cfg
