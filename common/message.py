"""message.py
"""

import ctypes
import struct

MESSAGE_TYPE_TOKEN = 1    # agent -> proxy

MESSAGE_TYPE_TESTBED_LIST = 1001    # proxy -> agent
MESSAGE_TYPE_TESTBED_DELETE = 1002   # proxy -> agent
MESSAGE_TYPE_TESTBED_RENEW = 1003    # proxy -> agent

MESSAGE_TYPE_TESTBED_LIST_ACK = 2001 # agent -> proxt



class MsgHeader(ctypes.BigEndianStructure):
    """MsgHeader Class
    """
    _fields_ = [("type", ctypes.c_uint16),
                ("length", ctypes.c_uint16)]
    _pack_ = 1




class ProxyMsg(object):
    """ProxyMsg
    """
    def __init__(self, msgtype, msgbody):
        self.type = msgtype
        if msgbody:
            self.length = len(msgbody) + ctypes.sizeof(MsgHeader)
        else:
            self.length = ctypes.sizeof(MsgHeader)
        self.body = msgbody

    def str(self):
        """str
        """
        if self.body:
            return struct.pack('!HH', self.type, self.length) + self.body
        else:
            return struct.pack('!HH', self.type, self.length)

    @classmethod
    def get_topo_id(cls, val):
        """ get_topo_id
        """
        e_str = str(chr(0))
        e_pos = val.find(e_str)
        if e_pos == -1:
            return val
        else:
            return val[: e_pos]


class TopologyInfo(ctypes.BigEndianStructure):
    """MsgHeader Class
    """
    _fields_ = [("expiry", ctypes.c_uint64),
                ("topologid", ctypes.c_uint8 * 10)]
    _pack_ = 1

    MAX_TESTBED_NAME_LEN = 10
    TESTBED_NAME_FMT = "!Q" + str(MAX_TESTBED_NAME_LEN) + 's'

    @classmethod
    def get_topoinfo_size(cls):
        """get_topoinfo_size
        """
        return ctypes.sizeof(TopologyInfo)
