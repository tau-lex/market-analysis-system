#ifndef LIBTNT_WINHEADERS_H
#define LIBTNT_WINHEADERS_H

#define WIN32_LEAN_AND_MEAN 1
#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
struct sockaddr_un{
    short                    sun_family;                /*AF_UNIX*/
    char                     sun_path[108];        /*path name */
};

#endif //LIBTNT_WINHEADERS_H
