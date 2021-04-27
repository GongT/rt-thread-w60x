from os import stat
from os.path import isfile
from time import sleep
from xmodem import XMODEM1k as XMODEM
from serial import Serial, PARITY_NONE
from pyprind import ProgBar
import struct
import threading

from helpers import print, open_port, port_path, FLASH_SIGNAL, PROJECT_ROOT, IMG_FILE, do_exit, die, exclusive_kill
from . import get_port_number_from_first_arg

help_title = '刷机'


def main(argv):
    exclusive_kill()
    serial_port = open_port(get_port_number_from_first_arg(argv), open=True)
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
    print('please restart device!')
    stop_hold = threading.Event()
    holder_thread = threading.Thread(target=hold_esc, args=[serial_port, stop_hold], name='hold_esc')
    holder_thread.daemon = False
    holder_thread.start()

    c_cnt = 0
    while True:
        if not holder_thread.is_alive():
            print('hold thread died, flash fail.')
            return False
        c_in = serial_port.read(1)
        if c_in is None or len(c_in) == 0 or c_in == b'\x1B':
            continue

        if c_in == b'C':
            c_cnt += 1
            if c_cnt >= 3:
                break
        else:
            c_cnt = 0
            serial_port.read_all()

    stop_hold.set()
    print('\nGot CCC...')

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
                return True

    # up speed
    def switch_baudrate(br):
        clear_buffer()
        serial_port.baudrate = br

    if not low_speed:
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
            if c_in == b'C':
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
        print('Enter high speed mode!')
    serial_port.timeout = None

    stream = open(IMG_FILE, 'rb')

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


def hold_esc(serial_port, stop):
    try:
        while not stop.is_set():
            serial_port.write(struct.pack('<B', 27))
            sleep(0.1)
            # read all that is there or wait for one byte
    except serial.SerialException:
        print(f"hold ESC failed: {e}")
