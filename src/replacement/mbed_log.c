#include <mbedtls/ssl.h>

void __wrap_mbedtls_ssl_config_init(mbedtls_ssl_config *conf);
void __real_mbedtls_ssl_config_init(mbedtls_ssl_config *conf);

static void mbed_ssl_output(void *nil, int lvl, const char *file, int line, const char *msg)
{
	if (lvl > 3)
		return;

	static int last_l = -1;

	if (last_l != line)
	{
		last_l = line;
		rt_kprintf("[mbed][%d] %s:%d\n", lvl, file, line);
	}
	rt_kputs("  ");
	rt_kputs(msg);
}

void __wrap_mbedtls_ssl_config_init(mbedtls_ssl_config *conf)
{
	__real_mbedtls_ssl_config_init(conf);
	mbedtls_ssl_conf_dbg(conf, mbed_ssl_output, NULL);
}
