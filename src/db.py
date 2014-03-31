#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
db.py - Communicate with SQLite database
'''

import sqlite3

import config

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

def execute_commit():
    if conn:
        conn.commit()

def init_conn():
    global conn, cursor
    if conn is None:
        print "connect to %s..." % config.dbfile,
        conn = sqlite3.connect(config.dbfile)
        cursor = conn.cursor()
        print "done."

def init_db():
    print "clear %s..." % config.dbfile,
    f = open(config.dbfile, 'w')
    f.close()
    print "done."
    
    print "load %s..." % config.sqlfile
    f = open(config.sqlfile)
    execute_script(f.read())
    f.close()
    print "...done."

# Message board
def insert_msgboard(*args):
    knames = ["cmtid"]
    insert_template("msgboard", knames, *args)

def insert_msgreply(*args):    
    knames = ["cmtid", "rplid"]
    insert_template("msgreply", knames, *args)

# Blogs
def insert_bloglist(*args):    
    knames = ["blogid"]
    insert_template("bloglist", knames, *args)

def insert_blogcmt(*args):    
    knames = ["blogid", "cmtid"]
    insert_template("blogcmt", knames, *args)

def insert_blogreply(*args):    
    knames = ["blogid", "cmtid", "rplid"]
    insert_template("blogreply", knames, *args)

# Shuo Shuo    
def insert_sslist(*args):    
    knames = ["ssid"]
    insert_template("sslist", knames, *args)

def insert_sscmt(*args):    
    knames = ["ssid", "cmtid"]
    insert_template("sscmt", knames, *args)

def insert_ssreply(*args):    
    knames = ["ssid", "cmtid", "rplid"]
    insert_template("ssreply", knames, *args)

# Photos
def insert_albumlist(*args):    
    knames = ["albumid"]
    insert_template("albumlist", knames, *args)

def insert_photolist(*args):    
    knames = ["albumid", "photoid"]
    insert_template("photolist", knames, *args)

def insert_photocmt(*args):    
    knames = ["albumid", "photoid", "cmtid"]
    insert_template("photocmt", knames, *args)

def insert_photoreply(*args):    
    knames = ["albumid", "photoid", "cmtid", "rplid"]
    insert_template("photoreply", knames, *args)

def query_bloglist():
    lst = query_template("bloglist", ["blogid"], None)
    return [t[0] for t in lst]

def query_albumlist():
    lst = query_template("albumlist", ["albumid"], None)
    return [t[0] for t in lst]

def query_photolist(albumid):
    lst = query_template("photolist", ["photoid"], ["albumid"], albumid)
    return [t[0] for t in lst]

'''
Internal helper functions
'''

def insert_template(tablename, knames, *args):
    '''
    According to DELETE&INSERT to add one record into the database
    '''
    knames = list(kn+"=? " for kn in knames)
    cmd = "DELETE FROM %s WHERE %s" % (tablename, "and ".join(knames))
    execute_cmd(cmd, *args[:len(knames)])
    
    splst = ["?" for i in range(len(args))]
    cmd = "INSERT INTO %s VALUES (%s)" % (tablename, ",".join(splst))
    execute_cmd(cmd, *args)
    
def query_template(tablename, cnames, knames, *args):
    '''
    @param tablename: the table to be queried
    @param cnames: the list of columns to be selected
    @param knames: the list of condition names
    @param args: N values that used in WHERE clauses   
    @return: a list, whose elements are tuples of one row in database
    '''
    if cnames is None:
        select = "*"
    else:
        select = ",".join(cnames)
        
    if knames is None:
        where = ""
    else:
        knames = list(kn+"=? " for kn in knames)
        where = " WHERE %s" % "and ".join(knames)
    
    # local cursor
    cmd = "SELECT %s FROM %s %s" % (select, tablename, where)
    cursor = execute_cmd(cmd, *args)
    return cursor.fetchall()