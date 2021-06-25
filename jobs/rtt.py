from os import name as PLATFORM_NAME, environ, getenv, mkdir, makedirs
from os.path import join, isdir, abspath, isfile, dirname
from .scons import scons
from shutil import copytree

from helpers import request_config, update_config, ENV_ROOT, print, PROJECT_ROOT, exec_pass, do_exit, die, try_get_env

help_title = "下载和管理RT-Thread源码"
RTT_GIT_GITHUB = 'https://github.com/RT-Thread/rt-thread.git'
RTT_GIT_GITEE = 'https://gitee.com/rtthread/rt-thread.git'


def do_update(rtt_root):
    if isdir(join(rtt_root, '.git')):
        die("rtthread未受git管理（或受父项目控制），不支持自动更新")

    exec_pass("git", ['reset', '--force'], cwd=rtt_root)
    exec_pass("git", ['clean', '-ffdx'], cwd=rtt_root)
    exec_pass("git", ['pull'], cwd=rtt_root)
    exec_pass("git", ['branch'])


def do_clone(rtt_root, remote):
    print(f"clone {remote} to {rtt_root}")
    pp = dirname(abspath(rtt_root))
    if not isdir(pp):
        print("create directory: " + pp)
        makedirs(pp, exist_ok=True)
    exec_pass("git", ['clone', '--depth', '3', '--recurse-submodules', '--shallow-submodules', remote, rtt_root])
    exec_pass("git", ['branch'])


def do_export(rtt_root, target):
    print(f"copy {rtt_root} to {target}")
    print("正在复制文件，请等待……")

    bsp = join(rtt_root, 'bsp')

    def get_ignore(src, names):
        if src == bsp:
            names.remove('w60x')
            return names

        print(src)
        ig = ['__pycache__']
        if src == rtt_root:
            ig.append('examples')
            ig.append('documentation')
        for ele in names:
            if ele[0] == '.':
                ig.append(ele)
        return ig

    copytree(rtt_root, target, ignore=get_ignore, symlinks=True, ignore_dangling_symlinks=True, dirs_exist_ok=True)
    print("\nDone.")


def usage():
    print("Usage: control.py rtt <command>")
    print("  update: clone or update rt-thread source code")
    print("  fork: copy rt-thread source code into current project")
    print("")
    print("Node: default clone from gitee.com, pass '--github' to use github.com")
    do_exit(1)


def rtt_root_fallback():
    rtt_root = try_get_env('RTT_ROOT')
    if rtt_root is None:
        rtt_root = join(ENV_ROOT, 'rt-thread-src')
    return rtt_root


def main(argv):
    if len(argv) < 1:
        return usage()

    if 'CI' in environ:
        rtt_root = join(PROJECT_ROOT, "rt-thread")
    else:
        rtt_root = request_config("RTT_ROOT")
        if rtt_root is None:
            rtt_root = rtt_root_fallback()

    source = RTT_GIT_GITHUB if '--github' in argv else RTT_GIT_GITEE

    if argv[0] == 'update':
        if isfile(join(rtt_root, 'Kconfig')):
            do_update(rtt_root)
        else:
            do_clone(rtt_root, source)
    elif argv[0] == 'fork':
        clone_to = join(PROJECT_ROOT, "rt-thread")
        if (rtt_root == clone_to):
            rtt_root = rtt_root_fallback()

        if isfile(join(PROJECT_ROOT, 'rt-thread/Kconfig')):
            die("rt-thread already copied to project")

        if not isdir(join(rtt_root, '.git')):
            do_clone(rtt_root, source)

        do_export(rtt_root, clone_to)
        rtt_root = '${workspaceFolder}/rt-thread'
        update_config('RTT_ROOT', rtt_root)
    else:
        return usage()
