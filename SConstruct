from os import getenv, getcwd, chdir, environ
from os.path import join, abspath, dirname, isfile
from sys import path as importPath, stderr, executable as argv0
from pathlib import Path
import re


def die(msg):
    debug(msg)
    exit(1)


def debug(*vargs, **kvargs):
    print(*vargs, **kvargs, file=stderr)


Export('die')
Export('debug')

LIBRARY_ROOT = dirname((lambda x: x).__code__.co_filename)
print(f" * LIBRARY_ROOT = {LIBRARY_ROOT}")
Export('LIBRARY_ROOT')

PROJECT_ROOT = getenv('PROJECT_ROOT')  # abspath(getcwd())
print(f" * PROJECT_ROOT = {PROJECT_ROOT}")
Export('PROJECT_ROOT')

PKGS_DIR = join(PROJECT_ROOT, 'packages')
print(f" * PKGS_DIR = {PKGS_DIR}")
Export('PKGS_DIR')

if LIBRARY_ROOT == PROJECT_ROOT:
    die("LIBRARY_ROOT must not same with PROJECT_ROOT")

RTT_ROOT = getenv('RTT_ROOT')
if not RTT_ROOT:
    die("no RTT_ROOT environment, you must set it in settings.json")
BSP_ROOT = join(RTT_ROOT, 'bsp/w60x')

BINARY_NAME = getenv('BINARY_NAME', 'app_bin')

importPath.append(join(RTT_ROOT, 'tools'))
importPath.append(BSP_ROOT)

environ["BSP_ROOT"] = BSP_ROOT
environ["RTT_ROOT"] = RTT_ROOT
environ["PKGS_DIR"] = PKGS_DIR
environ["ENV_ROOT"] = join(Path.home(), '.env')

print(" * RTT_ROOT = %s" % RTT_ROOT)

# 加载最主要的构建设置文件
try:
    chdir(LIBRARY_ROOT)
    sc = SConscript

    def SConscript(f, *args, **kw):
        debug('CALL ', f)

    from building import *
except:
    print('Cannot found RT-Thread root directory, please edit project settings file, or set environment variable "RTT_ROOT".')
    print('找不到 RT-Thread 根目录，请修改项目配置文件，或设置环境变量“RTT_ROOT”')
    print('\x1B[38;5;3m./control.py rtt update\x1B[0m')
    exit(-1)

rtconfig_file = join(BSP_ROOT, 'rtconfig.py')
if not isfile(rtconfig_file):
    print(f'missing {rtconfig_file}.')
    exit(-1)

BUILD_ENV = getenv('BUILD_ENV', 'debug')
# rtconfig.py补丁
with open(rtconfig_file, 'r+t') as rtconfig_fd:
    content = rtconfig_fd.read()
    old_content = content

    r_want = re.compile(f"^BUILD = '{BUILD_ENV}'$", re.MULTILINE)
    if re.search(r_want, content) == None:
        r_repl = re.compile("^BUILD\s*=.*$", re.MULTILINE)
        CODE = f"BUILD = '{BUILD_ENV}'"
        if re.search(r_repl, content) == None:
            content = CODE + '\n\n' + content
        else:
            content = re.sub(r_repl, CODE, content)

    if content.find(" -w ") != -1:
        content = content.replace(" -w ", " ")

    if content.find(" -mcpu=cortex-m3 -mthumb ") != -1:
        content = content.replace(" -mcpu=cortex-m3 -mthumb ", " -march=armv7-m -mtune=cortex-m3 -mthumb ")

    if content != old_content:
        print("[WARN] patch file: %s" % rtconfig_fd.name)
        rtconfig_fd.seek(0)
        rtconfig_fd.write(content)
        rtconfig_fd.truncate()
Export('BUILD_ENV')

# 加载w60x特定的构建设置
if True:
    chdir(BSP_ROOT)
    import rtconfig
    chdir(LIBRARY_ROOT)

rtconfig.POST_ACTION = f'''
$SIZE $TARGET
$OBJCPY -O binary $TARGET Bin/{BINARY_NAME}.bin
{argv0} {LIBRARY_ROOT}/control.py makeimg
'''

GCC_OPT = getenv('GCC_OPT', '2')
rtconfig.CFLAGS = re.sub(' -O. ', f' -O{GCC_OPT} ', rtconfig.CFLAGS)
rtconfig.CFLAGS += ' -fdiagnostics-color=always -fdiagnostics-urls=always '

# 导出
Export('BSP_ROOT')
Export('RTT_ROOT')
Export('rtconfig')

TARGET = f'Bin/{BINARY_NAME}.{rtconfig.TARGET_EXT}'

# 输出调试信息
print(" * COMPILER_PATH = %s" % rtconfig.EXEC_PATH)
rtconfig.LFLAGS = rtconfig.LFLAGS.replace('drivers/linker_scripts', join(BSP_ROOT, 'drivers/linker_scripts'))

print(" * ASFLAGS = %s" % rtconfig.AFLAGS)
print(" * CCFLAGS = %s" % rtconfig.CFLAGS)
print(" * LINKFLAGS = %s" % rtconfig.LFLAGS)

# Kconfig补丁
with open(join(BSP_ROOT, 'Kconfig'), 'r+t') as kconf_file:
    content = kconf_file.read()
    import re
    if re.search('^mainmenu', content) != None:
        print("[WARN] patch file: %s" % kconf_file.name)
        content = re.sub('^mainmenu', '# mainmenu', content)
        kconf_file.seek(0)
        kconf_file.write(content)
        kconf_file.truncate()

# 导出构建过程
DefaultEnvironment(tools=[])
env = Environment(
    tools=['mingw'],
    AS=rtconfig.AS,
    ASFLAGS=rtconfig.AFLAGS,
    CC=rtconfig.CC,
    CCFLAGS=rtconfig.CFLAGS,
    AR=rtconfig.AR,
    ARFLAGS='-rc',
    LINK=rtconfig.LINK,
    LINKFLAGS=rtconfig.LFLAGS,
    SIZE=rtconfig.SIZE,
    OBJCPY=rtconfig.OBJCPY,
    CPPPATH=[join(LIBRARY_ROOT, 'include')],
    CPPDEFINES=[('BUILD_ENV', BUILD_ENV)],
    COMPILATIONDB_USE_ABSPATH=True)
Export('env')
env.PrependENVPath('PATH', rtconfig.EXEC_PATH)
env.PrependENVPath('PROJECT_ROOT', PROJECT_ROOT)
env.PrependENVPath('LIBRARY_ROOT', LIBRARY_ROOT)

if rtconfig.PLATFORM == 'iar':
    env.Replace(CCCOM=['$CC $CCFLAGS $CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS -o $TARGET $SOURCES'])
    env.Replace(ARFLAGS=[''])
    env.Replace(LINKCOM=env["LINKCOM"] + ' --map project.map')

objs = PrepareBuilding(env, RTT_ROOT, has_libcpu=False)
env['BSP_ROOT'] = BSP_ROOT

# 生成compile_commands.json
env.Tool('compilation_db')
cdb = env.CompilationDatabase('.vscode/compile_commands.json')
Alias('cdb', cdb)

# 运行
DoBuilding(TARGET, objs)
