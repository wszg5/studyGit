# coding:utf-8
import httplib, json
import time
import re

from dbapi import dbapi
from zcache import cache
import util


class client_jyzszp:
    def __init__(self, serial, username, password):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}
        self.domain = "api.jyzszp.com"
        self.port = 80
        self.serial = serial
        self.logger = util.logger
        self.author = "powerman"
        self.username = username
        self.password = password
        self.im_type_list = {
            'wechat_register': "1289",
            'bind_qq_security_center': "1332",
            'qq_contact_bind': "5008",
            'qq_register': "2982",
            'alipay_register': "1023",
        }

    def GetToken(self, useCache=True):
        key = 'jyzszp_Token_%s' % (hash(self.serial) % 10)  # 根据手机串码的hash值尾号共用token, 每10个手机共用一个token
        if useCache:
            tokenCache = cache.get(key)
            if tokenCache:
                return tokenCache

        user = self.username.encode("utf-8")
        pwd = self.password.encode("utf-8")

        path = "/Api/index/loginIn?uid=%s&pwd=%s"%(user, pwd )
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        time.sleep(1)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            token = data.split('|');
            if len(token) == 3:
                token = token[2]
                cache.set(key, token, None)
                return token
            elif len(token) == 1:
                if not cache.get("HELLOTRUE_ERROR_PASS"):
                    cache.set("HELLOTRUE_ERROR_PASS", True)
                    dbapi.log_error("", "菜众享登录失败了", "菜众享登录失败，错误码：%s"%data)
                time.sleep(3)
        return self.GetToken()

    def ReleaseAllPhone(self):
        token = self.GetToken()
        try:
            path = "/api/do.php?action=cancelAllRecv&token=%s" % token
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
        except Exception:
            ok = 'ok'

    def GetPhoneNumber(self, itemId, times=0):
        round = times + 1
        if round > 30:
            raise 'jyzszp has tried 3 minutes'
        token = self.GetToken()
        key = 'phone_%s_%s' % (token, itemId)
        phone = cache.popSet(key)
        if phone:
            return phone
        try:
            itemcode = self.im_type_list[itemId]
            path = "/Api/index/getMobilenum?pid=%s&uid=%s&token=%s&size=1" % (itemcode,self.username, token)
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
        except Exception as e:
            self.logger.info(e.message)
            return self.GetPhoneNumber(itemId, round)


        if response.status == 200:
            data = response.read()#.decode('GBK')
            self.logger.info("=jyzszp==SERVER RESTURN:%s" % data)

            data = data.split('|');
            if len(data) == 2:
                cache.addSet(key, data[0])
            else:
                time.sleep(3)
        return self.GetPhoneNumber(itemId, round)

    def ReleasePhone(self, phoneNumber, itemId):
        token = self.GetToken()
        itemcode = self.im_type_list[itemId]
        path = "/Api/index/cancelSMSRecv?uid=%s&token=%s&mobiles=%s&pid=%s" % (self.username, token, phoneNumber, itemcode)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
        else:
            ok = 'ok'

    def GetCode(self, number, itemId, length=6):
        key = 'verify_code_%s_%s' % (itemId, number)
        code = cache.get(key)
        if code:
            return code
        token = self.GetToken()
        try:
            itemcode = self.im_type_list[itemId]
            path = "/Api/index/getVcodeAndReleaseMobile?uid=%s&token=%s&mobile=%s&pid=%s&author_uid=%s" % (self.username,token, number,itemcode, self.author)
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
            if response.status == 200:
                data = response.read()#.decode('GBK')
                dataObj = data.split('|');
                if len(dataObj) >=3 :
                    targetNumber = re.findall(r'1\d{10}', data)
                    targetNumber = targetNumber[0]
                    if len(dataObj[1]) == length:
                        code = dataObj[1]
                        sms_number_key = 'verify_code_%s_%s' % (itemId, targetNumber)
                        cache.set(sms_number_key, code)
            else:
                data = response.read()#.decode('GBK')
                util.logger.error(data)
        except Exception:
            return None



    def GetVertifyCode(self, number, itemId, length=6):
        for i in range(1, 22):
            time.sleep(3)
            code = self.GetCode(number, itemId, length)
            if code is not None:
                return code
        return ""

    def defriendPhoneNumber(self, phoneNumber, itemId):
        token = self.GetToken()
        itemcode = self.im_type_list[itemId]
        path = "/Api/index/addIgnoreList?uid=%s&token=%s&mobiles=%s&pid=%s" % (self.username, token, phoneNumber,itemcode)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
        else:
            ok = 'ok'

    def MatchPhoneNumber(self, number, itemId):

        token = self.GetToken()
        path = "/getPhone?ItemId=" + itemId + "&token=" + token + "&Phone=" + number + ""
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        try:
            response = conn.getresponse()
        except Exception:
            return 0
        if response.status == 200:
            data = response.read()
            #data = data.decode('GBK')
            if len(data) == 12:
                return data
            else:
                return 0
        else:
            return "Error Getting Account, Please check your repo"


if __name__ == '__main__':
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')


    xunma = client_jyzszp("as23222334fasdf", "42019-fuk","13141314abc")

    number =  xunma.GetPhoneNumber("wechat_register")
    print number
    print xunma.GetVertifyCode(number , "wechat_register", 4)