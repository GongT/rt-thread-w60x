#!/usr/bin/env python3

if __name__ != '__main__':
    raise "This file can not use as a module"

from os.path import dirname, abspath, split, isfile, isdir, join, relpath
from os import getcwd, listdir, mkdir, chmod, chdir
from shutil import copy2, copystat
from pathlib import Path
from json5 import load, dump

from helpers.output import die, debug as print
from helpers.exec import exec_pass, python_pass

SELF_DIR = dirname(abspath(__file__))
INSTALL_TO = getcwd()

if INSTALL_TO == SELF_DIR:
    INSTALL_TO = dirname(INSTALL_TO)

SELF_NAME = split(SELF_DIR)[1]
SELF_DIR_REL = relpath(SELF_DIR, INSTALL_TO)
if SELF_DIR_REL.startswith('..'):
    SELF_DIR_REL = None

ENV_RT_DIR = join(Path.home(), '.env/rt-thread-src')
if not isdir(ENV_RT_DIR):
    ENV_RT_DIR = ''

dircontents = listdir(INSTALL_TO)
dircontents.remove(split(SELF_DIR)[1])
# if len(dircontents) != 0:
#     die("无法在此目录初始化项目，因为有多余的文件：%s...\n当前目录：%s" % (', '.join(dircontents[0:5]), INSTALL_TO))

print("初始化项目……( %s )" % INSTALL_TO)

if not isdir(join(INSTALL_TO, '.git')) and not isfile(join(INSTALL_TO, '.git')):
    exec_pass('git', ['init', '.'], cwd=INSTALL_TO)
    exec_pass('git', ['submodule', 'add', 'https://github.com/GongT/rt-thread-w60x.git'], cwd=INSTALL_TO)
    chdir(INSTALL_TO)
    python_pass([join(INSTALL_TO, 'rt-thread-w60x/install.py')])
    exit(0)


def place_file(name, data=None, copy=None, overwrite=False):
    p = join(INSTALL_TO, name)
    if not overwrite and isfile(p):
        # print("exists:", name)
        return
    # print("create:", name)
    d = dirname(p)
    if not isdir(d):
        mkdir(d)
    if data is not None:
        with open(p, 'wt', encoding='utf-8') as f:
            f.write(data)
        if copy is not None:
            copystat(src=copy, dst=p)
    elif copy is not None:
        copy2(src=copy, dst=p)


def readall(file):
    with open(file, 'rt', encoding='utf-8') as f:
        return f.read()


def copy_file(name, filter=None, overwrite=False):
    src = join(SELF_DIR, 'pkg-contents', name)
    data = None
    if filter is not None:
        data = filter(readall(src))
    place_file(name, data, src, overwrite)


def replace_rtt_root(data):
    return data.replace('{RT_THREAD_ROOT}', ENV_RT_DIR)


def replace_self_name(data):
    return data.replace('{SELF_NAME}', SELF_NAME)


def replace_self_path(data):
    if SELF_DIR_REL is None:
        return data.replace('{SELF_DIR}', SELF_DIR)
    else:
        return data.replace('{SELF_DIR}', '{CWD}/' + SELF_DIR_REL)


for i in ['c_cpp_properties.json', 'extensions.json']:
    copy_file(f'.vscode/{i}')
copy_file('.vscode/settings.json', replace_rtt_root)

if not isdir(join(INSTALL_TO, 'applications')):
    for i in ['app.h', 'main.c']:
        copy_file(f'applications/{i}')

copy_file('applications/SConscript')
copy_file('ports/SConscript')

for i in ['.gitignore', '.editorconfig', 'version.txt', 'SConscript']:
    copy_file(i)

copy_file('README.md', replace_self_name)
copy_file('control.py', replace_self_path, overwrite=True)
ctlpy = join(INSTALL_TO, 'control.py')
chmod(ctlpy, 0o777)

tasks_file_path = join(SELF_DIR, 'pkg-contents/.vscode/tasks.json')
tasks_file_dist_path = join(INSTALL_TO, '.vscode/tasks.json')

with open(tasks_file_path, 'rt') as tasks_file:
    tasks = load(tasks_file)

if isfile(tasks_file_dist_path):
    with open(tasks_file_dist_path, 'rt') as tasks_file_dist:
        try:
            merge_to = load(tasks_file_dist)
        except:
            merge_to = {}
else:
    merge_to = {}

merge_to['version'] = tasks['version']
known_keys = []
for task in tasks['tasks']:
    known_keys.append(task['id'])


def find(id):
    for task in tasks['tasks']:
        if task['id'] == id:
            task['# class'] = 'rt-thread-w60x'
            task['# comment'] = '这个项目是自动生成的，不要修改'
            return task
    raise Exception(f"no found task {id}")


if 'tasks' not in merge_to:
    merge_to['tasks'] = []
for task_index, task in reversed(list(enumerate(merge_to['tasks']))):
    if task.get('# class') == 'rt-thread-w60x':
        if task.get('id') in known_keys:
            merge_to['tasks'][task_index] = find(task['id'])
            known_keys.remove(task['id'])
        else:
            merge_to['tasks'].remove(task)
for task_id in known_keys:
    merge_to['tasks'].append(find(task_id))

with open(tasks_file_dist_path, 'wt') as tasks_file:
    dump(merge_to, tasks_file, quote_keys=True, allow_duplicate_keys=False, ensure_ascii=False, indent='\t')
