from building import *
from os.path import join, split, isfile, abspath, dirname
from os import listdir

__dir__ = dirname(abspath((lambda x: x).__code__.co_filename))


def IncludeChilds(root, variant_dir='', skip=[], duplicate=0):
    objs = []

    if variant_dir:
        variant_dir += '/'

    for d in listdir(root):
        if d in skip:
            continue

        path = join(root, d)
        if path == __dir__:
            continue

        absfile = join(path, 'SConscript')
        if isfile(absfile):
            debug(f'Using {absfile}')
            objs += SConscript(absfile, duplicate=duplicate, variant_dir=variant_dir + d)
    return objs


Import('PROJECT_ROOT')
Import('LIBRARY_ROOT')
Import('BSP_ROOT')
Import('debug')
Import('die')
Export('IncludeChilds')

self_dir = split(LIBRARY_ROOT)[1]

proj_script = join(PROJECT_ROOT, 'SConscript')
debug(f'Using {proj_script}')

objs = []
objs += SConscript(proj_script, duplicate=0, variant_dir='user')
objs += IncludeChilds(BSP_ROOT, duplicate=0, variant_dir='bsp', skip=['applications'])

Return('objs')
