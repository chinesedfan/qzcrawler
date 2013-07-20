#!/usr/bin/python

'''
db.py - Communicate with SQLite database
'''

import sqlite3

dbfile = "../db/qzone.db"
sqlfile = "../db/db.sql"

conn = None
cursor = None

def execute_cmd(cmd, *args):
    init_conn()
    return cursor.execute(cmd, args)

def execute_list(cmd, lst):
    init_conn()
    return cursor.executemany(cmd, lst)

def execute_script(script):
    init_conn()
    return cursor.executescript(script)

def init_conn():
    global dbfile
    global conn, cursor
    if conn is None:
        print "connect to %s..." % dbfile,
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        print "done."

def init_db():
    global dbfile, sqlfile
    
    print "clear %s..." % dbfile,
    f = open(dbfile, 'w')
    f.close()
    print "done."
    
    print "load %s..." % sqlfile
    f = open(sqlfile)
    execute_script(f.read())
    f.close()
    print "...done."

def insert_msgboard(cmtid, uin, content, pubtime, modifytime, replynum):
    cmd = "DELETE FROM msgboard WHERE cmtid=?"
    execute_cmd(cmd, cmtid)
    cmd = "INSERT INTO msgboard VALUES (?, ?, ?, ?, ?, ?)"
    execute_cmd(cmd, cmtid, uin, content, pubtime, modifytime, replynum)

def insert_msgreply(cmtid, rplid, uin, content, time):    
    cmd = "DELETE FROM msgreply WHERE cmtid=? and rplid=?"
    execute_cmd(cmd, cmtid, rplid)
    cmd = "INSERT INTO msgreply VALUES (?, ?, ?, ?, ?)"
    execute_cmd(cmd, cmtid, rplid, uin, content, time)