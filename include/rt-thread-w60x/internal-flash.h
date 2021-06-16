#pragma once

#ifndef INSIDE_FLS_BLOCK_SIZE
#define INSIDE_FLS_BLOCK_SIZE (0x10000UL)
#define INSIDE_FLS_SECTOR_SIZE (0x1000UL)
#define INSIDE_FLS_PAGE_SIZE 256 // (0x100UL)
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

extern struct fal_flash_dev w60x_onchip;

#define W60X_INTFLS_PART_FAL_PART(name, start, size)                               \
	{                                                                              \
		FAL_PART_MAGIC_WROD, name, "w60x_onchip", start - FLASH_BASE_ADDR, size, 0 \
	}

#define W60X_INTFLS_PART_PAGE(name, start) W60X_INTFLS_PART_FAL_PART(name, start, INSIDE_FLS_PAGE_SIZE)
#define W60X_INTFLS_PART_SECTOR(name, start) W60X_INTFLS_PART_FAL_PART(name, start, INSIDE_FLS_SECTOR_SIZE)

#define W600_INTERNAL_FLASH_PARTITION_TABLE W60X_INTFLS_PART_SECTOR("param_phy", TLS_PHY_PARAM_ADDR),                                      \
											W60X_INTFLS_PART_SECTOR("param_flash", TLS_QFLASH_PARAM_ADDR),                                 \
											W60X_INTFLS_PART_PAGE("secboot_hdr", SECBOOT_HEADER_ADDR),                                     \
											W60X_INTFLS_PART_FAL_PART("secboot", SECBOOT_ADDR, SECBOOT_AREA_LEN),                          \
											W60X_INTFLS_PART_PAGE("code_header", CODE_RUN_HEADER_ADDR),                                    \
											W60X_INTFLS_PART_FAL_PART("code", CODE_RUN_START_ADDR, CODE_RUN_AREA_LEN),                     \
											W60X_INTFLS_PART_FAL_PART(FAL_PARTITION_UPDATE_IMAGE, CODE_UPD_START_ADDR, CODE_UPD_AREA_LEN), \
											W60X_INTFLS_PART_FAL_PART(FAL_PARTITION_STORAGE, USER_ADDR_START, USER_AREA_LEN),              \
											W60X_INTFLS_PART_PAGE(FAL_PARTITION_UPDATE_IMAGE "_header", CODE_UPD_HEADER_ADDR),             \
											W60X_INTFLS_PART_SECTOR("param_1", TLS_FLASH_PARAM1_ADDR),                                     \
											W60X_INTFLS_PART_SECTOR("param_2", TLS_FLASH_PARAM2_ADDR),                                     \
											W60X_INTFLS_PART_SECTOR("param_res", TLS_FLASH_PARAM_RESTORE_ADDR)

extern void print_internal_flash_map();
