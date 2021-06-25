from os.path import join, isfile, isdir
from os import mkdir, environ
from .pathvars import ENV_ROOT

ENV_FILE = join(ENV_ROOT, "rt-thread-w60x.env.sh")
already_open = False
data = {}

if 'CI' in environ:
    already_open = True


def read_file():
    global already_open, data
    if already_open:
        return
    already_open = True

    if not isdir(ENV_ROOT):
        mkdir(ENV_ROOT)
    if isfile(ENV_FILE):
        with open(ENV_FILE, 'rt') as myfile:
            for line in myfile:
                name, var = line.partition('=')[::2]
                name = name.strip()
                if name[0] == '#':
                    continue
                data[name] = var.strip()


def try_get_env(name):
    read_file()
    if name in data:
        return data[name]
    else:
        return None


def save_env(name, value):
    global data
    read_file()
    data[name] = value

    with open(ENV_FILE, 'wt') as myfile:
        for k, v in data.items():
            myfile.write(f'{k}={v}\n')
