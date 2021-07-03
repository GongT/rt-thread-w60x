from subprocess import run, PIPE
from sys import executable as argv0, stderr, stdin

from .output import debug as print
from .pid import do_exit
from .pathvars import PROJECT_ROOT


def python_pass(args, encoding=None):
    exec_pass(argv0, args, encoding)


def exec_pass(exe, args, encoding=None, cwd=PROJECT_ROOT):
    print("\x1B[2m +", exe, ' '.join(args), "\x1B[0m")
    p = run(executable=exe, args=[exe, *args], stderr=stderr, stdout=stderr, shell=False, encoding=encoding, cwd=cwd)
    print("\x1B[2m +", exe, ' '.join(args), '- exit with code', p.returncode, "\x1B[0m")
    if p.returncode != 0:
        print("\x1B[38;5;9mcommand failed.\x1B[0m")
        do_exit(p.returncode)

def exec_get(exe, args, encoding='utf8', cwd=PROJECT_ROOT):
    print("\x1B[2m +", exe, ' '.join(args), "\x1B[0m")
    p = run(executable=exe, args=[exe, *args], stderr=stderr, stdout=PIPE, input="", shell=False, encoding=encoding, cwd=cwd)
    print("\x1B[2m +", exe, ' '.join(args), '- exit with code', p.returncode, "\x1B[0m")
    if p.returncode != 0:
        print("\x1B[38;5;9mcommand failed.\x1B[0m")
        do_exit(p.returncode)
    return p.stdout

def eval_pass(fn, args, name=None):
    if name is None:
        name = fn.__name__
    print("\x1B[2m +", name, ' '.join(args), "\x1B[0m")
    return fn([name] + args)


def stream_process(process):
    go = process.poll() is None
    for line in process.stdout:
        print(line)
    return go
