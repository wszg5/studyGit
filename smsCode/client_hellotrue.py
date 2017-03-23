# coding:utf-8
import httplib, json
import time
import re

from dbapi import dbapi
from zcache import cache
import util


class client_hellotrue:
    def __init__(self, serial, username, password):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}
        self.domain = "api.hellotrue.com"
        self.port = 80
        self.serial = serial
        self.logger = util.logger
        self.author = "powerman"
        self.username = username
        self.password = password
        self.im_type_list = {
            'wechat_register': "1017",
            'bind_qq_security_center': "1332",
            'qq_contact_bind': "1463",
            'qq_register': "2982",
            'alipay_register': "1023",
        }

    def GetToken(self, useCache=True):
        key = 'HelloTrue_Token_%s' % (hash(self.serial) % 10)  # 根据手机串码的hash值尾号共用token, 每10个手机共用一个token
        if useCache:
            tokenCache = cache.get(key)
            if tokenCache:
                return tokenCache

        user = self.username.encode("utf-8")
        pwd = self.password.encode("utf-8")

        path = "/api/do.php?action=loginIn&name=" + user + "&password=" + pwd + "&Developer=apFsnhXLxQG5W0AWiDhr%2fg%3d%3d"
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        time.sleep(1)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            if data.startswith("1|"):
                token = data.split('|')[1];
                cache.set(key, token, None)
                return token
            elif "密码" in data:
                if not cache.get("HELLOTRUE_ERROR_PASS"):
                    cache.set("HELLOTRUE_ERROR_PASS", True)
                    dbapi.log_error("", "开放云登录失败了", "开放云用户密码错误，请修改")

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
            raise 'Hellotrue has tried 3 minutes'
        token = self.GetToken()
        key = 'HelloTrue_phone_%s_%s' % (token, itemId)
        phone = cache.popSet(key)
        if phone:
            return phone
        try:
            itemcode = self.im_type_list[itemId]
            path = "/api/do.php?action=getPhone&sid=%s&token=%s" % (itemcode, token)
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
        except Exception as e:
            self.logger.info(e.message)
            return self.GetPhoneNumber(itemId, round)


        if response.status == 200:
            data = response.read()#.decode('GBK')
            self.logger.info("===SERVER RESTURN:%s" % data)

            data = data.split('|');
            if data[0] == "1":
                cache.addSet(key, data[1])
            else:
                time.sleep(3)
        return self.GetPhoneNumber(itemId, round)

    def ReleasePhone(self, phoneNumber, itemId):
        token = self.GetToken()
        path = "/api/do.php?action=cancelRecv&token=%s&phone=%s&sid=%s" % (token, phoneNumber, itemId)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
        else:
            ok = 'ok'

    def GetCode(self, number, itemId, length=6):
        key = 'hellotrue_verify_code_%s_%s' % (itemId, number)
        code = cache.get(key)
        if code:
            return code
        token = self.GetToken()
        try:
            itemcode = self.im_type_list[itemId]
            path = "/api/do.php?action=getMessage&token=%s&sid=%s&phone=%s&author=%s" % (token, itemcode, number, self.author)
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
            if response.status == 200:
                data = response.read()#.decode('GBK')
                if data.startswith("0|"):
                    return None
                res = re.findall("\d{%s}" % length, data)
                code = res[0]
                sms_number_key = 'hellotrue_verify_code_%s_%s' % (itemId, number)
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
        path = "/api/do.php?action=addBlacklist&token=%s&sid=%s&phone=%s" % (token, itemId, phoneNumber)
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


    xunma = client_hellotrue("as23222334fasdf", "api-gbis8b3h","13141314abc")

    number =  xunma.GetPhoneNumber("qq_contact_bind")
    print number
    print xunma.GetVertifyCode(number , "qq_contact_bind", 4)