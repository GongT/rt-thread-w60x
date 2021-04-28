from os import name as PLATFORM_NAME, getenv
from .scons import scons

help_title = "运行menuconfig（或pyconfig）"


def main(argv):
    if PLATFORM_NAME == 'nt' or getenv('DISPLAY') is not None:
        scons(['--pyconfig'])
    else:
        scons(['--menuconfig'])
