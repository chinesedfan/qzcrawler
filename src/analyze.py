#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
analyze.py - Analysis from the scratched file, and save into the database
'''

import json

import db
import config

def analyze_msgboard(logfile):
    for s in get_jsonstr(logfile):
        data = json.loads(s)
        
        cmtlst = data["data"]["commentList"]        
        print "got commentList=%d" % len(cmtlst)
        for cmt in cmtlst:
            rpllst = cmt["replyList"]
            db.insert_msgboard(cmt["id"], cmt["uin"], json.dumps(cmt["ubbContent"], ensure_ascii=False),
                               cmt["pubtime"], cmt["modifytime"], len(rpllst))
    
            print "got replyList=%d" % len(rpllst)
            for i in range(len(rpllst)):
                rpl = rpllst[i]
                db.insert_msgreply(cmt["id"], i, rpl["uin"], 
                                   rpl["content"], rpl["time"])
    db.execute_commit()
    print "...done."

def analyze_bloglist(logfile):
    for s in get_jsonstr(logfile):
        data = json.loads(s)
        
        bloglst = data["data"]["list"]        
        print "got bloglst=%d" % len(bloglst)
        for blog in bloglst:
            db.insert_bloglist(blog["blogId"], blog["cate"], blog["title"], 
                               blog["pubTime"], blog["commentNum"])    
    db.execute_commit()
    print "...done."

def analyze_blogcmt(blogid, logfile):
    for s in get_jsonstr(logfile):
        data = json.loads(s)
        
        cmtlst = data["data"]["comments"]        
        print "got commentList=%d" % len(cmtlst)
        for cmt in cmtlst:
            rpllst = cmt["replies"]
            db.insert_blogcmt(blogid, cmt["id"], cmt["poster"]["id"], json.dumps(cmt["content"], ensure_ascii=False),
                               cmt["postTime"], len(rpllst))
    
            print "got replyList=%d" % len(rpllst)
            for rpl in rpllst:
                db.insert_blogreply(blogid, cmt["id"], rpl["id"], rpl["poster"]["id"], 
                                   rpl["content"], rpl["postTime"])    
    db.execute_commit()
    print "...done."

def analyze_shuoshuo(logfile):
    for s in get_jsonstr(logfile):
        data = json.loads(s)
        
        msglst = data["msglist"]
        print "got msgList=%d" % len(msglst)
        for msg in msglst:
            db.insert_sslist(msg["tid"], msg["content"], msg["createTime"], msg["cmtnum"])
            if not "commentlist" in msg:
                continue       
            
            # someone adds comments on this message
            cmtlst = msg["commentlist"]
            print "got commentList=%d" % len(cmtlst)
            for cmt in cmtlst:
                db.insert_sscmt(msg["tid"], cmt["tid"], cmt["uin"], cmt["content"],
                                   cmt["createTime"], cmt["reply_num"])
        
                if not "list_3" in cmt:
                    continue
                
                # someone replies on this comment            
                rpllst = cmt["list_3"]
                print "got replyList=%d" % len(rpllst)
                for rpl in rpllst:
                    db.insert_ssreply(msg["tid"], cmt["tid"], rpl["tid"], rpl["uin"], 
                                       rpl["content"], rpl["createTime"])
    db.execute_commit()
    print "...done."

def analyze_albumlist(logfile):
    for s in get_jsonstr(logfile):
        data = json.loads(s)
        
        albumlst = data["data"]["album"]        
        print "got albumlst=%d" % len(albumlst)
        for album in albumlst:
            db.insert_albumlist(album["id"], album["name"], album["desc"], album["createtime"],
                                album["lastuploadtime"], album["modifytime"], album["total"])    
    db.execute_commit()
    print "...done."

def analyze_photolist(albumid, logfile):
    for s in get_jsonstr(logfile):
        data = json.loads(s)
        
        photolst = data["data"]["photoList"]
        # no photo in this album
        if photolst is None:
            break
        print "got photolst=%d" % len(photolst)
        for photo in photolst:
            db.insert_photolist(albumid, photo["lloc"], photo["name"], photo["desc"], 
                                photo["uploadtime"], photo["forum"])
    db.execute_commit()
    print "...done."  

def analyze_photocmt(albumid, photoid, logfile):
    for s in get_jsonstr(logfile):
        data = json.loads(s)
        
        cmtlst = []
        if "comments" in data["data"]:
            cmtlst = data["data"]["comments"]        
        print "got commentList=%d" % len(cmtlst)
        for cmt in cmtlst:
            rpllst = []
            if "replies" in cmt:
                rpllst = cmt["replies"]
            db.insert_photocmt(albumid, photoid, cmt["id"], cmt["poster"]["id"], cmt["content"],
                               cmt["postTime"], len(rpllst))
    
            print "got replyList=%d" % len(rpllst)
            for rpl in rpllst:
                db.insert_photoreply(albumid, photoid, cmt["id"], rpl["id"], rpl["poster"]["id"], 
                                   rpl["content"], rpl["postTime"])    
    db.execute_commit()
    print "...done."

'''
Internal helper functions
'''

def get_jsonstr(logfile):
    f = open(logfile)
    content = f.read().decode(config.code) # Use the saved coding
    
    lst = []
    callbacks = content.split("_Callback")
    for i in range(1, len(callbacks)):
        lst.append(callbacks[i][1:-3])
    print "get_jsonstr size=%d" % len(lst)
    return lst