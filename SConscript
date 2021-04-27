from building import *
from os.path import join, split, isfile
from os import listdir

Import('PROJECT_ROOT')
Import('LIBRARY_ROOT')
Import('BSP_ROOT')
Import('debug')
Import('die')

self_dir = split(LIBRARY_ROOT)[1]

objs = []


def IncludeChilds(root, vdparent='', skip=[]):
    global objs

    if vdparent:
        vdparent += '/'

    for d in listdir(root):
        if d in skip:
            continue

        path = join(root, d)
        absfile = join(path, 'SConscript')
        if isfile(absfile):
            debug(f'Using {absfile}')
            objs += SConscript(absfile, duplicate=0, variant_dir=vdparent + d)


IncludeChilds(PROJECT_ROOT, skip=[self_dir])
IncludeChilds(BSP_ROOT, vdparent='bsp', skip=['applications'])

# absfile = join(BSP_ROOT, 'SConscript')
# debug(f'Using {absfile}')
# objs += SConscript(absfile, duplicate=1, variant_dir='bsp')

Return('objs')
