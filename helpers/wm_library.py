from json import load
from os.path import join
from importlib.util import spec_from_file_location, module_from_spec

from .pathvars import PACKAGES_ROOT
from .output import debug, die

wm_lib_path = None


def find_wm_library():
    global wm_lib_path
    if wm_lib_path is not None:
        return
    try:
        with open(join(PACKAGES_ROOT, 'pkgs.json'), 'rt') as f:
            data = load(f)
        for ele in data:
            if ele['name'] == 'WM_LIBRARIES':
                wm_lib_path = join(PACKAGES_ROOT, 'wm_libraries-' + ele['ver'])
                debug(f"use wm library path {wm_lib_path}...")
                return
    except:
        die("missing packages, you should run `pkgs --update`")
    die("can not found wm_libraries, you must select w60X from menuconfig")


def load_wm_module(name):
    spec = spec_from_file_location(f"wm_libraries.{name}", tools_path(f"{name}.py"))
    mdl = module_from_spec(spec)
    spec.loader.exec_module(mdl)
    return mdl


def tools_path(element):
    find_wm_library()
    return join(wm_lib_path, f"Tools/{element}")
