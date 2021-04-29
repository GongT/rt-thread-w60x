from helpers import print, open_port, exclusive_kill

from .flash import flash
from .term import term
from . import get_port_number_from_first_arg

help_title = '刷机并打开串口'


def main(argv):
    exclusive_kill()
    serial_instance = open_port(get_port_number_from_first_arg(argv))
    r = flash(serial_instance, '--force' in argv, False)
    if not r:
        print("刷机失败")
        return
    print("切换到串口输出，请等待程序解压缩……")
    term(serial_instance)
