from json5 import load, dump
from os.path import join, isfile
from os import environ

from .pathvars import PROJECT_ROOT
from .output import debug, die

loaded = None
configfile = join(PROJECT_ROOT, '.vscode/settings.json')


def update_config(name, value):
    global loaded
    curr = request_config(name)
    if (curr == value):
        return

    loaded[name] = value
    with open(configfile, 'wt') as config_file:
        dump(loaded, config_file, quote_keys=True, allow_duplicate_keys=False, ensure_ascii=False, indent='\t')


def request_config(name):
    global loaded
    if loaded is None:
        if isfile(configfile):
            with open(configfile, 'rt') as f:
                loaded = load(f)
            # print(loaded)
        else:
            debug("missing vscode config file:", configfile)
            loaded = False
    if not loaded:
        return None

    if name in loaded:
        value = str(loaded[name])
        if isinstance(value, str):
            value = value.replace('${workspaceFolder}', PROJECT_ROOT)
        return value
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
