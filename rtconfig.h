#ifndef RT_CONFIG_H__
#define RT_CONFIG_H__

/* Automatically generated file; DO NOT EDIT. */
/* RT-Thread Configuration */

/* RT-Thread Kernel */

#define RT_NAME_MAX 8
#define RT_ALIGN_SIZE 4
#define RT_THREAD_PRIORITY_32
#define RT_THREAD_PRIORITY_MAX 32
#define RT_TICK_PER_SECOND 1000
#define RT_USING_OVERFLOW_CHECK
#define RT_USING_HOOK
#define RT_USING_IDLE_HOOK
#define RT_IDLE_HOOK_LIST_SIZE 4
#define IDLE_THREAD_STACK_SIZE 256
#define RT_USING_TIMER_SOFT
#define RT_TIMER_THREAD_PRIO 4
#define RT_TIMER_THREAD_STACK_SIZE 512
#define RT_DEBUG
#define RT_DEBUG_COLOR

/* Inter-Thread communication */

#define RT_USING_SEMAPHORE
#define RT_USING_MUTEX
#define RT_USING_EVENT
#define RT_USING_MAILBOX
#define RT_USING_MESSAGEQUEUE

/* Memory Management */

#define RT_USING_MEMPOOL
#define RT_USING_SMALL_MEM
#define RT_USING_HEAP

/* Kernel Device Object */

#define RT_USING_DEVICE
#define RT_USING_CONSOLE
#define RT_CONSOLEBUF_SIZE 128
#define RT_CONSOLE_DEVICE_NAME "uart0"
#define RT_VER_NUM 0x40003

/* RT-Thread Components */

#define RT_USING_COMPONENTS_INIT
#define RT_USING_USER_MAIN
#define RT_MAIN_THREAD_STACK_SIZE 2048
#define RT_MAIN_THREAD_PRIORITY 10

/* C++ features */


/* Command shell */


/* Device virtual file system */

#define RT_USING_DFS
#define DFS_FILESYSTEMS_MAX 4
#define DFS_FILESYSTEM_TYPES_MAX 4
#define DFS_FD_MAX 16
#define RT_USING_DFS_DEVFS

/* Device Drivers */

#define RT_USING_DEVICE_IPC
#define RT_PIPE_BUFSZ 512
#define RT_USING_SYSTEM_WORKQUEUE
#define RT_SYSTEM_WORKQUEUE_STACKSIZE 2048
#define RT_SYSTEM_WORKQUEUE_PRIORITY 23
#define RT_USING_SERIAL
#define RT_SERIAL_USING_DMA
#define RT_SERIAL_RB_BUFSZ 128
#define RT_USING_HWTIMER
#define RT_USING_PIN
#define RT_USING_RTC
#define RT_USING_SOFT_RTC
#define RT_USING_WDT
#define RT_USING_HWCRYPTO
#define RT_HWCRYPTO_DEFAULT_NAME "hwcryto"
#define RT_HWCRYPTO_IV_MAX_SIZE 16
#define RT_HWCRYPTO_KEYBIT_MAX_SIZE 256
#define RT_HWCRYPTO_USING_AES
#define RT_HWCRYPTO_USING_AES_ECB
#define RT_HWCRYPTO_USING_AES_CBC
#define RT_HWCRYPTO_USING_MD5
#define RT_HWCRYPTO_USING_SHA1
#define RT_HWCRYPTO_USING_RNG
#define RT_HWCRYPTO_USING_CRC
#define RT_HWCRYPTO_USING_CRC_07
#define RT_HWCRYPTO_USING_CRC_8005
#define RT_HWCRYPTO_USING_CRC_1021
#define RT_HWCRYPTO_USING_CRC_04C11DB7
#define RT_HWCRYPTO_USING_BIGNUM
#define RT_HWCRYPTO_USING_BIGNUM_EXPTMOD
#define RT_HWCRYPTO_USING_BIGNUM_MULMOD
#define RT_USING_WIFI
#define RT_WLAN_DEVICE_STA_NAME "wlan0"
#define RT_WLAN_DEVICE_AP_NAME "wlan1"
#define RT_WLAN_SSID_MAX_LENGTH 32
#define RT_WLAN_PASSWORD_MAX_LENGTH 32
#define RT_WLAN_DEV_EVENT_NUM 2
#define RT_WLAN_MANAGE_ENABLE
#define RT_WLAN_SCAN_WAIT_MS 10000
#define RT_WLAN_CONNECT_WAIT_MS 10000
#define RT_WLAN_MSH_CMD_ENABLE
#define RT_WLAN_PROT_ENABLE
#define RT_WLAN_PROT_NAME_LEN 8
#define RT_WLAN_PROT_MAX 2
#define RT_WLAN_DEFAULT_PROT "lwip"
#define RT_WLAN_PROT_LWIP_ENABLE
#define RT_WLAN_PROT_LWIP_NAME "lwip"
#define RT_WLAN_WORK_THREAD_ENABLE
#define RT_WLAN_WORKQUEUE_THREAD_NAME "wlan_job"
#define RT_WLAN_WORKQUEUE_THREAD_SIZE 2048
#define RT_WLAN_WORKQUEUE_THREAD_PRIO 22

