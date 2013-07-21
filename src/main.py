#!/usr/bin/python

'''
main.py - Main entry
'''

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
        # override the file each time
        scratch.scratch_blogcmt(blogid, config.rawfile["blogcmt"])
        analyze.analyze_blogcmt(blogid, config.rawfile["blogcmt"])

def do_shuoshuo():
    scratch.scratch_shuoshuo(config.rawfile["shuoshuo"])
    analyze.analyze_shuoshuo(config.rawfile["shuoshuo"])
    
def do_photos():
    scratch.scratch_albumlist(config.rawfile["albumlist"])
    analyze.analyze_albumlist(config.rawfile["albumlist"])
    albumlst = db.query_albumlist()
    for albumid in albumlst:
        # override the file each time
        scratch.scratch_photolist(albumid, config.rawfile["photolist"])
        analyze.analyze_photolist(albumid, config.rawfile["photolist"])
        
        photolst = db.query_photolist(albumid)
        for photoid in photolst:
            # override the file each time
            scratch.scratch_photocmt(albumid, photoid, config.rawfile["photocmt"])
            analyze.analyze_photocmt(albumid, photoid, config.rawfile["photocmt"])

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