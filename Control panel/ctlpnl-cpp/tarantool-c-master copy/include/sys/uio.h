
#pragma once

#ifdef __linux__
#include <sys/uio.h>
#else
typedef char *          __kernel_caddr_t;
typedef __kernel_caddr_t        caddr_t;
struct iovec {
    caddr_t	iov_base;
    int	iov_len;
};
#endif
