#pragma once

#include <stdio.h>
#include <string.h>

#define ALWAYS_INLINE __attribute__((always_inline)) inline static

#if defined(RT_DEBUG_COLOR) || defined(MY_DEBUG_COLOR)
#define KPRINTF_COLOR(COLOR, MSG, ...) printf("\r\x1B[38;5;" #COLOR "m" MSG "\x1B[0m\n", ##__VA_ARGS__)
#define KPRINTF_LIGHT(MSG, ...) (printf("\r\x1B[1m" MSG "\x1B[0m\n", ##__VA_ARGS__))
#define KPRINTF_DIM(MSG, ...) (printf("\r\x1B[2m" MSG "\x1B[0m\n", ##__VA_ARGS__))
#define SET_COLOR_RAW(RAW) (puts("\x1B[" RAW "m"))
#else
#define KPRINTF_COLOR(COLOR, MSG, ...) printf(MSG, ##__VA_ARGS__)
#define KPRINTF_LIGHT(COLOR) printf(MSG, ##__VA_ARGS__)
#define KPRINTF_DIM(COLOR) printf(MSG, ##__VA_ARGS__)
#define SET_COLOR_RAW(RAW)
#endif

#define RESET_COLOR() SET_COLOR_RAW("0")
#define SET_COLOR(COLOR) SET_COLOR_RAW("38;5;" #COLOR)
#define SET_BG_COLOR(COLOR) SET_COLOR_RAW("48;5;" #COLOR)
#define SET_COLOR_DIM() SET_COLOR_RAW("2")

__attribute__((noreturn)) void thread_suspend();
void show_context();

#define RT_TICK_FROM_MILLISECOND(ms) (RT_TICK_PER_SECOND * (ms / 1000) + (RT_TICK_PER_SECOND * (ms % 1000) + 999) / 1000)

#define str_prefix(string, find) str_nprefix(string, strlen(find), find)
ALWAYS_INLINE int str_nprefix(const char *string, size_t max_char, const char *find)
{
	return strncmp(string, find, max_char) == 0;
}

ALWAYS_INLINE int str_eq(const char *str, const char *cmp)
{
	return strcmp(str, cmp) == 0;
}

#define assert0(V) assert(V == 0)
#define assertok(V) assert(V == RT_EOK)
