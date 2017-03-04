#!/usr/bin/python
"""proxy.py
"""
import asyncore
import ctypes
import socket
import struct
import threading
import time

from common import config, fish, httpd, message, url


class ProxyHandler(asyncore.dispatcher):
    """ProxyHandler
    """
    def __init__(self, sock, addr, fisher):
        asyncore.dispatcher.__init__(self, sock)
        self.sock = sock
        self.addr = addr
        self.token = 0
        self.fisher = fisher

    def handle_read(self):
        """handle_read
        """
        print 'handle_read'
        msgheader = self.recv(ctypes.sizeof(message.MsgHeader))
        if msgheader:
            msgtype, msglen = struct.unpack('!HH', msgheader)
            msgbody = None
            if msglen > ctypes.sizeof(message.MsgHeader):
                msgbody = self.recv(msglen - ctypes.sizeof(message.MsgHeader))
            self.proxy_msg_dispatcher(msgtype, msgbody)
        else:
            print 'no data'

    def writable(self):
        pass

    def handle_write(self):
        pass

    def handle_close(self):
        print str(self.token) + ' handle_close'
        self.fisher.tokenmap_delete(self.token)
        self.close()

    def proxy_msg_dispatcher(self, msgtype, msgbody):
        """proxy_msg_dispatcher
        """
        print "proxy_msg_dispatcher"
        if msgtype == message.MESSAGE_TYPE_TOKEN:
            self.token, = struct.unpack('!L', msgbody)
            print self.token
            self.fisher.tokensockmap_insert(self.token, self.sock)
            self.fisher.tokenaddrmap_insert(self.token, repr(self.addr))
            self.fisher.tokenmap_show()
            self.fisher.testbed_list_request(self)
        elif msgtype == message.MESSAGE_TYPE_TESTBED_LIST_ACK:
            if len(msgbody) == 0:
                print 'no topo'
            else:
                print len(msgbody)
                id_num = len(msgbody)/message.TopologyInfo.get_topoinfo_size()
                print id_num
                for i in range(id_num):
                    start = i * message.TopologyInfo.get_topoinfo_size()
                    end = start + message.TopologyInfo.get_topoinfo_size()
                    expiry, topo_value = struct.unpack(message.TopologyInfo.TESTBED_NAME_FMT,
                                                       msgbody[start:end])
                    topoid = message.ProxyMsg.get_topo_id(topo_value)
                    print expiry, topoid


    def send(self, msg):
        """send
        """
        self.sock.send(msg)


class ProxyServer(asyncore.dispatcher):
    """ProxyServer
    """
    def __init__(self, host, port, fisher):
        asyncore.dispatcher.__init__(self)
        self.fisher = fisher
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = ProxyHandler(sock, addr, self.fisher)

    def handle_close(self):
        self.close()


class Proxy(object):
    """Proxy Class
    """
    def __init__(self):
        self.server = None
        self.fisher = fish.Fisher()
        self.urlhandle = httpd.ProxyUrlHandle()
        self.proxyserver_thread = threading.Thread(target=self.backend_server_thread)
        self.httpserver_thread = threading.Thread(target=self.httpd_thread)

    def httpd_thread(self):
        """httpdThread
        """
        self.urlhandle.url_get_mapping_register('/', url.root_get)
        self.urlhandle.url_get_mapping_register('/version', url.version_get)
        self.urlhandle.url_get_mapping_register('/topo', url.topo_get)
        self.urlhandle.url_post_mapping_register('/config', url.config_post)
        proxyhttpd = httpd.HttpServer(config.PROXYHTTPD_PORT, self.fisher, self.urlhandle)
        proxyhttpd.runserver()

    def backend_server_thread(self):
        """backend_server_thread
        """
        self.server = ProxyServer('localhost', config.PROXYSERVER_PORT, self.fisher)
        asyncore.loop()

    def start(self):
        """start
        """
        self.proxyserver_thread.daemon = True
        self.proxyserver_thread.start()
        self.httpserver_thread.daemon = True
        self.httpserver_thread.start()

def proxy_main():
    """proxy_main
    """
    proxy = Proxy()
    proxy.start()
    try:
        while True:
            time.sleep(1)
        print 'main function finished'
    except KeyboardInterrupt:
        print '^C received, shutting down the web server'

if __name__ == "__main__":
    proxy_main()
