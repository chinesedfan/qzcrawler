#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
analyze.py - Analysis from the scratched file, and save into the database
'''

import json

from db import CrawlerDb
from config import Config

class Analyzer(object):
    def __init__(self, config):
        self.config = config
        self.db = CrawlerDb(config.dbfile)

    def analyze_msgboard(self, logfile):
        for s in self.get_jsonstr(logfile):
            data = json.loads(s)
            
            cmtlst = data["data"]["commentList"]        
            print "got commentList=%d" % len(cmtlst)
            for cmt in cmtlst:
                rpllst = cmt["replyList"]
                self.db.insert_msgboard(cmt["id"], cmt["uin"], json.dumps(cmt["ubbContent"], ensure_ascii=False),
                                   cmt["pubtime"], cmt["modifytime"], len(rpllst))
        
                print "got replyList=%d" % len(rpllst)
                for i in range(len(rpllst)):
                    rpl = rpllst[i]
                    self.db.insert_msgreply(cmt["id"], i, rpl["uin"], 
                                       rpl["content"], rpl["time"])
        self.db.execute_commit()
        print "...done."

    def analyze_bloglist(self, logfile):
        for s in self.get_jsonstr(logfile):
            data = json.loads(s)
            
            bloglst = data["data"]["list"]        
            print "got bloglst=%d" % len(bloglst)
            for blog in bloglst:
                self.db.insert_bloglist(blog["blogId"], blog["cate"], blog["title"], 
                                   blog["pubTime"], blog["commentNum"])    
        self.db.execute_commit()
        print "...done."

    def analyze_blogcmt(self, blogid, logfile):
        for s in self.get_jsonstr(logfile):
            data = json.loads(s)
            
            cmtlst = data["data"]["comments"]        
            print "got commentList=%d" % len(cmtlst)
            for cmt in cmtlst:
                rpllst = cmt["replies"]
                self.db.insert_blogcmt(blogid, cmt["id"], cmt["poster"]["id"], json.dumps(cmt["content"], ensure_ascii=False),
                                   cmt["postTime"], len(rpllst))
        
                print "got replyList=%d" % len(rpllst)
                for rpl in rpllst:
                    self.db.insert_blogreply(blogid, cmt["id"], rpl["id"], rpl["poster"]["id"], 
                                       rpl["content"], rpl["postTime"])    
        self.db.execute_commit()
        print "...done."

    def analyze_shuoshuo(self, logfile):
        for s in self.get_jsonstr(logfile):
            data = json.loads(s)
            
            msglst = data["msglist"]
            print "got msgList=%d" % len(msglst)
            for msg in msglst:
                self.db.insert_sslist(msg["tid"], msg["content"], msg["createTime"], msg["cmtnum"])
                if not "commentlist" in msg:
                    continue       
                
                # someone adds comments on this message
                cmtlst = msg["commentlist"]
                print "got commentList=%d" % len(cmtlst)
                for cmt in cmtlst:
                    self.db.insert_sscmt(msg["tid"], cmt["tid"], cmt["uin"], cmt["content"],
                                       cmt["createTime"], cmt["reply_num"])
            
                    if not "list_3" in cmt:
                        continue
                    
                    # someone replies on this comment            
                    rpllst = cmt["list_3"]
                    print "got replyList=%d" % len(rpllst)
                    for rpl in rpllst:
                        self.db.insert_ssreply(msg["tid"], cmt["tid"], rpl["tid"], rpl["uin"], 
                                           rpl["content"], rpl["createTime"])
        self.db.execute_commit()
        print "...done."

    def analyze_albumlist(self, logfile):
        for s in self.get_jsonstr(logfile):
            data = json.loads(s)
            
            albumlst = data["data"]["album"]        
            print "got albumlst=%d" % len(albumlst)
            for album in albumlst:
                self.db.insert_albumlist(album["id"], album["name"], album["desc"], album["createtime"],
                                    album["lastuploadtime"], album["modifytime"], album["total"])    
        self.db.execute_commit()
        print "...done."

    def analyze_photolist(self, albumid, logfile):
        for s in self.get_jsonstr(logfile):
            data = json.loads(s)
            
            photolst = data["data"]["photoList"]
            # no photo in this album
            if photolst is None:
                break
            print "got photolst=%d" % len(photolst)
            for photo in photolst:
                self.db.insert_photolist(albumid, photo["lloc"], photo["name"], photo["desc"], 
                                    photo["uploadtime"], photo["forum"])
        self.db.execute_commit()
        print "...done."  

    def analyze_photocmt(self, albumid, photoid, logfile):
        for s in self.get_jsonstr(logfile):
            data = json.loads(s)
            
            cmtlst = []
            if "comments" in data["data"]:
                cmtlst = data["data"]["comments"]        
            print "got commentList=%d" % len(cmtlst)
            for cmt in cmtlst:
                rpllst = []
                if "replies" in cmt:
                    rpllst = cmt["replies"]
                self.db.insert_photocmt(albumid, photoid, cmt["id"], cmt["poster"]["id"], cmt["content"],
                                   cmt["postTime"], len(rpllst))
        
                print "got replyList=%d" % len(rpllst)
                for rpl in rpllst:
                    self.db.insert_photoreply(albumid, photoid, cmt["id"], rpl["id"], rpl["poster"]["id"], 
                                       rpl["content"], rpl["postTime"])    
        self.db.execute_commit()
        print "...done."

    def get_jsonstr(self, logfile):
        f = open(logfile)
        content = f.read().decode(self.config.code) # Use the saved coding
        
        lst = []
        callbacks = content.split("_Callback")
        for i in range(1, len(callbacks)):
            lst.append(callbacks[i][1:-3])
        print "get_jsonstr size=%d" % len(lst)
        return lst

# For testing
if __name__ == '__main__':
    config = Config("123456789", "test", True)
    config.dbfile = "../db/test.db"
    analyzer = Analyzer(config)
    analyzer.analyze_msgboard(config.rawfile["msgboard"])