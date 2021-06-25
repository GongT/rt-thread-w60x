from os import environ
from os.path import join

from .vscode_config import request_config
from .env import save_env, try_get_env
from .output import die
from .pathvars import ENV_ROOT


def set_env_if_not(env, config=None, global_store=False, required=True, default=None):
    if env in environ:
        if global_store:
            save_env(env, environ[env])
        return environ[env]
    if config is None:
        config = env
    value = request_config(config)
    if value is not None:
        value = str(value)
    if global_store:
        if value is None:
            value = try_get_env(env)
        else:
            save_env(env, value)

    if value is None:
        if required:
            die(f"invalid config: {config} = {value}")
        elif default is not None:
            value = default

    if value is not None:
        environ[env] = str(value)
    return value


def ensure_rtt_root():
    return set_env_if_not('RTT_ROOT', global_store=True, default=join(ENV_ROOT, 'rt-thread-src'))
