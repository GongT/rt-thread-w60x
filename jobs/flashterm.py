from helpers import print, open_port, exclusive_kill,do_exit

from .flash import flash
from .term import term
from . import get_port_number_from_first_arg

help_title = '刷机并打开串口'


def main(argv):
    exclusive_kill()
    serial_instance = open_port(get_port_number_from_first_arg(argv))
    if serial_instance is None:
        do_exit(1)
    r = flash(serial_instance, '--force' in argv, False)
    if not r:
        print("刷机失败")
        return
    serial_instance.baudrate = 115200
    print("切换到串口输出，请等待程序解压缩……")
    term(serial_instance)
