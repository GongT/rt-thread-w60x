from .pathvars import SELF_ROOT
from importlib.util import spec_from_file_location, module_from_spec
from os.path import join, isfile


def action_file(action):
    return join(SELF_ROOT, f"jobs/{action}.py")


def load(action):
    spec = spec_from_file_location(f"jobs.{action}", action_file(action))
    mdl = module_from_spec(spec)
    spec.loader.exec_module(mdl)
    return mdl


def loadJob(action):
    if isfile(action_file(action)):
        return getattr(load(action), 'main')
    else:
        return None


def loadJobDesc(action):
    try:
        return getattr(load(action), 'help_title', '')
    except Exception as e:
        return str(e)
