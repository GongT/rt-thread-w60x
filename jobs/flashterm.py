from helpers import print,open_port

from .flash import flash
from .term import term
from . import get_port_number_from_first_arg

help_title = '刷机并打开串口'

def main(argv):
    exclusive_kill()
    serial_instance = open_port(get_port_number_from_first_arg(argv))
    r=flash(serial_instance, '--force' in argv,False)
    if not r:
        return
    print("drop to terminal, please wait device decompress code...")
    term(serial_instance)
