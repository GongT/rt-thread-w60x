from helpers import md5_file, exec_pass, request_config, die, SELF_ROOT, PROJECT_ROOT, print, BINARY_NAME, BIN_FILE
from os import environ, chdir, name as PLATFORM_NAME, remove
from os.path import join, isfile, getmtime
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
    if getmtime(library_config_file) == getmtime(project_config_file):
        print('config file did not change')
        return
    print(f"[WARN] copy to {project_config_file}")
    copy2(src=library_config_file, dst=project_config_file)
    # remove(library_config_file)


def scons(argv):
    main(argv)


def get_last_hash():
    try:
        with open(join(SELF_ROOT, '.config.hash'), 'rt') as f:
            return f.read()
    except:
        return ''


def write_last_hash(src):
    h = md5_file(src)
    with open(join(SELF_ROOT, '.config.hash'), 'wt') as f:
        return f.write(h)


def main(argv):
    argv.append(f"--sconstruct={join(SELF_ROOT, 'SConstruct')}")
    argv.append(f"--directory=={PROJECT_ROOT}")
    # argv.append(f"--verbose")

    if '--verbose' not in argv:
        if '-j' not in argv and len([i for i in argv if i.startswith('--jobs')]) == 0:
            import multiprocessing
            argv.append(f'--jobs={multiprocessing.cpu_count()}')

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

    rtconfig_project_file = join(PROJECT_ROOT, 'rtconfig_project.h')
    if not isfile(rtconfig_project_file):
        with open(rtconfig_project_file, 'wt') as f:
            f.write('// place custom config here')

    is_menuconfig = ('--menuconfig' in argv) or ('--pyconfig' in argv)
    if is_menuconfig:
        copy_config()
    elif md5_file(project_config_file) != get_last_hash():
        print("config changed, updateing rtconfig.h. project will full rebuild.")
        exec_pass('scons', [f'--useconfig={project_config_file}'])
        write_last_hash(project_config_file)

    exec_pass('scons', argv)

    if is_menuconfig:
        if moveback():
            exec_pass('scons', [f'--useconfig={project_config_file}'])
