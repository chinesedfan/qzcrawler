#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
login.py - Simulate to login and get the required information, 
           which is inspired by https://github.com/junit/qzonelogin
'''

import urllib2, cookielib
import random
import hashlib

class LoginUtil(object):
    def __init__(self):
        pass

    @staticmethod
    def install_opener():
        cj = cookielib.CookieJar()
        cookieProc = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookieProc)
        
        urllib2.install_opener(opener)
        return cj

    @staticmethod
    def get_template(key, args):
        host = args["host"]
        url = args["url"]
        headers = {"Host": host}
        
        # ATTENTION: instead of httplib, we use urllib2 here to manage cookies automatically
        req = urllib2.Request("http://" + host + url, None, headers)
        resp = urllib2.urlopen(req)
        content = resp.read()
        
        if not ("mark1" in args) or not ("mark2" in args):
            return content
        
        mark1 = args["mark1"]
        mark2 = args["mark2"]
        pos1 = content.find(mark1)
        if pos1 < 0:
            raise Exception("...%s not found" % key)
        pos2 = content.find(mark2, pos1)
        value = content[pos1+len(mark1):pos2]
        print "...found %s=%s" % (key, value)

        return value

    @staticmethod
    def get_login_sig():
        args = {}
        args["host"] = "ui.ptlogin2.qq.com"
        args["url"] = "/cgi-bin/login?daid=5&pt_qzone_sig=1&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=12&target=self&s_url=http%3A//qzs.qq.com/qzone/v5/loginsucc.html?para=izone&pt_qr_app=%CA%D6%BB%FAQQ%BF%D5%BC%E4&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=http%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=http%3A//z.qzone.com/download.html"
        args["mark1"] = "login_sig:\""
        args["mark2"] = "\","
        
        return LoginUtil.get_template("login_sig", args)

    @staticmethod
    def get_vc_image(uin, path = "../raw/vc.jpg"):
        args = {}
        args["host"] = "captcha.qq.com"
        args["url"] = "/getimage?uin=%s" % uin \
            + "&aid=549000912&%s" % random.random()
        content = LoginUtil.get_template("vc_image", args)

        # FIXME: it's better to define the path in config.py, but config.py wants to import this file
        f = open(path, "w")
        f.write(content)
        f.flush()
        f.close()
        print "...save vc in file %s" % path

    @staticmethod
    def get_verify_code(uin, login_sig):
        '''
        @return: verify code, or None when failed to auto-verify
        '''
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
        
        values = LoginUtil.get_template("check_vc", args).split(",")

        # right sample: '0','!MYP','\x00\x00\x00\x00\x15\xb9\x5f\x9f'
        # wrong sample: '1','sPKvl2bLJsTJYLwKBmBONNcAh8eFyaYy','\x00\x00\x00\x00\x00\xbc\x4f\xf2'
        if len(values) != 3 or values[0] != "\'0\'":
            # need request for verify code image
            return None
        return values[1][1:-1]

    @staticmethod
    def get_real_uin(uin):
        # treat QQ as a number, and present as 16-bit hex
        hex_uin = hex(int(uin))
        real_uin = '0'*(16-len(hex_uin)+2) + hex_uin[2:]
        return real_uin

    @staticmethod
    def get_pwd(real_uin, pwd, vc):
        '''
        @param real_uin: 16-bit hex of QQ number
        @param pwd: QQ password
        @param vc: verfiy code
        @return: hash code of these information
        '''
        # binary md5 of the password
        code = hashlib.md5(pwd).digest()
        # treat uin as hex and decode it, then attach after the previous and calculate upper hex md5
        code = hashlib.md5(code + real_uin.upper().decode("hex")).hexdigest().upper()
        # attach upper vc and calculate upper hex md5 again
        code = hashlib.md5(code + vc.upper()).hexdigest().upper()
        print "...uin=%s pwd=%s vc=%s code=%s" % (real_uin, pwd, vc, code)

        return code

    @staticmethod
    def do_login(uin, pwd, vc, login_sig):
        '''
        @param uin: QQ number
        @param pwd: calculated by get_pwd, not QQ password
        @param vc: verfiy code
        @param login_sig: requested by get_login_sig
        '''
        args = {}
        args["host"] = "ptlogin2.qq.com"
        args["url"] = "/login?" \
            + "u=%s&p=%s" % (uin, pwd) \
            + "&verifycode=%s" % vc \
            + "&aid=549000912" \
            + "&u1=http%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&h=1&ptredirect=0&ptlang=2052&daid=5&from_ui=1&dumy=&low_login_enable=0&regmaster=&fp=loginerroralert&action=2-21-1385452444158&mibao_css=&t=1&g=1&js_ver=10052&js_type=1" \
            + "&login_sig=%s" % login_sig \
            + "&pt_rsa=0&pt_qzone_sig=1"
        args["mark1"] = "("
        args["mark2"] = ")"

        values = LoginUtil.get_template("login_info", args).split(",")

        # sample: '3','0','','0','User name or password error', '123456789'
        #         '4','0','','0','Verify code error, please reinput', '123456789'
        #         '0','0','http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone&ptsig=1234567890abcdef','0','login ok', 'username'
        if values[0] != "\'0\'":
            raise Exception("...failed to login")

    @staticmethod
    def get_cookies(cj):
        '''
        @return: a dictionary which includes necessary cookies
        '''
        cookies = cj._cookies
        keys = ["uin", "skey"]
        results = {}
        for domain in cookies.keys():
            for path in cookies[domain].keys():
                for name in cookies[domain][path].keys():
                    ck = cookies[domain][path][name]
                    if ck.name in keys:
                        results[ck.name] = ck.value
        return results

    @staticmethod
    def get_gtk(skey):
        magic = 5381
        for c in skey:
            magic += (magic << 5) + ord(c)
        return magic & 0x7fffffff

    @staticmethod
    def main(uin, pwd):
        '''
        @return: gtk and cookies string for config.py
        '''
        cj = LoginUtil.install_opener()
        
        login_sig = LoginUtil.get_login_sig()
        vc = LoginUtil.get_verify_code(uin, login_sig)
        if vc is None:
            LoginUtil.get_vc_image(uin)
            vc = raw_input("Please input vc: ")
        
        pwd = LoginUtil.get_pwd(LoginUtil.get_real_uin(uin), pwd, vc)
        LoginUtil.do_login(uin, pwd, vc, login_sig)

        cookies = LoginUtil.get_cookies(cj)
        gtk = LoginUtil.get_gtk(cookies["skey"])
        return gtk, "; ".join([key+"="+cookies[key] for key in cookies.keys()])

#For Testing
if __name__ == '__main__':
    uin = "123456789"
    pwd = "testpwd"
    LoginUtil.main(uin, pwd)
