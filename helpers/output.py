from sys import stderr, argv
from os.path import join, dirname, splitext
from os import listdir
from .job import loadJobDesc
from .pid import do_exit


def Usage(Die=True):
    debug(f"Usage: {argv[0]} <action> [...args], valid action is: ")
    for I in listdir(join(dirname(__file__), '../jobs')):
        if I != '__init__.py' and I.endswith('.py'):
            action = splitext(I)[0]

            debug(f"    {action} -", end='')
            debug("", loadJobDesc(action))
    if Die:
        die('')


def debug(*vargs, **kvargs):
    print(*vargs, **kvargs, file=stderr)


def die(msg):
    debug(msg)
    do_exit(1)
