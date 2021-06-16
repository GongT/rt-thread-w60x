#include <rtthread.h>
#include <rt-thread-w60x/helper.h>

extern void list_thread();

void show_context()
{
	SET_COLOR(7);
	rt_thread_t self = rt_thread_self();
	if (self == RT_NULL)
		puts(" * thread context: no.\n");
	else
		printf(" * thread context: [%d] %.*s.\n", self->stat, RT_NAME_MAX, self->name);
#ifdef RT_USING_FINSH
	puts("=================================\n");
	list_thread();
	puts("=================================\n");
#endif
	RESET_COLOR();
}
