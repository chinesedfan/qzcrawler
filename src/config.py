#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
config.py - Global configuration
'''

from login import LoginUtil

class Config(object):
    def __init__(self, qq="123456789", pwd="test", isLogin=False):
        # account ids
        self.H_QQ = qq
        self.G_QQ = qq

        # authorization information
        self.PWD = pwd
        if isLogin:
            self.G_TK, self.COOKIE = LoginUtil.main(self.H_QQ, self.PWD)

        # raw file coding
        self.code = "gbk"

        # scratch related
        self.rawfile = {
            "msgboard": "../raw/msgboard.txt",
            "bloglist": "../raw/bloglist.txt",    
            "shuoshuo": "../raw/shuoshuo.txt",
            "albumlist": "../raw/albumlist.txt",
            # reuse these files, override every time
            "blogcmt": "../raw/blogcmt.txt",
            "photolist": "../raw/photolist.txt",
            "photocmt": "../raw/photocmt.txt",
            # avoid to override, and directories should end with slash
            "blogdir": "../raw/blog/",
            "albumdir": "../raw/album/",   
        }
        self.retry = 5    # retry times
        self.timeout = 2  # timeout for web operations

        # database related
        self.dbfile = "../db/qzone.db"
        self.sqlfile = "../db/db.sql"

    def updateLoginInfo(self):
        self.G_TK, self.COOKIE = LoginUtil.main(self.H_QQ, self.PWD)

# For testing
if __name__ == '__main__':
    config = Config(isLogin=True);