#include <rtthread.h>
#include <rt-thread-w60x/internal-flash.h>

#ifdef RT_DEBUG_COLOR
#define __RT_DEBUG_COLOR_DIM "\x1B[2m"
#define __RT_DEBUG_COLOR_RESET "\x1B[0m"
#else
#define __RT_DEBUG_COLOR_DIM
#define __RT_DEBUG_COLOR_RESET
#endif

void print_internal_flash_map()
{
	rt_kprintf(__RT_DEBUG_COLOR_DIM "Internal Flash Map:\n");
	rt_kprintf("Basic: start=0x%X end=0x%X\n", FLASH_BASE_ADDR, FLASH_1M_END_ADDR);
	rt_kprintf("       end=0x%X\n", TLS_FLASH_END_ADDR);
	rt_kprintf("Program header: address=0x%X len=%d\n", CODE_RUN_HEADER_ADDR, CODE_RUN_HEADER_AREA_LEN);
	rt_kprintf("Program code  : address=0x%X len=%d\n", CODE_RUN_START_ADDR, CODE_RUN_AREA_LEN);
	rt_kprintf("Update header: address=0x%X len=%d\n", CODE_UPD_HEADER_ADDR, TLS_FLASH_PARAM1_ADDR - CODE_UPD_HEADER_ADDR);
	rt_kprintf("Update code  : address=0x%X len=%d\n", CODE_UPD_START_ADDR, CODE_UPD_AREA_LEN);
	rt_kprintf("User area: address=0x%X len=%d end=0x%X\n", USER_ADDR_START, USER_AREA_LEN, USER_ADDR_END);
	rt_kprintf("Params:\n");
	rt_kprintf("  default=0x%X\n", TLS_FLASH_PARAM_DEFAULT);
	rt_kprintf("  1      =0x%X\n", TLS_FLASH_PARAM1_ADDR);
	rt_kprintf("  2      =0x%X\n", TLS_FLASH_PARAM2_ADDR);
	rt_kprintf("  restore=0x%X"__RT_DEBUG_COLOR_RESET
			   "\n",
			   TLS_FLASH_PARAM_RESTORE_ADDR);
}
