#!/usr/bin/python

'''
scratch.py - Scratch information from the web, and store in specified files
'''

import config
import pool

import copy
import string

args_template = {
    # required
    "host": "",
    "headers": {},
    "logfile": "",
    "num": 0,
    "scratch_item": "",
    "url_template": "",
    # alternative    
        #"mark1": "",
        #"mark2": "",
        #"total": 0,
    # optional
    "append": False,
    "code": "gbk",
    "connection_type": "http",
    "method": "GET",
    "postdata": "",
}

def scratch_msgboard(logfile):
    real_args = copy.deepcopy(args_template)
    real_args["host"] = "m.qzone.qq.com"
    real_args["headers"] = {"Host": real_args["host"], "Cookie": config.COOKIE}
    real_args["logfile"] = logfile
    real_args["num"] = 10
    real_args["scratch_item"] = "msgboard"
    real_args["url_template"] = "/cgi-bin/new/get_msgb?" \
        + "uin=%s&hostUin=%s" % (config.G_QQ, config.H_QQ) \
        + "&inCharset=%s&outCharset=%s&format=%s" % ("gbk", "gbk", "jsonp") \
        + "&g_tk=%s" % config.G_TK \
        + "&num=%d&start=%d"
    
    real_args["mark1"] = "total\":"
    real_args["mark2"] = ","   
    
    scratch_template(real_args)

def scratch_bloglist(logfile):
    real_args = copy.deepcopy(args_template)
    real_args["host"] = "b1.qzone.qq.com"
    real_args["headers"] = {"Host": real_args["host"], "Cookie": config.COOKIE}
    real_args["logfile"] = logfile
    real_args["num"] = 15
    real_args["scratch_item"] = "bloglist"
    real_args["url_template"] = "/cgi-bin/blognew/get_abs?" \
        + "uin=%s&hostUin=%s" % (config.G_QQ, config.H_QQ) \
        + "&inCharset=%s&outCharset=%s&format=%s" % ("gbk", "gbk", "jsonp") \
        + "&g_tk=%s" % config.G_TK \
        + "&blogType=0&reqInfo=1" \
        + "&num=%d&pos=%d"
    
    real_args["mark1"] = "totalNum\":"
    real_args["mark2"] = ","   
    
    scratch_template(real_args)

def scratch_blogcmt(blogid, logfile, append):
    pass

def scratch_shuoshuo(logfile):
    real_args = copy.deepcopy(args_template)
    real_args["host"] = "taotao.qq.com"
    real_args["headers"] = {"Host": real_args["host"], "Cookie": config.COOKIE}
    real_args["logfile"] = logfile
    real_args["num"] = 20
    real_args["scratch_item"] = "shuoshuo"
    real_args["url_template"] = "/cgi-bin/emotion_cgi_msglist_v6?" \
        + "uin=%s&hostUin=%s" % (config.G_QQ, config.H_QQ) \
        + "&inCharset=%s&outCharset=%s&format=%s" % ("gbk", "gbk", "jsonp") \
        + "&g_tk=%s" % config.G_TK \
        + "&num=%d&pos=%d"
    
    real_args["mark1"] = "msgnum\":"
    real_args["mark2"] = ","
    
    real_args["code"] = "utf-8"
    
    scratch_template(real_args)

def scratch_albumlist(logfile):
    real_args = copy.deepcopy(args_template)
    
    real_args["logfile"] = logfile
    real_args["num"] = 100
    real_args["scratch_item"] = "albumlist"
    real_args["url_template"] = "/fcgi-bin/fcg_list_album_v2?" \
        + "uin=%s&hostUin=%s" % (config.G_QQ, config.H_QQ) \
        + "&inCharset=%s&outCharset=%s&format=%s" % ("gbk", "gbk", "jsonp") \
        + "&g_tk=%s" % config.G_TK \
        + "&num=%d&start=%d" # non-sense in this function
    
    real_args["mark1"] = "albumnum\" : "
    real_args["mark2"] = ","
    
    # try following known servers until get the list, still not always work
    album_hosts = ['xalist.photo.qq.com', 'hzalist.photo.qq.com']    
    for host in album_hosts:  
        real_args["host"] = host
        real_args["headers"] = {"Host": real_args["host"], "Cookie": config.COOKIE}
        ret, n = scratch_template(real_args)
        if ret and n > 0:
            break

def scratch_photolist(albumid, logfile, append):
    pass

def scratch_photocmt(photid, logfile, append):
    pass

'''
Internal helper function
'''

def scratch_template(args):
    host = args["host"]
    if args["connection_type"] == "HTTPS":
        conn = pool.get_https_connection(host)
    else:
        conn = pool.get_http_connection(host)
    
    code = args["code"]
    url_template = args["url_template"]
    
    print "try to scratch %s..." % args["scratch_item"]
    
    num = args["num"]
    start = 0
    flag = False # whether total has been set
    if "total" in args:
        total = args["total"]
        flag = True
    else: 
        total = num
    
    logfile = args["logfile"] 
    if args["append"]:
        f = open(logfile, "a")
    else:
        f = open(logfile, "w")
    
    while start < total:
        print "start=%d total=%d" % (start, total)
        url = url_template % (num, start)
        conn.request(args["method"], url, args["postdata"], args["headers"])
        try:
            resp = conn.getresponse()
        except:
            continue
        
        if resp.status != 200:
            print "...failed, returns %d" % resp.status
            return False, -1
        content = resp.read().decode(code)
    
        # update the real total count, if a function or value has been provided
        if not flag:
            pos1 = content.find(args["mark1"])
            if pos1 < 0:
                print "...failed, not found"
                return False, -1
            pos2 = content.find(args["mark2"], pos1)
            total = string.atoi(content[pos1+len(args["mark1"]):pos2])
         
        f.write(content)
        f.write("\n")
         
        start = start + num
    f.flush()
    f.close()
    print "...total=%d" % total
    print "...done."
    return True, total