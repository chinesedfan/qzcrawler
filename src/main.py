#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
main.py - Main entry
'''

import hashlib

import config
import scratch
import analyze
import db

def do_msgboard():
    scratch.scratch_msgboard(config.rawfile["msgboard"])
    analyze.analyze_msgboard(config.rawfile["msgboard"])

def do_blog():    
    scratch.scratch_bloglist(config.rawfile["bloglist"])
    analyze.analyze_bloglist(config.rawfile["bloglist"])
    bloglst = db.query_bloglist()
    for blogid in bloglst:
        cmtfile = config.rawfile["blogdir"] + str(blogid) + ".txt"
        scratch.scratch_blogcmt(blogid, cmtfile)
        analyze.analyze_blogcmt(blogid, cmtfile)

def do_shuoshuo():
    scratch.scratch_shuoshuo(config.rawfile["shuoshuo"])
    analyze.analyze_shuoshuo(config.rawfile["shuoshuo"])
    
def do_photos():
    scratch.scratch_albumlist(config.rawfile["albumlist"])
    analyze.analyze_albumlist(config.rawfile["albumlist"])
    albumlst = db.query_albumlist()
    for albumid in albumlst:
        plfile = config.rawfile["albumdir"] + albumid + "_photolist.txt"
        scratch.scratch_photolist(albumid, plfile)
        analyze.analyze_photolist(albumid, plfile)
        
        photolst = db.query_photolist(albumid)
        for photoid in photolst:
            pcfile = config.rawfile["albumdir"] + albumid + "_" \
                + hashlib.md5(photoid).hexdigest().upper() + "_photocmt.txt"
            scratch.scratch_photocmt(albumid, photoid, pcfile)
            analyze.analyze_photocmt(albumid, photoid, pcfile)

def main():
    # prepare the database
    config.dbfile = "../db/%s.db" % config.H_QQ
    db.init_db()
    
    # web -> files -> db
    do_msgboard()
    do_blog()
    do_shuoshuo()
    do_photos()
    print "Congratulations! All is done!"
    
if __name__ == '__main__':
    main()