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

    serial_instance = serial_for_url(portpath, baudrate, timeout=timeout, parity=PARITY_NONE, stopbits=1, bytesize=8, rtscts=False, xonxoff=False, do_not_open=True)
    serial_instance.dtr = False
    serial_instance.rts = False
    serial_instance.exclusive = True
    try:
        if open:
            serial_instance.open()
    except SerialException as e:
        debug('could not open port {portpath}: {e}\n')
        return None
    return serial_instance
