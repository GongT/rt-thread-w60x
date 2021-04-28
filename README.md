# W600 RT-Thread 工具集（用vscode编程）

## 使用
1. 找一个放源码的目录
	```bash
	mkdir ~/Workspace/w600/my-new-project
	cd ~/Workspace/w600/my-new-project
	```

1. 下载工具集
	```bash
	git clone https://github.com/GongT/rt-thread-w60x.git
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

　

0. 安装系统级依赖（只需要一次）
	* 系统包：python3、scons、串口驱动
	* 第三方：arm gcc（在[这里](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)下载）
	* python：`pip install -r requirements.txt --user`（或者其他安装方法）
	* `rt-thread`源码：[GitHub](https://github.com/RT-Thread/rt-thread)或[码云](https://gitee.com/rtthread/rt-thread)，通过`git clone`或下载zip包都可以，版本至少4.x

## 命令
```bash
python3 control.py <命令> [...参数]
```

1.
