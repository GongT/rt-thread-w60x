#include <rtthread.h>
#include <stdio.h>

extern void __wrap_rt_show_version();
extern void __real_rt_show_version();

void __wrap_rt_show_version()
{
	rt_kprintf("\r\x1B"
			   "c");

	__real_rt_show_version();
}
