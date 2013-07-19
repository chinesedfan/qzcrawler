#!/usr/bin/python

'''
db.py - Communicate with SQLite database
'''

import sqlite3

dbfile = "../db/qzone.db"

conn = None
cursor = None

def execute_cmd(cmd, *args):
    global conn, cursor
    if conn is None:
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
    return cursor.execute(cmd, args)

def is_table_existed(tablename):
    cmd = "SELECT count(*) FROM sqlite_master " \
          "WHERE type='table' AND name=?"
    row = execute_cmd(cmd, tablename).fetchone()
    return (row and row[0] != 0)

def drop_table(tablename):
    cmd = "DROP TABLE IF EXISTS %s" % tablename
    execute_cmd(cmd)

def init_db():
    drop_table("msgboard")
    drop_table("msgreply")
    
    cmds = ["CREATE TABLE msgboard(cmtid, uin, content, pubtime, modifytime, PRIMARY KEY(cmtid))",
            "CREATE TABLE msgreply(cmtid, rplid, uin, content, time, PRIMARY KEY(cmtid, rplid))",]
           
    for c in cmds:
        execute_cmd(c)

def insert_msgboard(cmtid, uin, content, pubtime, modifytime):
    cmd = "DELETE FROM msgboard WHERE cmtid=?"
    execute_cmd(cmd, cmtid)
    cmd = "INSERT INTO msgboard VALUES (?, ?, ?, ?, ?)"
    execute_cmd(cmd, cmtid, uin, content, pubtime, modifytime)

def insert_msgreply(cmtid, rplid, uin, content, time):    
    cmd = "DELETE FROM msgreply WHERE cmtid=? and rplid=?"
    execute_cmd(cmd, cmtid, rplid)
    cmd = "INSERT INTO msgreply VALUES (?, ?, ?, ?, ?)"
    execute_cmd(cmd, cmtid, rplid, uin, content, time)