from os import chmod, remove
from os.path import isfile

from helpers import md5_file, die, exec_pass, load_wm_module, tools_path, python_pass, eval_pass, BIN_FILE, VERSION_FILE, IMG_FILE, FLS_FILE, FLASH_SIGNAL, print

# 1M
# "python" $WM_TOOLS/wm_gzip.py "./Bin/rtthread.bin"
# "$WM_TOOLS/makeimg" "./Bin/rtthread.bin" "./Bin/rtthread_1M.img" 0 0 "./Bin/version.txt" 90000 10100
# "$WM_TOOLS/makeimg" "./Bin/rtthread.bin.gz" "./Bin/rtthread_GZ_1M.img" 0 1 "./Bin/version.txt" 90000 10100 "./Bin/rtthread.bin"
# "$WM_TOOLS/makeimg" "./Bin/rtthread.bin" "./Bin/rtthread_SEC_1M.img" 0 0 "./Bin/version.txt" 90000 10100
# "$WM_TOOLS/makeimg_all" "./Bin/secboot.img" "./Bin/rtthread_1M.img" "./Bin/rtthread_1M.FLS"
# 2M
# "python" $WM_TOOLS/wm_gzip.py "./Bin/rtthread.bin"
# "$WM_TOOLS/makeimg" "./Bin/rtthread.bin" "./Bin/rtthread_2M.img" 3 0 "./Bin/version.txt" 100000 10100
# "$WM_TOOLS/makeimg" "./Bin/rtthread.bin.gz" "./Bin/rtthread_GZ_2M.img" 3 1 "./Bin/version.txt" 100000 10100 "./Bin/rtthread.bin"
# "$WM_TOOLS/makeimg" "./Bin/rtthread.bin" "./Bin/rtthread_SEC_2M.img" 3 0 "./Bin/version.txt" 100000 10100
# "$WM_TOOLS/makeimg_all" "./Bin/secboot.img" "./Bin/rtthread_2M.img" "./Bin/rtthread_2M.FLS"

help_title = '为w600生成刷机包'


def main(argv):
    if not isfile(BIN_FILE):
        die(f"application not compiled. (missing {BIN_FILE})")

    if not isfile(VERSION_FILE):
        print(f'version file did not exists, create one with v0.0.0. ({VERSION_FILE})')
        f = open(VERSION_FILE, 'wt')
        f.write('0.0.0')
        f.close()

    runMakeImg = load_wm_module('makeimg').main
    runMakeImgFls = load_wm_module('makeimg_fls').main

    python_pass([tools_path('wm_gzip.py'), BIN_FILE])

    eval_pass(runMakeImg, [BIN_FILE + '.gz', IMG_FILE, '0', '1', VERSION_FILE, '90000', '10100', BIN_FILE])
    print()
    eval_pass(runMakeImgFls, [tools_path('secboot.img'), IMG_FILE, FLS_FILE])
    print()

    with open(IMG_FILE + '.md5', 'rt+' if isfile(IMG_FILE + '.md5') else 'wt+') as f:
        f.seek(0)
        old_hash = f.read().strip()
        new_hash = md5_file(IMG_FILE)
        print("Output file hash: %s" % (new_hash))
        if old_hash != new_hash:
            f.seek(0)
            f.truncate()
            f.write(new_hash)
            f.flush()
            if isfile(FLASH_SIGNAL):
                remove(FLASH_SIGNAL)

    print("Done.")
