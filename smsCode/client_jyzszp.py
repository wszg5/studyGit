# coding:utf-8
import httplib, json
import time
import re
from zcache import cache
import util


class client_jyzszp:
    def __init__(self, serial, username, password):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}
        self.domain = "api.xunma.net"
        self.port = 8888
        self.serial = serial
        self.logger = util.logger

        self.username = username
        self.password = password
        self.im_type_list = {
            'wechat_register': 1001,
            'qq_contact_bind': 1001,
            'qq_register': 2111,
            'alipay_register': 1001,
        }

    def GetToken(self, useCache=True):
        key = 'XunMa_Token_%s' % (hash(self.serial) % 10)  # 根据手机串码的hash值尾号共用token, 每10个手机共用一个token
        if useCache:
            tokenCache = cache.get(key)
            if tokenCache:
                return tokenCache

        user = self.username.encode("utf-8")
        pwd = self.password.encode("utf-8")

        path = "/Login?uName=" + user + "&pWord=" + pwd + "&Developer=apFsnhXLxQG5W0AWiDhr%2fg%3d%3d"
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        time.sleep(1)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            token = data.split('&')[0];
            cache.set(key, token, None)
            return token
        else:
            return self.GetToken()

    def ReleaseAllPhone(self):
        token = self.GetToken()
        try:
            path = "/pubApi/ReleaseAllPhone?token=%s" % token
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
        except Exception:
            ok = 'ok'

    def GetPhoneNumber(self, itemId, times=0):
        round = times + 1
        if round > 30:
            raise 'XunMa has tried 3 minutes'
        token = self.GetToken()
        key = 'phone_%s_%s' % (token, itemId)
        phone = cache.popSet(key)
        if phone:
            return phone

        try:
            itemcode = self.im_type_list[itemId]
            path = "/getPhone?ItemId=%s&token=%s&Count=10" % (itemcode, token)
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
        except Exception as e:
            self.logger.info(e.message)
            return self.GetPhoneNumber(itemId, round)
        if response.status == 200:
            data = response.read().decode('GBK')
            self.logger.info("===XUNMA RESTURN:%s" % data)
            import string
            if string.find(data, '单个用户获取数量不足') != -1:
                self.ReleaseAllPhone()
            if 'Session 过期' in data or 'Session过期' in data :
                self.GetToken(False)
            if data.startswith('False'):
                time.sleep(3)
            numbers = data.split(";");
            for number in numbers:
                if re.search("\d{11}", str(number)):
                    cache.addSet(key, number)
            return self.GetPhoneNumber(itemId, round)
        else:
            return self.GetPhoneNumber(itemId, round)

    def ReleasePhone(self, phoneNumber, itemId):
        token = self.GetToken()
        path = "/releasePhone?token=%s&phoneList=%s-%s" % (token, phoneNumber, itemId)
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
            path = "/getQueue?token=" + token + ""
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
            if response.status == 200:
                data = response.read().decode('GBK')

                if 'Session 过期' in data or 'Session过期' in data:
                    self.GetToken(False)
                    return None
        except Exception:
            return None

        if 'MSG' in data:
            targetNumber = re.findall(r'1\d{10}', data)
            targetNumber = targetNumber[0]

            par = r"MSG&(\d+)&%s&(.+?)\[End]" % targetNumber
            res = re.findall(par, data)
            res = res[0]
            if len(res) == 2:
                targetItemId = res[0]
                res = re.findall("\d{%s}" % length, res[1])
                code = res[0]
                sms_number_key = 'verify_code_%s_%s' % (targetItemId, targetNumber)
                cache.set(sms_number_key, code)

    def GetVertifyCode(self, number, itemId, length=6):
        for i in range(1, 22):
            time.sleep(3)
            code = self.GetCode(number, itemId, length)
            if code is not None:
                return code
        return ""

    def defriendPhoneNumber(self, phoneNumber, itemId):
        token = self.GetToken()
        path = "/addBlack?token=%s&phoneList=%s-%s" % (token, itemId, phoneNumber)
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
            data = data.decode('GBK')
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


    xunma = client_xunma("asdfasdfasdf", "powerman","12341234abc")
    print xunma.GetPhoneNumber("qq_register")