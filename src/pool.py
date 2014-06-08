#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
pool.py - Maintain HTTP/HTTPS connections
'''

import httplib
import sys

class BasePool(object):
    def __init__(self, name, func, timeout=2, retry=5):
        self.pool = {}
        self.name = name
        self.func = func
        self.timeout = timeout
        self.retry = retry
        
    def get_connection(self, host):
        if self.func is None:
            return None

        if not host in self.pool:
            for i in range(self.retry):
                try:
                    conn = self.func(host, timeout = self.timeout)
                    conn.connect()
                
                    print "...create %s connection to %s" % (self.name, host)
                    self.pool[host] = conn
                    break
                except:
                    print sys.exc_info()
                    if i == self.retry - 1:
                        print "...abort to retry, exit"
                        sys.exit()
                    print "...retry, i=%d" % i
                    continue                    
        print "...done."
        return self.pool[host]

class HttpPool(BasePool):    
    instance = None

    def __init__(self, timeout=2, retry=5):
        super(HttpPool, self).__init__("HTTP", httplib.HTTPConnection, timeout, retry)

    @staticmethod
    def get_instance():
        # FIXME: consider mulit-thread here
        if HttpPool.instance is None:
            HttpPool.instance = HttpPool()
        return HttpPool.instance

class HttpsPool(BasePool):
    instance = None

    def __init__(self, timeout=2, retry=5):
        super(HttpsPool, self).__init__("HTTPS", httplib.HTTPSConnection, timeout, retry)

    @staticmethod
    def get_instance():
        # FIXME: consider mulit-thread here
        if Https.instance is None:
            Https.instance = HttpsPool()
        return Https.instance

# For testing
if __name__ == '__main__':
    pool = HttpPool.get_instance()
    pool.get_connection("www.baidu.com")