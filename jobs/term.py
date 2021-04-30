from serial.tools.miniterm import Miniterm, key_description
from helpers import print, open_port, exclusive_kill
from . import get_port_number_from_first_arg

help_title = '打开串口'


def main(argv):
    serial_instance = open_port(get_port_number_from_first_arg(argv))

    if serial_instance is None:
        do_exit(1)

    term(serial_instance)


def term(serial_instance):
    exclusive_kill()
    encoding = 'Latin1'

    if not hasattr(serial_instance, 'cancel_read'):
        # enable timeout for alive flag polling if cancel_read is not available
        serial_instance.timeout = 1
    serial_instance.write_timeout = None

    serial_instance.baudrate = 115200

    miniterm = Miniterm(serial_instance, echo=False, eol='lf')
    miniterm.raw = True
    miniterm.set_rx_encoding(encoding)
    miniterm.set_tx_encoding(encoding)

    print('--- Miniterm on {p.name}  {p.baudrate},{p.bytesize},{p.parity},{p.stopbits} ---\n'.format(p=miniterm.serial))
    print('--- Quit: {} | Menu: {} | Help: {} followed by {} ---\n'.format(
        key_description(miniterm.exit_character), key_description(miniterm.menu_character), key_description(miniterm.menu_character), key_description('\x08')))

    miniterm.start()
    try:
        miniterm.join(True)
    except KeyboardInterrupt:
        pass
    print('\n--- exit ---\n')
    miniterm.join()
    miniterm.close()
