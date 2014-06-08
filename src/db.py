#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
db.py - Communicate with SQLite database
'''

import sqlite3

class BaseDb(object):
    def __init__(self, dbfile):
        self.dbfile = dbfile

        print "connect to %s..." % self.dbfile,
        self.conn = sqlite3.connect(self.dbfile)
        self.cursor = self.conn.cursor()
        print "done."

    def execute_cmd(self, cmd, *args):
        return self.cursor.execute(cmd, args)

    def execute_list(self, cmd, lst):
        return self.cursor.executemany(cmd, lst)

    def execute_script(self, script):
        return self.cursor.executescript(script)

    def execute_commit(self):
        self.conn.commit()

    def init_db(self, sqlfile):
        print "clear %s..." % self.dbfile,
        f = open(self.dbfile, 'w')
        f.close()
        print "done."
        
        print "load %s..." % sqlfile
        f = open(sqlfile)
        self.execute_script(f.read())
        f.close()
        print "...done."

    def insert_template(self, tablename, knames, *args):
        '''
        According to DELETE&INSERT to add one record into the database
        @param tablename: the table to be operated
        @param knames: K values as keys
        @param args: K + N values to be inserted, while keys are in the front
        '''
        knames = list(kn+"=? " for kn in knames)
        cmd = "DELETE FROM %s WHERE %s" % (tablename, "and ".join(knames))
        self.execute_cmd(cmd, *args[:len(knames)])
        
        splst = ["?" for i in range(len(args))]
        cmd = "INSERT INTO %s VALUES (%s)" % (tablename, ",".join(splst))
        self.execute_cmd(cmd, *args)
    
    def query_template(self, tablename, cnames, knames, *args):
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
        cursor = self.execute_cmd(cmd, *args)
        return self.cursor.fetchall()

class CrawlerDb(BaseDb):
    def __init__(self, *args):
        super(CrawlerDb, self).__init__(*args)
        
    # Message board
    def insert_msgboard(self, *args):
        knames = ["cmtid"]
        self.insert_template("msgboard", knames, *args)

    def insert_msgreply(self, *args):    
        knames = ["cmtid", "rplid"]
        self.insert_template("msgreply", knames, *args)

    # Blogs
    def insert_bloglist(self, *args):    
        knames = ["blogid"]
        self.insert_template("bloglist", knames, *args)

    def insert_blogcmt(self, *args):    
        knames = ["blogid", "cmtid"]
        self.insert_template("blogcmt", knames, *args)

    def insert_blogreply(self, *args):    
        knames = ["blogid", "cmtid", "rplid"]
        self.insert_template("blogreply", knames, *args)

    # Shuo Shuo    
    def insert_sslist(self, *args):    
        knames = ["ssid"]
        self.insert_template("sslist", knames, *args)

    def insert_sscmt(self, *args):    
        knames = ["ssid", "cmtid"]
        self.insert_template("sscmt", knames, *args)

    def insert_ssreply(self, *args):    
        knames = ["ssid", "cmtid", "rplid"]
        self.insert_template("ssreply", knames, *args)

    # Photos
    def insert_albumlist(self, *args):    
        knames = ["albumid"]
        self.insert_template("albumlist", knames, *args)

    def insert_photolist(self, *args):    
        knames = ["albumid", "photoid"]
        self.insert_template("photolist", knames, *args)

    def insert_photocmt(self, *args):    
        knames = ["albumid", "photoid", "cmtid"]
        self.insert_template("photocmt", knames, *args)

    def insert_photoreply(self, *args):    
        knames = ["albumid", "photoid", "cmtid", "rplid"]
        self.insert_template("photoreply", knames, *args)

    def query_bloglist(self):
        lst = self.query_template("bloglist", ["blogid"], None)
        return [t[0] for t in lst]

    def query_albumlist(self):
        lst = self.query_template("albumlist", ["albumid"], None)
        return [t[0] for t in lst]

    def query_photolist(self, albumid):
        lst = self.query_template("photolist", ["photoid"], ["albumid"], albumid)
        return [t[0] for t in lst]

if __name__ == '__main__':
    db = CrawlerDb("../db/test.db")
    db.init_db("../db/db.sql")