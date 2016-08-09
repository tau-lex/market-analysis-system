//
// Created by aleksey on 07.08.2016.
//


#include <iostream.h>
#include <stdlib.h>
#include <stdio.h>
#include <chrono>
#include <thread>

#include <tarantool/tarantool.h>
#include <tarantool/tnt_net.h>
#include <tarantool/tnt_opt.h>

#ifdef __cplusplus
extern "C" {
#endif

#define CALL_MODE _cdecl

typedef struct tnt_stream *(CALL_MODE *tnt_net_Type)(struct tnt_stream *s);
typedef int (CALL_MODE *tnt_set_Type)(struct tnt_stream *s, int opt, ...);
typedef int (CALL_MODE *tnt_connect_Type)(struct tnt_stream *s);
typedef ssize_t (CALL_MODE *tnt_ping_Type)(struct tnt_stream *s);
typedef struct tnt_reply *(CALL_MODE *tnt_reply_init_Type)(struct tnt_reply *r);
typedef void (CALL_MODE *tnt_reply_free_Type)(struct tnt_reply *r);
typedef void (CALL_MODE *tnt_close_Type)(struct tnt_stream *s);
typedef void (CALL_MODE *tnt_stream_free_Type)(struct tnt_stream *s);

#ifdef __cplusplus
}
#endif

bool dll_test() {
    HINSTANCE hGetProcIDDLL = LoadLibrary("libtarantool.dll");
    if (!hGetProcIDDLL) {
        std::cout << "could not load the dynamic library" << std::endl;
        return false;
    }

    tnt_net_Type tnt_net = (tnt_net_Type)GetProcAddress(hGetProcIDDLL, "tnt_net");
    tnt_set_Type tnt_set = (tnt_set_Type)GetProcAddress(hGetProcIDDLL, "tnt_set");
    tnt_connect_Type tnt_connect = (tnt_connect_Type)GetProcAddress(hGetProcIDDLL, "tnt_connect");
    tnt_ping_Type tnt_ping = (tnt_ping_Type)GetProcAddress(hGetProcIDDLL, "tnt_ping");
    tnt_reply_init_Type tnt_reply_init = (tnt_reply_init_Type)GetProcAddress(hGetProcIDDLL, "tnt_reply_init");
    tnt_reply_free_Type tnt_reply_free = (tnt_reply_free_Type)GetProcAddress(hGetProcIDDLL, "tnt_reply_free");
    tnt_close_Type tnt_close = (tnt_close_Type)GetProcAddress(hGetProcIDDLL, "tnt_close");
    tnt_stream_free_Type tnt_stream_free = (tnt_stream_free_Type)GetProcAddress(hGetProcIDDLL, "tnt_stream_free");

    const char * uri = "192.168.0.11:3301";
    struct tnt_stream * tnt = tnt_net(NULL); // Allocating stream
    tnt_set(tnt, TNT_OPT_URI, uri); // Setting URI
    tnt_set(tnt, TNT_OPT_SEND_BUF, 0); // Disable buffering for send
    tnt_set(tnt, TNT_OPT_RECV_BUF, 0); // Disable buffering for recv
    int res = tnt_connect(tnt); // Initialize stream and connect to Tarantool
    tnt_ping(tnt); // Send ping request
    struct tnt_reply * reply = tnt_reply_init(NULL); // Initialize reply
    tnt->read_reply(tnt, reply); // Read reply from server
    tnt_reply_free(reply); // Free reply
    tnt_close(tnt); tnt_stream_free(tnt); // Close connection and free stream object

    FreeLibrary(hGetProcIDDLL);
    return true;
}

int main() {
    dll_test();
    return EXIT_SUCCESS;
}