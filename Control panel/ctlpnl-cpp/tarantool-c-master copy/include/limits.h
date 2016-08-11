
#pragma once

#ifdef __linux__
#include <limits.h>
#else
#include <limits.h>
#include <stdio.h>
#define _POSIX_PATH_MAX 240
#define IOV_MAX 50
#define LLONG_MAX  9223372036854775807LL
#define LLONG_MIN  (-9223372036854775807LL - 1)
#endif