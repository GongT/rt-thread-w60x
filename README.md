# W600 RT-Thread 工具集（用vscode编程）

## 使用

0. 安装系统级依赖（只需要一次）
	* 系统包：python3（+pip）、串口驱动
	* 第三方：arm gcc（在[这里](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)下载）
	* python：`pip install --user pyserial xmodem PyPrind json5 scons`
	* `rt-thread`源码：
		1. 运行`python control.py rtt update`
		1. [GitHub](https://github.com/RT-Thread/rt-thread)或[码云](https://gitee.com/rtthread/rt-thread)，通过`git clone`或下载zip包都可以，版本至少4.x


1. 找一个放源码的目录
	```bash
	cd ~/Workspace/w600 # 随便找个地方

	git init my-new-project # 随便起个名
	cd my-new-project
	```

1. 下载工具集
	```bash
	git submodule add https://github.com/GongT/rt-thread-w60x.git
	```

1. 初始化项目
	```bash
	python3 rt-thread-w60x/install.py
	```

1. 修改配置（位于.vscode/settings.json）
	* RTT_EXEC_PATH：`arm gcc`的路径（到bin文件夹）。
	* RTT_ROOT：`rt-thread`源码路径，指向它的根目录
	* BUILD_ENV：设为`debug`则编译时使用`-O0`，其他任何内容都会使用`-O2`
	* serialPortNumber：当执行刷写等串口命令时，使用哪个串口，填一数字，如COM1、/dev/ttyUSB1都填“1”



## 命令
```bash
./control.py --help
./control.py <命令> [...参数]
```
