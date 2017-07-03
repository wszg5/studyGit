# -*- coding:utf-8 -*-
import httplib, json
import time
import re
import traceback

from zcache import cache
import util


class client_xunma:
    def __init__(self, serial, username, password, im_type_list):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}
        self.domain = "xapi.xunma.net"
        self.port = 80
        self.serial = serial
        self.logger = util.logger

        self.username = username
        self.password = password
        self.im_type_list = im_type_list

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
            if data.startswith("False"):  # Token以False开头，嵌套调用
                return self.GetToken()
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

    def GetPhoneNumber(self, itemId, phoneNum=None, times=0):
        round = times + 1
        if round > 30:
            return None
            # raise 'XunMa has tried 3 minutes'
        token = self.GetToken()
        key = 'phone_%s_%s' % (token, itemId)
        phone = cache.popSet(key)
        if phone:
            return phone

        count = 1;
        itemcode = self.im_type_list[itemId]
        self.logger.info("itemcode_%s" % itemcode)
        self.logger.info("token_%s" % token)
        path = "/getPhone?ItemId=%s&token=%s&Count=%s" % (itemcode, token, str(count))
        if phoneNum is not None:
            path = "%s&Phone=%s" % (path, phoneNum)
        try:
            # self.logger.info("===XUNMA URL:%s" % path)
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
        except Exception as e:
            self.logger.error(traceback.format_exc())
            return self.GetPhoneNumber(itemId, phoneNum,round)
        if response.status == 200:
            data = response.read().decode('GBK')
            self.logger.info("===XUNMA RESTURN:%s" % data)
            import string
            if string.find(data, u'单个用户获取数量不足') != -1:
                self.ReleaseAllPhone()
            if u'Session 过期' in data or u'Session过期' in data:
                self.GetToken(False)
            if u'暂时没有此项目号码，请等会试试'  in data:
                return None

            if data.startswith('False'):
                time.sleep(3)
            numbers = data.split(";");
            for number in numbers:
                if re.search("\d{11}", str(number)):
                    cache.addSet(key, number)
            return self.GetPhoneNumber(itemId, phoneNum,round)
        else:
            data = response.read().decode('GBK')
            self.logger.info("===Failed XUNMA RESTURN:%s" % data)
            return self.GetPhoneNumber(itemId, phoneNum,round)

    def ReleasePhone(self, phoneNumber, itemId):
        token = self.GetToken()
        itemcode = self.im_type_list[itemId]
        path = "/releasePhone?token=%s&phoneList=%s-%s" % (token, phoneNumber, itemcode)
        try:
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
        except Exception:
            return 'ok'
        if response.status == 200:
            data = response.read()
        else:
            ok = 'ok'

    def GetCode(self, number, itemId, length=6):
        itemcode = self.im_type_list[itemId]
        key = 'verify_code_%s_%s' % (itemcode, number)
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
                print(data)
                if u'Session 过期' in data or u'Session过期' in data:
                    self.GetToken(False)
                    return None
        except Exception:
            return None

        smsList = self.ExtractSMS(data, length)
        for sms in smsList:
            if 'phone' in sms and 'code' in sms:
                sms_number_key = 'verify_code_%s_%s' % (sms['itemid'], sms['phone'])
                print ("KEY: %s, Code: %s" % (sms_number_key, sms['code']))
                cache.set(sms_number_key, sms['code'])
                    #cache.set(sms['phone'], sms['code'])
                '''
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

                '''

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
        try:
            path = "/addBlack?token=%s&phoneList=%s-%s" % (token, itemcode, phoneNumber)
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)

            response = conn.getresponse()
        except Exception:
            return 'ok'


        if response.status == 200:
            data = response.read()
        else:
            return 'ok'

    def MatchPhoneNumber(self, number, itemId):
        itemcode = self.im_type_list[itemId]

        token = self.GetToken()
        path = "/getPhone?ItemId=" + itemcode + "&token=" + token + "&Phone=" + number + ""
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

    def ExtractSMS(self, content, length):
        if content is None:
            return []
        result = []
        smsList = content.split('[End]')
        for sms in smsList:
            if 'MSG' not in sms:
                continue
            data = sms.split('&');
            if len(data) >=4:
                itemid = data[1]
                phone = data[2]
                sms = data[3]
                res = re.findall("\d{%s}" % length, sms)
                code = res[0]
                result.append({'phone': phone, 'code' : code, 'itemid': itemid});
        print(result)
        return result;



if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

    im_type_list = {"qq_register": "2251"}
    xunma = client_xunma("asdfasdfasdf", "powerman", "12341234abc", im_type_list)

    sms = u'MSG&2251&13941940790&【腾讯科技】你正在注册微信帐号，验证码303615。请勿转发。[End]RES&2251&13941940790[End]'
    sms = None
    print(xunma.ExtractSMS(sms, 6))
    phone =  xunma.GetPhoneNumber("qq_register")

    phone =  xunma.GetPhoneNumber("qq_register", phone)
    print phone
    print xunma.GetVertifyCode(phone, "qq_register", 6)
