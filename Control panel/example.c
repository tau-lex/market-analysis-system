#include <stdlib.h>
#include <stdio.h>

#include <tarantool/tarantool.h>
#include <tarantool/tnt_net.h>
#include <tarantool/tnt_opt.h>

int main() {
    const char * uri = "localhost:3301";
    struct tnt_stream * tnt = tnt_net(NULL); // Allocating stream
    tnt_set(tnt, TNT_OPT_URI, uri); // Setting URI
    tnt_set(tnt, TNT_OPT_SEND_BUF, 0); // Disable buffering for send
    tnt_set(tnt, TNT_OPT_RECV_BUF, 0); // Disable buffering for recv
    tnt_connect(tnt); // Initialize stream and connect to Tarantool
    tnt_ping(tnt); // Send ping request
    struct tnt_reply * reply = tnt_reply_init(NULL); // Initialize reply
    tnt->read_reply(tnt, reply); // Read reply from server
    tnt_reply_free(reply); // Free reply
    tnt_close(tnt); tnt_stream_free(tnt); // Close connection and free stream object
}