#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
scratch.py - Scratch information from the web, and store in specified files
'''

# Usage samples:
#     scratch_msgboard("../raw/msgboard.txt")
#     scratch_bloglist("../raw/bloglist.txt")
#     scratch_blogcmt("1226814446", "../raw/blogcmt.txt", True) 
#     scratch_shuoshuo("../raw/shuoshuo.txt")
#     scratch_albumlist("../raw/albumlist.txt")  
#     scratch_photolist("318908369", "../raw/photolist.txt", True)
#     scratch_photocmt("318908369", "NDJ0n1.5FWCUkFHgzZsB.d*8X8AjAAA!", "../raw/photocmt.txt", True)        

import copy
import string
import sys
import time

import config
import pool

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
    "exit": True,
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
        + "&inCharset=%s&outCharset=%s&format=%s" % (real_args["code"], real_args["code"], "jsonp") \
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
        + "&inCharset=%s&outCharset=%s&format=%s" % (real_args["code"], real_args["code"], "jsonp") \
        + "&g_tk=%s" % config.G_TK \
        + "&blogType=0&reqInfo=1" \
        + "&num=%d&pos=%d"
    
    real_args["mark1"] = "totalNum\":"
    real_args["mark2"] = ","   
    
    scratch_template(real_args)

def scratch_blogcmt(blogid, logfile, append = False):
    real_args = copy.deepcopy(args_template)
    real_args["host"] = "b1.qzone.qq.com"
    real_args["headers"] = {"Host": real_args["host"], "Cookie": config.COOKIE}
    real_args["logfile"] = logfile
    real_args["num"] = 15
    real_args["scratch_item"] = "blogcmt"
    real_args["url_template"] = "/cgi-bin/blognew/get_comment_list?" \
        + "uin=%s&hostUin=%s" % (config.G_QQ, config.H_QQ) \
        + "&inCharset=%s&outCharset=%s&format=%s" % (real_args["code"], real_args["code"], "jsonp") \
        + "&g_tk=%s" % config.G_TK \
        + "&topicId=%s_%s" % (config.H_QQ, blogid) \
        + "&num=%d&start=%d"
    
    real_args["mark1"] = "total\":"
    real_args["mark2"] = ","   
    
    real_args["append"] = append
    
    scratch_template(real_args)

def scratch_shuoshuo(logfile):
    real_args = copy.deepcopy(args_template)
    real_args["host"] = "taotao.qq.com"
    real_args["headers"] = {"Host": real_args["host"], "Cookie": config.COOKIE}
    real_args["logfile"] = logfile
    real_args["num"] = 20
    real_args["scratch_item"] = "shuoshuo"
    real_args["code"] = "utf-8"
    real_args["url_template"] = "/cgi-bin/emotion_cgi_msglist_v6?" \
        + "uin=%s&hostUin=%s" % (config.G_QQ, config.H_QQ) \
        + "&inCharset=%s&outCharset=%s&format=%s" % (real_args["code"], real_args["code"], "jsonp") \
        + "&g_tk=%s" % config.G_TK \
        + "&num=%d&pos=%d"
    
    real_args["mark1"] = "msgnum\":"
    real_args["mark2"] = ","
    
    scratch_template(real_args)

def scratch_albumlist(logfile):
    real_args = copy.deepcopy(args_template)
    
    real_args["logfile"] = logfile
    real_args["num"] = 10
    real_args["scratch_item"] = "albumlist"
    real_args["url_template"] = "/fcgi-bin/fcg_list_album_v2?" \
        + "uin=%s&hostUin=%s" % (config.G_QQ, config.H_QQ) \
        + "&inCharset=%s&outCharset=%s&format=%s" % (real_args["code"], real_args["code"], "jsonp") \
        + "&g_tk=%s" % config.G_TK \
        + "&num=%d&start=%d" # non-sense in this function
    
    real_args["mark1"] = "albumnum\" : "
    real_args["mark2"] = ","
    
    # try following known servers until get the list, still not always work
    album_hosts = ['xalist.photo.qq.com', 'hzalist.photo.qq.com']    
    for host in album_hosts:  
        real_args["host"] = host
        real_args["headers"] = {"Host": real_args["host"], "Cookie": config.COOKIE}
        real_args["exit"] = (host == album_hosts[-1])
        ret, n = scratch_template(real_args)
        if ret and n > 0:
            break

def scratch_photolist(albumid, logfile, append = False):
    real_args = copy.deepcopy(args_template)
    
    real_args["logfile"] = logfile
    real_args["num"] = 12
    real_args["scratch_item"] = "photolist"
    real_args["url_template"] = "/fcgi-bin/cgi_list_photo?" \
        + "uin=%s&hostUin=%s" % (config.G_QQ, config.H_QQ) \
        + "&inCharset=%s&outCharset=%s&format=%s" % (real_args["code"], real_args["code"], "jsonp") \
        + "&g_tk=%s" % config.G_TK \
        + "&topicId=%s" % albumid \
        + "&pageNum=%d&pageStart=%d"
    
    real_args["mark1"] = "totalInAlbum\" : "
    real_args["mark2"] = ","
        
    real_args["append"] = append
    
    # try following known servers until get the list, still not always work
    album_hosts = ['hzplist.photo.qq.com']    
    for host in album_hosts:  
        real_args["host"] = host
        real_args["headers"] = {"Host": real_args["host"], "Cookie": config.COOKIE}
        ret, n = scratch_template(real_args)
        if ret and n > 0:
            break

def scratch_photocmt(albumid, photoid, logfile, append = False):
    real_args = copy.deepcopy(args_template)
    real_args["host"] = "app.photo.qq.com"
    real_args["headers"] = {"Host": real_args["host"], "Cookie": config.COOKIE}
    real_args["logfile"] = logfile
    real_args["num"] = 5
    real_args["scratch_item"] = "photocmt"
    real_args["code"] = "utf-8"
    real_args["url_template"] = "/cgi-bin/app/cgi_pcomment_xml_v2?" \
        + "uin=%s&hostUin=%s" % (config.G_QQ, config.H_QQ) \
        + "&inCharset=%s&outCharset=%s&format=%s" % (real_args["code"], real_args["code"], "jsonp") \
        + "&g_tk=%s" % config.G_TK \
        + "&topicId=%s_%s" % (albumid, photoid) \
        + "&num=%d&start=%d"
    
    real_args["mark1"] = "\"total\" : "
    real_args["mark2"] = "\n"   
            
    real_args["append"] = append
    
    scratch_template(real_args)

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
        total = start + num
    
    logfile = args["logfile"] 
    if args["append"]:
        f = open(logfile, "a")
    else:
        f = open(logfile, "w")
    
    times = 1
    while start < total:
        print "start=%d total=%d" % (start, total)
        url = url_template % (num, start)
        content = ""
        try:
            conn.request(args["method"], url, args["postdata"], args["headers"])
            resp = conn.getresponse()
        
            if resp.status != 200:
                raise Exception("...status failed, returns %d" % resp.status)
            content = resp.read().decode(code, "ignore")

            # update the real total count, if a function or value has been provided
            if not flag:
                pos1 = content.find(args["mark1"])
                if pos1 < 0:
                    raise Exception("...not found")
                pos2 = content.find(args["mark2"], pos1)
                total = string.atoi(content[pos1+len(args["mark1"]):pos2])
        except:
            print sys.exc_info()
            if (times == config.retry):
                print "...failed, abort to retry"
                if args["exit"]:
                    sys.exit()
                else:
                    return False, -1
            times = times + 1
            # wait for a while to re-request
            time.sleep(1)
            continue     
        f.write(content.encode(config.code)) # encoding the same as the editor, or failed to open and analyze
        f.write("\n")
         
        start = start + num
    f.flush()
    f.close()
    print "...total=%d" % total
    print "...done."
    return True, total