/* Using USB */


/* POSIX layer and C standard library */

#define RT_USING_LIBC
#define RT_USING_POSIX

/* Network */

/* Socket abstraction layer */

#define RT_USING_SAL
#define SAL_INTERNET_CHECK

/* protocol stack implement */

#define SAL_USING_LWIP
#define SAL_USING_POSIX

/* Network interface device */

#define RT_USING_NETDEV
#define NETDEV_USING_IFCONFIG
#define NETDEV_USING_PING
#define NETDEV_USING_NETSTAT
#define NETDEV_USING_AUTO_DEFAULT
#define NETDEV_IPV4 1
#define NETDEV_IPV6 0

/* light weight TCP/IP stack */

#define RT_USING_LWIP
#define RT_USING_LWIP202
#define RT_LWIP_MEM_ALIGNMENT 4
#define RT_LWIP_IGMP
#define RT_LWIP_ICMP
#define RT_LWIP_DNS
#define RT_LWIP_DHCP
#define IP_SOF_BROADCAST 1
#define IP_SOF_BROADCAST_RECV 1

/* Static IPv4 Address */

#define RT_LWIP_IPADDR "192.168.1.1"
#define RT_LWIP_GWADDR "192.168.1.1"
#define RT_LWIP_MSKADDR "255.255.255.0"
#define RT_LWIP_UDP
#define RT_LWIP_TCP
#define RT_LWIP_RAW
#define RT_MEMP_NUM_NETCONN 8
#define RT_LWIP_PBUF_NUM 16
#define RT_LWIP_RAW_PCB_NUM 10
#define RT_LWIP_UDP_PCB_NUM 10
#define RT_LWIP_TCP_PCB_NUM 10
#define RT_LWIP_TCP_SEG_NUM 40
#define RT_LWIP_TCP_SND_BUF 10240
#define RT_LWIP_TCP_WND 10240
#define RT_LWIP_TCPTHREAD_PRIORITY 10
#define RT_LWIP_TCPTHREAD_MBOX_SIZE 8
#define RT_LWIP_TCPTHREAD_STACKSIZE 1024
#define LWIP_NO_RX_THREAD
#define LWIP_NO_TX_THREAD
#define RT_LWIP_ETHTHREAD_PRIORITY 12
#define RT_LWIP_ETHTHREAD_STACKSIZE 1024
#define RT_LWIP_ETHTHREAD_MBOX_SIZE 8
#define LWIP_NETIF_STATUS_CALLBACK 1
#define LWIP_NETIF_LINK_CALLBACK 1
#define SO_REUSE 1
#define LWIP_SO_RCVTIMEO 1
#define LWIP_SO_SNDTIMEO 1
#define LWIP_SO_RCVBUF 1
#define LWIP_SO_LINGER 0
#define LWIP_NETIF_LOOPBACK 0
#define RT_LWIP_USING_HW_CHECKSUM
#define RT_LWIP_USING_PING
#define RT_LWIP_DEBUG

