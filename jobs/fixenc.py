from os import name as PLATFORM_NAME, getenv
from pathlib import Path
from helpers import PACKAGES_ROOT, exec_get

help_title = "修复packages中的文件编码"


def main(argv):
    print(PACKAGES_ROOT)
    files = sorted(Path(PACKAGES_ROOT).glob("**/*.c")) + sorted(Path(PACKAGES_ROOT).glob("**/*.h"))
    for file in files:
        try:
            text = file.read_text(encoding='gb18030')
            if type(text) is str:
                # print("write file:",file.absolute().as_posix())
                file.write_text(text, encoding="utf8")
        except Exception as e:
            # print("failed file:",file.absolute().as_posix(), e)
            pass
