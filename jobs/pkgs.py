from helpers import exec_pass, die, print, ENV_ROOT, PROJECT_ROOT

help_title = '运行pkgs'


def main(argv):
    argv.insert(0, "--")
    argv.insert(0, f"source '{ENV_ROOT}/env.sh'; set -x; exec pkgs \"$@\"")
    argv.insert(0, "-c")
    exec_pass("bash", argv, cwd=PROJECT_ROOT)
