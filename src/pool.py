#!/usr/bin/python

'''
pool.py - Maintain HTTP/HTTPS connections
'''

import httplib

import config

http_pool = {}
https_pool = {}

def get_http_connection(host):
    return get_connection_template("http", host)

def get_https_connection(host):
    return get_connection_template("https", host)

'''
Internal helper functions
'''        

def get_connection_template(kind, host):
    global http_pool, https_pool
    
    print "try to get %s connection to %s..." % (kind, host)
    if "kind" == "http":
        f = httplib.HTTPConnection
        pool = http_pool
    elif "kind" == "https":
        f = httplib.HTTPSConnection
        pool = https_pool
        
    if not host in pool:
        # retry several times
        for i in range(config.retry):
            try:
                conn = f(host)
                conn.connect()
                break
            except:
                if i == config.retry:
                    print "...failed, abort to retry"
                    print sys.exc_info()
                else:
                    print "...retry, i=%d" % i
                    continue
            
        print "...create %s connection to %s" % (kind, host)
        pool[host] = conn
    print "...done."
    return pool[host]