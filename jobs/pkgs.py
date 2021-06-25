from pathlib import Path
from helpers import exec_pass, die, print, ENV_ROOT, PROJECT_ROOT, PACKAGES_ROOT

help_title = '运行pkgs'


def reset_pkgs():
    print("reset packages...")
    for dotGitDir in Path(PACKAGES_ROOT).glob('*/.git'):
        path = dotGitDir.parent.absolute().as_posix()
        exec_pass("git", ['reset', '--hard'], cwd=path)
        exec_pass("git", ['clean', '-ffdx'], cwd=path)


def main(argv):
    print(argv)
    if len(argv) > 0 and argv[0] == '--force-update':
        reset_pkgs()
    argv.insert(0, "--")
    argv.insert(0, f"source '{ENV_ROOT}/env.sh'; set -x; exec pkgs \"$@\"")
    argv.insert(0, "-c")
    exec_pass("bash", argv, cwd=PROJECT_ROOT)
