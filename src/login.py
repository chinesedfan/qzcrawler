#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
login.py - Simulate to login and get the required information, 
           which is inspired by https://github.com/junit/qzonelogin
'''

import pool
import random
import hashlib

def get_login_sig():
    args = {}
    args["host"] = "ui.ptlogin2.qq.com"
    args["url"] = "/cgi-bin/login?daid=5&pt_qzone_sig=1&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=12&target=self&s_url=http%3A//qzs.qq.com/qzone/v5/loginsucc.html?para=izone&pt_qr_app=%CA%D6%BB%FAQQ%BF%D5%BC%E4&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=http%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=http%3A//z.qzone.com/download.html"
    args["mark1"] = "login_sig:\""
    args["mark2"] = "\","
    
    return get_template("login_sig", args)

def get_verify_code(uin, login_sig):
    args = {}
    args["host"] = "check.ptlogin2.qq.com"
    args["url"] = "/check?regmaster=" \
        + "&uin=%s" % uin \
        + "&appid=549000912&js_ver=10052&js_type=1" \
        + "&login_sig=%s" % login_sig \
        + "&u1=http%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone" \
        + "&r=%s" % random.random()
    args["mark1"] = "("
    args["mark2"] = ")"
    
    values = get_template("check_vc", args).split(",")
    # expect: error code, verify code, uin
    if len(values) != 3 or values[0] != "\'0\'":
        return None #TODO: request for verify code image
    return values[1][1:-1] #TODO: update uin, but why?

def do_login(uin, pwd, vc, login_sig):
    args = {}
    args["host"] = "ptlogin2.qq.com"
    args["url"] = "/login?" \
        + "&u=%s&p=%s" % (uin, get_pwd(uin, pwd, vc)) \
        + "&verifycode=%s" % vc \
        + "&aid=549000912" \
        + "&u1=http%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&h=1&ptredirect=0&ptlang=2052&daid=5&from_ui=1&dumy=&low_login_enable=0&regmaster=&fp=loginerroralert&action=2-21-1385452444158&mibao_css=&t=1&g=1&js_ver=10052&js_type=1" \
        + "&login_sig=%s" % login_sig \
        + "&pt_rsa=0&pt_qzone_sig=1"
    args["mark1"] = "("
    args["mark2"] = ")"
    
    values = get_template("login_info", args).split(",")
    if values[0] != "\'0\'": # failed to login
        pass
    print values

'''
Internal helper function
'''

def get_pwd(uin, pwd, vc):
    # binary md5 of the password
    code = hashlib.md5(pwd).digest()
    # treat uin as hex and decode it, then attach after the previous and calculate upper hex md5
    if len(uin) % 2 == 1:
        uin += "0"
    code = hashlib.md5(code + uin.upper().decode("hex")).hexdigest().upper()
    # attach upper vc and calculate upper hex md5 again
    code = hashlib.md5(code + vc.upper()).hexdigest().upper()
    print "...pwd=%s" % code

    return code

def get_template(key, args):
    host = args["host"]
    url = args["url"]
    headers = {"Host": host}
    
    conn = pool.get_http_connection(host)
    conn.request("GET", url, None, headers)
    resp = conn.getresponse()
    content = resp.read()
    
    mark1 = args["mark1"]
    mark2 = args["mark2"]
    pos1 = content.find(mark1)
    if pos1 < 0:
        raise Exception("...%s not found" % key)
    pos2 = content.find(mark2, pos1)
    value = content[pos1+len(mark1):pos2]
    print "...found %s=%s" % (key, value)

    return value

if __name__ == '__main__':
    uin = "123456789"
    #login_sig = get_login_sig()
    #vc = get_verify_code(uin, login_sig)
    #do_login("123456789", "test", vc, login_sig)

    login_sig = "1234567890abcdef"
    vc = "xanz"
    print get_pwd(uin, "123", vc)
