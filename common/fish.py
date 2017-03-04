"""fish.py
"""
import json

from . import message


class Fisher(object):
    """Fisher Class
    """
    def __init__(self):
        """Init object
        """
        self.tokensockmap = {}
        self.tokenaddrmap = {}

    def tokensockmap_insert(self, token, sock):
        """TokenSockMapInsert
        """
        self.tokensockmap[token] = sock

    def tokenaddrmap_insert(self, token, addr):
        """TokenAddrMapInsert
        """
        self.tokenaddrmap[token] = addr

    def tokenmap_delete(self, token):
        """token_delete
        """
        del self.tokensockmap[token]
        del self.tokenaddrmap[token]

    def tokenmap_show(self):
        """tokenmap_show
        """
        print self.tokensockmap
        print self.tokenaddrmap

    def testbed_list_request(self, proxyhandle):
        """testbed_list_request
        """
        print "testbed_list_request"
        msg = message.ProxyMsg(message.MESSAGE_TYPE_TESTBED_LIST, None)
        proxyhandle.send(msg.str())

    def topo_get(self, httphandle):
        """topo_get
        """
        httphandle.reply_ok(httphandle.path)

    def version_get(self, httphandle):
        """version_get
        """
        httphandle.reply_ok(httphandle.path)

    def root_get(self, httphandle):
        """root_get
        """
        print self.tokenaddrmap
        json_str = json.dumps(self.tokenaddrmap)
        httphandle.reply_ok(json_str)

    def config_post(self, httphandle):
        """config_post
        """
        print "config_post"
        content_len = int(httphandle.headers.getheader('content-length', 0))
        content = httphandle.rfile.read(content_len)
        print content
        self.config_json_parser(content)
        httphandle.reply_ok(content)

    def config_json_parser(self, json_string):
        """config_json_parser
        """
        print "config_json_parser"
        json_obj = json.loads(json_string)
        print json_obj
