from os import environ, chdir, name as PLATFORM_NAME, remove
from os.path import join, isfile, isdir, getmtime
from shutil import copy2

from helpers import md5_file, exec_pass, request_config, die, SELF_ROOT, PROJECT_ROOT, print, BINARY_NAME, BIN_FILE, try_get_env, save_env, ENV_ROOT

help_title = "运行scons"

project_config_file = join(PROJECT_ROOT, '.config')
library_config_file = join(SELF_ROOT, '.config')

ARM_GCC_DOWNLOAD_URL = 'https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads'
GCC_COLORS = [
    'error=38;5;1;1', 'warning=38;5;9;1', 'note=38;5;13;1', 'range1=32', 'range2=34', 'locus=48;5;2', 'quote=01', 'path=01;36', 'fixit-insert=32', 'fixit-delete=31', 'diff-filename=01',
    'diff-hunk=32', 'diff-delete=31', 'diff-insert=32', 'type-diff=01;32'
]


def set_env_if_not(env, config=None, global_store=False, required=True):
    if env in environ:
        if global_store:
            save_env(env, environ[env])
        return
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
    else:
        environ[env] = str(value)
    return value


def copy_config():
    if isfile(project_config_file):
        print(f"[WARN] copy to {library_config_file}")
        copy2(src=project_config_file, dst=library_config_file)


def moveback():
    if isfile(project_config_file) and isfile(library_config_file) and getmtime(library_config_file) == getmtime(project_config_file):
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
    if '--verbose' not in argv:
        if '-j' not in argv and len([i for i in argv if i.startswith('--jobs')]) == 0:
            import multiprocessing
            argv.append(f'--jobs={multiprocessing.cpu_count()}')

    environ['GCC_COLORS'] = ':'.join(GCC_COLORS)
    environ['GCC_URLS'] = 'st'
    environ['PROJECT_ROOT'] = PROJECT_ROOT
    environ['BINARY_NAME'] = BINARY_NAME
    set_env_if_not('BUILD_ENV')
    if set_env_if_not('GCC_OPT', required=False) is None:
        environ['GCC_OPT'] = '2'

    if set_env_if_not('RTT_ROOT', global_store=True, required=False) is None:
        rtt_root = join(ENV_ROOT, 'rt-thread-src')
        if isdir(rtt_root):
            environ['RTT_ROOT'] = rtt_root
        else:
            die(f"missing rt-thread source code (it should at {rtt_root}). use './control.py rtt update'.")

    gcc_bin = set_env_if_not('RTT_EXEC_PATH', global_store=True)
    gcc_exec = 'arm-none-eabi-gcc'
    if not isfile(join(gcc_bin, gcc_exec)):
        if isfile(join(gcc_bin, 'bin', gcc_exec)):
            environ['RTT_EXEC_PATH'] = join(gcc_bin, 'bin')
        else:
            die(f"missing arm gcc binary (in {gcc_bin})\n\nplease download one from {ARM_GCC_DOWNLOAD_URL}.")

    rtconfig_file = join(SELF_ROOT, 'rtconfig.h')
    if not isfile(rtconfig_file):
        with open(rtconfig_file, 'wt') as f:
            f.write('#pragma once')

    rtconfig_project_file = join(PROJECT_ROOT, 'rtconfig_project.h')
    if not isfile(rtconfig_project_file):
        with open(rtconfig_project_file, 'wt') as f:
            f.write('#pragma once\n\n// place custom config here')

    is_menuconfig = ('--menuconfig' in argv) or ('--pyconfig' in argv) or ('--pyconfig-silent' in argv)
    if is_menuconfig:
        copy_config()
    elif isfile(project_config_file):
        if md5_file(project_config_file) != get_last_hash():
            print("config changed, updateing rtconfig.h. project will full rebuild.")
            exec_pass('scons', [f'--useconfig={project_config_file}'], cwd=SELF_ROOT)
            write_last_hash(project_config_file)
    else:
        die("you have never run '\x1B[38;5;14m./control.py config\x1B[0m', no way to compile.")

    exec_pass('scons', argv, cwd=SELF_ROOT)

    if is_menuconfig:
        if moveback():
            exec_pass('scons', [f'--useconfig={project_config_file}'], cwd=SELF_ROOT)

    print("\x1B[38;5;10mscons success.\x1B[0m")
    cdb_file = join(SELF_ROOT, '.vscode/compile_commands.json')
    if isfile(cdb_file):
        dst = join(PROJECT_ROOT, '.vscode/compile_commands.json')
        print(f"copy cdb file to {dst}")
        copy2(src=cdb_file, dst=dst)
        remove(cdb_file)
