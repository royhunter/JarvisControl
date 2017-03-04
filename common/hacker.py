"""hacker.py
"""

import cookielib
import urllib
import urllib2



class JarvisHacker(object):
    """JarvisHacker
    """
    PAGE_VDNET = "https://vdnet.eng.vmware.com/jarvis/"
    PAGE_HOME = PAGE_VDNET + "topologies.html"
    PAGE_LOGIN = PAGE_VDNET + "php/login.php"
    PAGE_TESTBED_LIST = PAGE_VDNET + "php/testbed.php"
    PAGE_TESTBED_DELETE = PAGE_VDNET + "php/delete_testbed.php"
    PAGE_TESTBED_RENEW = PAGE_VDNET + "php/renew_lease.php"

    def __init__(self, username, passwd):
        self.username = username
        self.password = passwd
        self.opener = None

    def jarvis_login(self):
        """ jarvis_login
            if success reply: {"success":true,"username":"xxx"}
        """
        login_data = urllib.urlencode({'username':self.username,
                                       'password':self.password})

        cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        self.opener = urllib2.build_opener(handler)
        req = urllib2.Request(url=JarvisHacker.PAGE_LOGIN, data=login_data)
        response = self.opener.open(req)
        result = response.read()
        print result

    def jarvis_testbed_list(self):
        """jarvis_testbed_list
        """
        self.jarvis_login()
        response = self.opener.open(JarvisHacker.PAGE_TESTBED_LIST).read()
        return response

    def jarvis_testbed_delete(self, tbname):
        """jarvis_testbed_delete
        """
        self.jarvis_login()
        delete_data = urllib.urlencode({'id':tbname, 'user':self.username})
        req = urllib2.Request(url=JarvisHacker.PAGE_TESTBED_DELETE, data=delete_data)
        response = self.opener.open(req)
        result = response.read()
        print result

    def jarvis_testbed_renew(self, tbname):
        """jarvis_testbed_renew
        """
        self.jarvis_login()
        renew_data = urllib.urlencode({'id':tbname})
        req = urllib2.Request(url=JarvisHacker.PAGE_TESTBED_DELETE, data=renew_data)
        response = self.opener.open(req)
        result = response.read()
        print result
