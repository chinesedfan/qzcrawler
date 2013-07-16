#!/usr/bin/python

'''
pool.py - Maintain HTTP/HTTPS connections
'''

import httplib

http_pool = {}
https_pool = {}

def get_http_connection(host):
    print "try to get HTTP connection to %s..." % host
    if not host in http_pool:
        conn = httplib.HTTPConnection(host)
        conn.connect()
        print "...create HTTP connection to %s" % host
        http_pool[host] = conn
    print "...done."
    return http_pool[host]
        

def get_https_connection(host):
    print "try to get HTTPS connection to %s..." % host
    if not host in https_pool:
        conn = httplib.HTTPSConnection(host)
        conn.connect()
        print "...create HTTPS connection to %s" % host
        https_pool[host] = conn
    print "...done."
    return https_pool[host]