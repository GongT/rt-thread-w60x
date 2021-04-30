#pragma once

#if !defined(DBG_TAG) && !defined(DBG_SECTION_NAME)
#warning "此文件没有定义C语言常量DBG_TAG或DBG_SECTION_NAME，默认为unknown"
#define DBG_TAG "main"
#endif

#ifndef DBG_LVL
#define DBG_LVL DBG_LOG
#endif
#include <rtdbg.h>

#include <rtthread.h>
#include <rtdevice.h>
