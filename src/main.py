#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
main.py - Main entry
'''

import hashlib

from config import Config
from scratch import Scratcher
from analyze import Analyzer
from db import CrawlerDb

class Application(object):
    def __init__(self, config):
        self.config = config
        self.scratcher = Scratcher(self.config)
        self.analyzer = Analyzer(self.config)
        self.db = CrawlerDb(self.config.dbfile)

        # prepare the database
        self.config.dbfile = "../db/%s.db" % self.config.H_QQ
        self.db.init_db(self.config.sqlfile)

    def do_msgboard(self):
        self.scratcher.scratch_msgboard(self.config.rawfile["msgboard"])
        self.analyzer.analyze_msgboard(self.config.rawfile["msgboard"])

    def do_blog(self):    
        self.scratcher.scratch_bloglist(self.config.rawfile["bloglist"])
        self.analyzer.analyze_bloglist(self.config.rawfile["bloglist"])
        bloglst = self.db.query_bloglist()
        for blogid in bloglst:
            cmtfile = self.config.rawfile["blogdir"] + str(blogid) + ".txt"
            self.scratcher.scratch_blogcmt(blogid, cmtfile)
            self.analyzer.analyze_blogcmt(blogid, cmtfile)

    def do_shuoshuo(self):
        self.scratcher.scratch_shuoshuo(self.config.rawfile["shuoshuo"])
        self.analyzer.analyze_shuoshuo(self.config.rawfile["shuoshuo"])
        
    def do_photos(self):
        self.scratcher.scratch_albumlist(self.config.rawfile["albumlist"])
        self.analyzer.analyze_albumlist(self.config.rawfile["albumlist"])
        albumlst = self.db.query_albumlist()
        for albumid in albumlst:
            plfile = self.config.rawfile["albumdir"] + albumid + "_photolist.txt"
            self.scratcher.scratch_photolist(albumid, plfile)
            self.analyzer.analyze_photolist(albumid, plfile)
            
            photolst = self.db.query_photolist(albumid)
            for photoid in photolst:
                pcfile = self.config.rawfile["albumdir"] + albumid + "_" \
                    + hashlib.md5(photoid).hexdigest().upper() + "_photocmt.txt"
                self.scratcher.scratch_photocmt(albumid, photoid, pcfile)
                self.analyzer.analyze_photocmt(albumid, photoid, pcfile)

    def main(self):   
        # web -> files -> db
        self.do_msgboard()
        self.do_blog()
        self.do_shuoshuo()
        self.do_photos()
        print "Congratulations! All is done!"
    
if __name__ == '__main__':
    app = Application(Config("123456789", "test", True))
    app.main()