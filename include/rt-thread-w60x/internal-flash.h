#pragma once

#ifndef INSIDE_FLS_BLOCK_SIZE
#define INSIDE_FLS_BLOCK_SIZE (0x10000UL)
#define INSIDE_FLS_SECTOR_SIZE (0x1000UL)
#define INSIDE_FLS_PAGE_SIZE (0x100UL)
#endif

#define TLS_PHY_PARAM_ADDR (FLASH_BASE_ADDR)
#define TLS_QFLASH_PARAM_ADDR (TLS_PHY_PARAM_ADDR + INSIDE_FLS_SECTOR_SIZE)
#define SECBOOT_HEADER_ADDR (TLS_QFLASH_PARAM_ADDR + INSIDE_FLS_SECTOR_SIZE)
#define SECBOOT_HEADER_AREA_LEN (INSIDE_FLS_PAGE_SIZE)
#define SECBOOT_ADDR (SECBOOT_HEADER_ADDR + SECBOOT_HEADER_AREA_LEN)
#define SECBOOT_AREA_LEN (CODE_RUN_START_ADDR - SECBOOT_ADDR)

// ### flash settings
#include "wm_flash_map.h"
// ./packages/wm_libraries-latest/Include/Driver/wm_flash_map.h
/**Run-time image area size*/
#define CODE_RUN_AREA_LEN (512 * 1024 - 256)

/**Upgrade image area*/
#define CODE_UPD_START_ADDR (CODE_RUN_START_ADDR + CODE_RUN_AREA_LEN)
#define CODE_UPD_AREA_LEN (384 * 1024)

/**Area can be used by User*/
#define USER_ADDR_START (CODE_UPD_START_ADDR + CODE_UPD_AREA_LEN)
#define TLS_FLASH_PARAM_DEFAULT (USER_ADDR_START)
#define USER_AREA_LEN (48 * 1024)
#define USER_ADDR_END (USER_ADDR_START + USER_AREA_LEN - 1)

/**Upgrade image header area & System parameter area */
#define CODE_UPD_HEADER_ADDR (USER_ADDR_START + USER_AREA_LEN)
#define TLS_FLASH_PARAM1_ADDR (CODE_UPD_HEADER_ADDR + 0x1000)
#define TLS_FLASH_PARAM2_ADDR (TLS_FLASH_PARAM1_ADDR + 0x1000)
#define TLS_FLASH_PARAM_RESTORE_ADDR (TLS_FLASH_PARAM2_ADDR + 0x1000)
#define TLS_FLASH_END_ADDR (TLS_FLASH_PARAM_RESTORE_ADDR + 0x1000 - 1)
// ### flash settings END

#ifdef RT_DEBUG_COLOR
#define __RT_DEBUG_COLOR_DIM "\x1B[2m"
#define __RT_DEBUG_COLOR_RESET "\x1B[0m"
#else
#define __RT_DEBUG_COLOR_DIM
#define __RT_DEBUG_COLOR_RESET
#endif
#define print_internal_flash_map()                                                                                              \
	{                                                                                                                           \
		rt_kprintf(__RT_DEBUG_COLOR_DIM "Internal Flash Map:\n");                                                               \
		rt_kprintf("Basic: start=0x%X end=0x%X\n", FLASH_BASE_ADDR, FLASH_1M_END_ADDR);                                         \
		rt_kprintf("       end=0x%X\n", TLS_FLASH_END_ADDR);                                                                    \
		rt_kprintf("Program header: address=0x%X len=%d\n", CODE_RUN_HEADER_ADDR, CODE_RUN_HEADER_AREA_LEN);                    \
		rt_kprintf("Program code  : address=0x%X len=%d\n", CODE_RUN_START_ADDR, CODE_RUN_AREA_LEN);                            \
		rt_kprintf("Update header: address=0x%X len=%d\n", CODE_UPD_HEADER_ADDR, TLS_FLASH_PARAM1_ADDR - CODE_UPD_HEADER_ADDR); \
		rt_kprintf("Update code  : address=0x%X len=%d\n", CODE_UPD_START_ADDR, CODE_UPD_AREA_LEN);                             \
		rt_kprintf("User area: address=0x%X len=%d end=0x%X\n", USER_ADDR_START, USER_AREA_LEN, USER_ADDR_END);                 \
		rt_kprintf("Params:\n");                                                                                                \
		rt_kprintf("  default=0x%X\n", TLS_FLASH_PARAM_DEFAULT);                                                                \
		rt_kprintf("  1      =0x%X\n", TLS_FLASH_PARAM1_ADDR);                                                                  \
		rt_kprintf("  2      =0x%X\n", TLS_FLASH_PARAM2_ADDR);                                                                  \
		rt_kprintf("  restore=0x%X"__RT_DEBUG_COLOR_RESET                                                                       \
				   "\n",                                                                                                        \
				   TLS_FLASH_PARAM_RESTORE_ADDR);                                                                               \
	}
