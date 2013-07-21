#!/usr/bin/python

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

# scratch related
rawfile = {
    "msgboard": "../raw/msgboard.txt",
    "bloglist": "../raw/bloglist.txt",
    "blogcmt": "../raw/blogcmt.txt",
    "shuoshuo": "../raw/shuoshuo.txt",
    "albumlist": "../raw/albumlist.txt",
    "photolist": "../raw/photolist.txt",
    "photocmt": "../raw/photocmt.txt",    
}
retry = 5    # retry times
timeout = 2  # timeout for web operations

# database related
dbfile = "../db/qzone.db"
sqlfile = "../db/db.sql"
