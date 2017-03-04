#!/usr/bin/python
"""jarvis.py
"""
import asyncore
import ctypes
import json
import socket
import struct

from common import hacker, message

USERNAME = ''
PASSWORD = ''

class JarvisAgent(asyncore.dispatcher):
    """JarvisAgent
    """
    def __init__(self, host, token):
        asyncore.dispatcher.__init__(self)
        self.buffer = None
        self.hacker = hacker.JarvisHacker(USERNAME, PASSWORD)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, 6000))
        self.jarvis_agent_register(token)

    def handle_connect(self):
        """handle_connect
        """
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(ctypes.sizeof(message.MsgHeader))
        msgtype, msglen = struct.unpack('!HH', data)
        if msglen > ctypes.sizeof(message.MsgHeader):
            self.recv(msglen - ctypes.sizeof(message.MsgHeader))
        self.msg_dispatcher(msgtype)

    def writable(self):
        return len(self.buffer) > 0

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def jarvis_agent_register(self, token):
        """registerJarvisAgent
        """
        body = struct.pack("!L", token)
        msg = message.ProxyMsg(message.MESSAGE_TYPE_TOKEN, body)
        self.buffer = msg.str()

    def msg_dispatcher(self, msgtype):
        """msg_dispatcher
        """
        if msgtype == message.MESSAGE_TYPE_TESTBED_RENEW:
            self.jarvis_tb_renew()
        elif msgtype == message.MESSAGE_TYPE_TESTBED_DELETE:
            self.jarvis_tb_delete()

        self.jarvis_tb_list()

    def jarvis_tb_list(self):
        """jarvis_tb_list
        """
        print "jarvisTestbedList"
        #self.hacker.jarvis_login()
        result = self.hacker.jarvis_testbed_list()
        topo_list = self.jarvis_tb_parser(result)
        if topo_list is None:
            msg = message.ProxyMsg(message.MESSAGE_TYPE_TESTBED_LIST_ACK, None)
            self.buffer = msg.str()
        else:
            body = ''
            for topo in topo_list:
                print topo[0]
                print topo[1]
                body = body + struct.pack(message.TopologyInfo.TESTBED_NAME_FMT,
                                          topo[1],
                                          str(topo[0]))
            msg = message.ProxyMsg(message.MESSAGE_TYPE_TESTBED_LIST_ACK, body)
        self.buffer = msg.str()


    def jarvis_tb_renew(self):
        """jarvis_tb_renew
        """
        pass

    def jarvis_tb_delete(self):
        """jarvis_tb_delete
        """
        pass

    def jarvis_tb_parser(self, info):
        """ jarvis_tb_parser
            return [ [id, expiry], [id, expiry]...]
        """
        json_obj = json.loads(info.decode('string-escape').strip('"'))
        if len(json_obj) == 0:
            return None
        topo_list = []
        for topology in json_obj:
            topo = []
            topo.append(topology["id"])
            topo.append(topology["lease_expiry"])
            topo_list.append(topo)
        if len(topo_list) == 0:
            return None

        return topo_list




def jarvis_main():
    """1. username
       2. passwd
       3. token
    """
    jarvis = JarvisAgent('localhost', 132)
    asyncore.loop()

if __name__ == "__main__":
    jarvis_main()
