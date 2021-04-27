from helpers import exec_pass, request_config, die, SELF_ROOT, PROJECT_ROOT, print, BINARY_NAME, BIN_FILE
from os import environ, chdir, name as PLATFORM_NAME, remove
from os.path import join, isfile
from shutil import copy2

help_title = "运行scons"

project_config_file = join(PROJECT_ROOT, '.config')
library_config_file = join(SELF_ROOT, '.config')


def set_env_if_not(env, config=None):
    if env in environ:
        return
    if config is None:
        config = env
    v = request_config(config)
    if v is None or type(v) != str:
        die(f"invalid config: {config} = {v}")
    environ[env] = v


def copy_config():
    if isfile(project_config_file):
        print(f"[WARN] copy to {library_config_file}")
        copy2(src=project_config_file, dst=library_config_file)


def moveback():
    print(f"[WARN] copy to {project_config_file}")
    copy2(src=library_config_file, dst=project_config_file)
    remove(library_config_file)


def main(argv):
    argv.append(f"--sconstruct={join(SELF_ROOT, 'SConstruct')}")
    argv.append(f"--directory=={PROJECT_ROOT}")
    # argv.append(f"--verbose")
    chdir(SELF_ROOT)
    environ['PROJECT_ROOT'] = PROJECT_ROOT
    environ['BINARY_NAME'] = BINARY_NAME
    set_env_if_not('RTT_EXEC_PATH')
    set_env_if_not('RTT_ROOT')
    set_env_if_not('BUILD_ENV')

    rtconfig_file = join(SELF_ROOT, 'rtconfig.h')
    if not isfile(rtconfig_file):
        with open(rtconfig_file, 'wt') as f:
            f.write('#pragma once')

    is_menuconfig = ('--menuconfig' in argv) or ('--pyconfig' in argv)
    if is_menuconfig:
        copy_config()

    exec_pass('scons', argv)

    if is_menuconfig:
        moveback()
        exec_pass('scons', [f'--useconfig={project_config_file}'])
