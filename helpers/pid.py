from os import getpid, kill, mkdir, remove, waitpid
from sys import exit
from signal import SIGINT
from os.path import isdir, isfile
from .pathvars import BIN_PATH, PID_FILE, SELF_BIN_PATH

PID_WRITE = False


def do_exit(code):
    if PID_WRITE:
        remove(PID_FILE)
    exit(code)


def exclusive_kill():
    if isfile(PID_FILE):
        with open(PID_FILE, 'rt') as f:
            pid = int(f.read())
            print(f'kill process {pid}')
            try:
                kill(pid, SIGINT)
                waitpid(pid, 0)
            except:
                pass

    with open(PID_FILE, 'wt') as f:
        f.write(str(getpid()))

    global PID_WRITE
    PID_WRITE = True
