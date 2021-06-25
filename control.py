#!/usr/bin/env python3

from helpers import Usage, do_exit, loadJob, print, BIN_PATH, SELF_BIN_PATH
from os.path import isdir
from os import mkdir
from sys import argv
import traceback


def main(argv):
    pass

    action = argv[0]
    argv = argv[1:]

    handler = loadJob(action)
    if handler is None:
        print("action not found: " + action)
        Usage(True)

    if not isdir(BIN_PATH):
        mkdir(BIN_PATH)

    if not isdir(SELF_BIN_PATH):
        mkdir(SELF_BIN_PATH)

    handler(argv)
    do_exit(0)


if len(argv) == 1:
    Usage(True)
try:
    main(argv[1:])
except KeyboardInterrupt:
    print('\r^C')
except SystemExit as e:
    exit(e.code)
except:
    traceback.print_exc()
    do_exit(1)
