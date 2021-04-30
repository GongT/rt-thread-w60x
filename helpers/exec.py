from subprocess import run
from sys import stderr, stdout, executable as argv0
from .output import debug as print
from .pid import do_exit


def python_pass(args, encoding=None):
    exec_pass(argv0, args, encoding)


def exec_pass(exe, args, encoding=None):
    print("\x1B[2m +", exe, ' '.join(args), "\x1B[0m")
    p = run(executable=exe, args=[exe, *args], stderr=stderr, stdout=stderr, shell=False, encoding=encoding)
    print("\x1B[2m +", exe, ' '.join(args), '- exit with code', p.returncode, "\x1B[0m")
    if p.returncode != 0:
        print("\x1B[38;5;9mcommand failed.\x1B[0m")
        do_exit(p.returncode)


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
