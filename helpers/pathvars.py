from os.path import dirname, join, abspath
from os import getcwd, getenv

SELF_ROOT = dirname(dirname(__file__))
PID_FILE = join(SELF_ROOT, '.control.pid')

PROJECT_ROOT = getenv('PROJECT_ROOT', abspath(getcwd()))

BIN_PATH = join(PROJECT_ROOT, 'Bin')
SELF_BIN_PATH = join(SELF_ROOT, 'Bin')
BINARY_NAME = 'application'

ELF_FILE = join(SELF_BIN_PATH, f'{BINARY_NAME}.elf')

TEMP_BIN_FILE = join(SELF_BIN_PATH, f'{BINARY_NAME}.bin')
TEMP_IMG_FILE = join(SELF_BIN_PATH, f'{BINARY_NAME}.img')
TEMP_FLS_FILE = join(SELF_BIN_PATH, f'{BINARY_NAME}.fls')

BIN_FILE = join(SELF_BIN_PATH, f'{BINARY_NAME}.bin')
IMG_FILE = join(BIN_PATH, f'{BINARY_NAME}.img')
FLS_FILE = join(BIN_PATH, f'{BINARY_NAME}.fls')

FLASH_SIGNAL = join(BIN_PATH, 'already-flash')
VERSION_FILE = join(PROJECT_ROOT, 'version.txt')

PACKAGES_ROOT = join(PROJECT_ROOT, 'packages')

del dirname, join, abspath, getcwd, getenv
