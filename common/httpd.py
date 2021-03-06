"""http server
"""

import socket
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class ProxyUrlHandle(object):
    """ProxyUrlHandle
    """
    def __init__(self):
        self.url_post_map = {}
        self.url_get_map = {}

    def url_get_mapping_register(self, path, func):
        """url_get_mapping_register
        """
        self.url_get_map[path] = func

    def url_post_mapping_register(self, path, func):
        """url_post_mapping_register
        """
        self.url_post_map[path] = func

    def url_post_handle(self, serverhandle, path, fisher):
        """url_post_handle
        """
        try:
            self.url_post_map[path](fisher, serverhandle)
        except Exception, e:
            print Exception, ":", e
            serverhandle.reply_err()

    def url_get_handle(self, serverhandle, path, fisher):
        """url_get_handle
        """
        try:
            self.url_get_map[path](fisher, serverhandle)
        except Exception, e:
            print Exception, ":", e
            serverhandle.reply_err()





class ProxyHttpSeverHandle(BaseHTTPRequestHandler):
    """ProxyHttpSeverHandle
    """
    def version_handle(self):
        """version_handle
        """
        self.reply_ok('version')

    def config_handle(self):
        """config_handle
        """
        self.reply_ok('config')

    def reply_ok(self, content):
        """reply_ok
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)

    def reply_err(self):
        """reply_err
        """
        self.send_error(404, 'Path Not Found: %s' % self.path)

    def do_GET(self):
        """do_GET
        """
        print 'get url is ' + self.path
        self.server.urlhandle.url_get_handle(self,
                                             self.path,
                                             self.server.fisher)

    def do_POST(self):
        """do_POST
        """
        self.server.urlhandle.url_post_handle(self,
                                              self.path,
                                              self.server.fisher)


class MyHttpServer(HTTPServer):
    """MyHttpServer
    """
    def __init__(self, address, requesthandleclass, fisher, urlhandle):
        HTTPServer.__init__(self, address, requesthandleclass)
        self.fisher = fisher
        self.urlhandle = urlhandle



class HttpServer(object):
    """HttpServer
    """
    def __init__(self, port, fisher, urlhandle):
        self.port = port
        self.fisher = fisher
        self.urlhandle = urlhandle
        self.server = None

    def runserver(self):
        """RunServer
        """
        self.server = MyHttpServer(('', self.port), ProxyHttpSeverHandle,
                                   self.fisher, self.urlhandle)
        print 'Started httpserver on port ', self.port
        self.server.allow_reuse_address = True
        self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.serve_forever()

    def stopserver(self):
        """stopserver
        """
        self.server.server_close()