/* AT commands */

#define LWIP_USING_DHCPD
#define DHCPD_SERVER_IP "192.168.1.1"
#define DHCPD_USING_ROUTER

/* VBUS(Virtual Software BUS) */


/* Utilities */

#define RT_USING_ULOG
#define ULOG_OUTPUT_LVL_I
#define ULOG_OUTPUT_LVL 6
#define ULOG_USING_ISR_LOG
#define ULOG_ASSERT_ENABLE
#define ULOG_LINE_BUF_SIZE 128

/* log format */

#define ULOG_USING_COLOR
#define ULOG_OUTPUT_TIME
#define ULOG_OUTPUT_LEVEL
#define ULOG_OUTPUT_TAG
#define ULOG_BACKEND_USING_CONSOLE

/* RT-Thread online packages */

/* IoT - internet of things */


/* Wi-Fi */

/* Marvell WiFi */


/* Wiced WiFi */

#define PKG_USING_NETUTILS
#define PKG_NETUTILS_NTP
#define NETUTILS_NTP_TIMEZONE 8
#define NETUTILS_NTP_HOSTNAME "cn.ntp.org.cn"
#define NETUTILS_NTP_HOSTNAME2 "ntp.rt-thread.org"
#define NETUTILS_NTP_HOSTNAME3 "edu.ntp.org.cn"
#define PKG_USING_NETUTILS_LATEST_VERSION

/* IoT Cloud */


/* security packages */


/* language packages */


/* multimedia packages */


/* tools packages */

#define PKG_USING_EASYFLASH
#define PKG_EASYFLASH_ENV
#define PKG_EASYFLASH_ERASE_GRAN 4096
#define PKG_EASYFLASH_WRITE_GRAN_1BIT
#define PKG_EASYFLASH_WRITE_GRAN 1
#define PKG_EASYFLASH_START_ADDR 0
#define PKG_EASYFLASH_DEBUG
#define PKG_USING_EASYFLASH_V410
#define PKG_EASYFLASH_VER_NUM 0x40100

/* system packages */

#define PKG_USING_FAL
#define FAL_DEBUG_CONFIG
#define FAL_DEBUG 1
#define FAL_PART_HAS_TABLE_CFG
#define PKG_USING_FAL_V00500
#define PKG_FAL_VER_NUM 0x00500

/* Micrium: Micrium software products porting for RT-Thread */


/* peripheral libraries and drivers */

#define PKG_USING_WM_LIBRARIES
#define PKG_USING_WM_LIBRARIES_LATEST_VERSION
#define PKG_USING_AGILE_BUTTON
#define PKG_AGILE_BUTTON_DEBUG
#define PKG_AGILE_BUTTON_THREAD_STACK_SIZE 256
#define PKG_AGILE_BUTTON_THREAD_PRIORITY 28
#define PKG_AGILE_BUTTON_USING_EXAMPLE
#define PKG_USING_AGILE_BUTTON_LATEST_VERSION
#define PKG_USING_AGILE_LED
#define PKG_AGILE_LED_DEBUG
#define PKG_AGILE_LED_THREAD_STACK_SIZE 256
#define PKG_AGILE_LED_THREAD_PRIORITY 28
#define PKG_AGILE_LED_USING_EXAMPLE
#define PKG_USING_AGILE_LED_LATEST_VERSION

/* AI packages */


/* miscellaneous packages */


/* samples: kernel and components samples */


/* entertainment: terminal games and other interesting software packages */


/* Env config */

#define SYS_AUTO_UPDATE_PKGS
#define SYS_PKGS_DOWNLOAD_ACCELERATE
#define BSP_USING_WM_LIBRARIES

/* W60x Device config */

#define SOC_W600_A8xx
#define W60X_CUSTOM_BOARD

/* On-chip Peripheral Drivers */

#define BSP_USING_UART
#define BSP_USING_UART0
#define BSP_USING_PIN
#define BSP_USING_WIFI
#define BSP_USING_CRYPTO

/* External Libraries */

#define SOC_W60X
#include "rtconfig_project.h"

#endif
