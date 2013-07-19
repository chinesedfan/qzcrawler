#!/usr/bin/python

'''
analyze.py - Analysis from the scratched file
'''

import db
import json

'''
Analyze all items of this QZone
'''

def analyze_msgboard(logfile):
    for s in get_jsonstr(logfile):
        data = json.loads(s)
        
        cmtlst = data["data"]["commentList"]        
        print "got commentList=%d" % len(cmtlst)
        for cmt in cmtlst:
            db.insert_msgboard(cmt["id"], cmt["uin"], cmt["ubbContent"],
                               cmt["pubtime"], cmt["modifytime"])
    
            rpllst = cmt["replyList"]
            print "got replyList=%d" % len(rpllst)
            for i in range(0, len(rpllst)):
                rpl = rpllst[i]
                db.insert_msgreply(cmt["id"], i, rpl["uin"], 
                                   rpl["content"], rpl["time"])
    db.conn.commit()
    print "...done."

def analyze_blogs(logfile):
    pass

def analyze_shuoshuo(logfile):
    pass

def analyze_photos(logfile):
    pass

'''
Internal helper functions
'''
def get_jsonstr(logfile, code = "gbk"):
    f = open(logfile)
    content = f.read().decode(code)
    
    lst = []
    callbacks = content.split("_Callback")
    for i in range(1, len(callbacks)):
        lst.append(callbacks[i][1:-3])
    print "get_jsonstr size=%d" % len(lst)
    return lst

def get_bloglist(logfile):
    pass

def get_albumlist(logfile):
    pass

def get_photolist(albumid, logfile):
    pass 