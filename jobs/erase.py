from os.path import isfile
from os import remove
from helpers import goto_flash_mode, exclusive_kill, open_port, do_exit, FLASH_SIGNAL, control_reset
from .scons import main as scons
from . import get_port_number_from_first_arg

help_title = "清除芯片内部Flash"


def main(argv):
    exclusive_kill()
    serial_port = open_port(get_port_number_from_first_arg(argv), open=True)
    if serial_port is None:
        do_exit(1)

    mode = goto_flash_mode(serial_port)

    if isfile(FLASH_SIGNAL):
        remove(FLASH_SIGNAL)

    if not mode:
        do_exit(1)
    erase_cmd = bytes.fromhex('210600414532000000')

    serial_port.timeout = None
    i = 0
    while (True):
        print(serial_port.read(1).decode(), end='', flush=True)
        i += 1
        if i == 4:
            print("send ", erase_cmd, '!')
        elif i == 5:
            print("flash erased!")
            break
    control_reset(serial_port)
