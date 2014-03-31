#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
config.py - Global configuration
'''

# Attention:
#     Don't store config.xxx in other modules, or changes of
#     config.xxx would not take effects.

# account ids
H_QQ = "123456789"
G_QQ = "123456789"

# authorization information
G_TK = "1234567890"
COOKIE = "key1=value1;key2=value2;"

# raw file coding
code = "gbk"

# scratch related
rawfile = {
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
retry = 5    # retry times
timeout = 2  # timeout for web operations

# database related
dbfile = "../db/qzone.db"
sqlfile = "../db/db.sql"
