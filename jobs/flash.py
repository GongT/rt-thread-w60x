from os import stat
from os.path import isfile
from time import sleep
from xmodem import XMODEM1k as XMODEM
from serial import Serial, PARITY_NONE, SerialException
from pyprind import ProgBar

from helpers import FLS_FILE, goto_flash_mode, print, do_exit, open_port, port_path, control_reset, FLASH_SIGNAL, PROJECT_ROOT, IMG_FILE, do_exit, die, exclusive_kill
from . import get_port_number_from_first_arg

help_title = '刷机'


def main(argv):
    exclusive_kill()
    serial_port = open_port(get_port_number_from_first_arg(argv), open=True)
    if serial_port is None:
        do_exit(1)
    r = flash(serial_port, '--force' in argv, '--low' in argv)
    if not r:
        do_exit(1)


def flash(serial_port, force, low_speed):
    # init
    stat_image_file = stat(IMG_FILE)
    p_bar = ProgBar(stat_image_file.st_size)

    def clear_buffer():
        serial_port.reset_output_buffer()
        serial_port.reset_input_buffer()

    def read_with_bar(data, timeout=0):
        return serial_port.read(data)

    def write_with_bar(data, timeout=0):
        write_with_bar.current += len(data)
        p_bar.title = "%d / %d" % (write_with_bar.current, stat_image_file.st_size)
        p_bar.update(len(data))
        ret = serial_port.write(data)
        sleep(0.001)
        return ret

    write_with_bar.current = 0

    # go to flash
    mode = goto_flash_mode(serial_port)

    if mode == 'C':
        image_file = IMG_FILE
    elif mode == 'P':
        image_file = FLS_FILE
    else:
        return False

    mac = ''
    get_mac_cmd = bytes.fromhex('210600ea2d38000000')
    serial_port.timeout = None
    while True:
        sleep(0.1)
        serial_port.write(get_mac_cmd)
        mac = (serial_port.read_until())
        pos = mac.find(b'MAC:')
        if pos >= 0:
            mac = mac[pos + 4:len(mac) - 1].decode("ascii")
            break

    print('MAC Address: %s' % mac)
    if isfile(FLASH_SIGNAL) and not force:
        with open(FLASH_SIGNAL, 'rt') as f:
            if f.read().strip() == mac:
                print("this device already flash this program! skip flash. (--force to overwrite)")
                clear_buffer()
                control_reset(serial_port)
                return True

    # up speed
    def switch_baudrate(br):
        clear_buffer()
        serial_port.baudrate = br

    if not low_speed:
        print('switching to 2M baudrate...')
        sleep(0.2)
        speed_magic = bytes.fromhex('210a00ef2a3100000080841e00')
        serial_port.write(speed_magic)
        sleep(0.01)
        switch_baudrate(2000000)
        serial_port.timeout = 300
        sleep(0.01)
        wront_cnt = 0
        while True:
            c_in = serial_port.read(1)
            # print('got: "%s"' % c_in)
            if c_in == b'C' or c_in == b'P':
                break
            if c_in == b'\x00':
                continue
            elif wront_cnt >= 10:
                print('retry...')
                wront_cnt = 0
                switch_baudrate(115200)
                serial_port.write(speed_magic)
                switch_baudrate(2000000)
                sleep(0.01)
            else:
                wront_cnt += 1
        print('high speed mode!')
    serial_port.timeout = None

    print('sending file:', image_file)
    stream = open(image_file, 'rb')

    clear_buffer()
    modem = XMODEM(getc=read_with_bar, putc=write_with_bar)
    print("please wait for download....")
    result = modem.send(stream)
    print('')
    if result:
        print("download image success!")
        with open(FLASH_SIGNAL, 'wt') as f:
            f.write(mac)
    else:
        print("download image fail!")
        return False

    stream.close()

    clear_buffer()
    return True
