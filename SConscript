from building import *
from os.path import join, split, isfile, abspath, dirname
from os import dup, listdir

__dir__ = dirname(abspath((lambda x: x).__code__.co_filename))


def IncludeFolder(path, variant_dir='', duplicate=0, missing_ok=False):
    objs = []
    if variant_dir and not variant_dir.endswith('/'):
        variant_dir += '/'
    absfile = join(path, 'SConscript')
    if isfile(absfile):
        debug(f'Using {absfile}')
        base = SConscript(absfile, duplicate=duplicate, variant_dir=variant_dir)
        if base is None:
            die(f"Missing Return(...) in {absfile}")
        objs += base
    elif not missing_ok:
        die(f"Missing imported file: {absfile}")
    return objs


def IncludeChilds(root, variant_dir='', skip=[], duplicate=0):
    objs = []

    if variant_dir and not variant_dir.endswith('/'):
        variant_dir += '/'

    for d in listdir(root):
        if d in skip:
            continue

        path = join(root, d)
        if path == __dir__ or path == PKGS_DIR:
            continue

        objs += IncludeFolder(path, variant_dir=variant_dir + d, duplicate=duplicate, missing_ok=True)
    return objs


Import('PROJECT_ROOT')
Import('LIBRARY_ROOT')
Import('BSP_ROOT')
Import('PKGS_DIR')
Import('debug')
Import('die')
Export('IncludeChilds')
Export('IncludeFolder')

self_dir = split(LIBRARY_ROOT)[1]

proj_script = join(PROJECT_ROOT, 'SConscript')
debug(f'Using {proj_script}')

objs = []

objs += IncludeFolder(PKGS_DIR, variant_dir='10-packages')

if isfile(proj_script):
    base = SConscript(proj_script, duplicate=0, variant_dir='00-user')
    if base is None:
        die(f"Missing Return(...) in {proj_script}")
    objs += base
else:
    objs += IncludeChilds(PROJECT_ROOT, variant_dir='00-user', skip=[self_dir], duplicate=0)

objs += IncludeChilds(BSP_ROOT, duplicate=0, variant_dir='99-bsp', skip=['applications'])

objs += IncludeFolder(join(LIBRARY_ROOT, 'src'), variant_dir='50-w60x-gongt-helpers', duplicate=0, missing_ok=False)

Return('objs')
