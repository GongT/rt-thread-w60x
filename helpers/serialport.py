from time import sleep
from xmodem import XMODEM1k as XMODEM
from serial import Serial, PARITY_NONE, SerialException
from pyprind import ProgBar
import threading
from serial import serial_for_url, SerialException, PARITY_NONE
from os import name as PLATFORM_NAME
from .output import debug, die
from .vscode_config import require_argument


def port_path(portnumber):
    if portnumber is None:
        portnumber = str(require_argument('SERIAL_PORT', 'serialPortNumber', '1'))
    if portnumber.startswith('COM') or portnumber.startswith('/'):
        return portnumber
    if PLATFORM_NAME == 'nt':
        return f'COM{portnumber}'
    else:
        return f'/dev/ttyUSB{portnumber}'


def open_port(portnumber, baudrate=115200, timeout=0, write_timeout=None, open=True):
    portpath = port_path(portnumber)

    serial_instance = serial_for_url(
        portpath, baudrate, write_timeout=write_timeout, timeout=timeout, parity=PARITY_NONE, stopbits=1, bytesize=8, rtscts=False, xonxoff=False, do_not_open=True)
    serial_instance.dtr = False
    serial_instance.rts = False
    serial_instance.exclusive = True
    try:
        if open:
            serial_instance.open()
    except SerialException as e:
        debug(f'could not open port {portpath}: {e}\n')
        return None
    return serial_instance


def control_reset(serial_instance):
    try:
        serial_instance.rts = True
        serial_instance.rts = False
        print("try hardware reset by RTS line")
    except:
        pass


def goto_flash_mode(serial_port):
    print('请重启设备！')
    stop_hold = threading.Event()
    holder_thread = threading.Thread(target=hold_esc, args=[serial_port, stop_hold], name='hold_esc')
    holder_thread.daemon = False
    holder_thread.start()

    serial_port.reset_output_buffer()
    serial_port.reset_input_buffer()

    sleep(0.5)
    control_reset(serial_port)

    c_cnt = 0
    p_cnt = 0
    # memory_input = ""
    while True:
        if not holder_thread.is_alive():
            print('hold thread died, flash fail.')
            RET = False
            break
        char_in = serial_port.read(1)
        if char_in is None or len(char_in) == 0 or char_in == b'\x1B':
            continue

        if char_in == b'C':
            c_cnt += 1
            if c_cnt >= 3:
                RET = 'C'
                break
        elif char_in == b'P':
            p_cnt += 1
            if p_cnt >= 3:
                RET = 'P'
                break
        else:
            # memory_input += str(char_in)
            c_cnt = 0
            p_cnt = 0
            serial_port.read_all()

    stop_hold.set()

    print(f'Got {RET}!')

    # if memory_input.find("secboot running") < 0:
    #     print("not found 'secboot running'")

    return RET


def hold_esc(serial_port, stop):
    from struct import pack
    try:
        while not stop.is_set():
            serial_port.write(pack('<B', 27))
            sleep(0.1)
            # read all that is there or wait for one byte
    except SerialException:
        print(f"hold ESC failed: {e}")
