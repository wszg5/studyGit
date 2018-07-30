# -*- coding:utf-8 -*-
import httplib
import re
import time
import traceback
import util

class client_suma:
    def __init__(self):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}
        self.domain = "api.eobzz.com"
        self.port = 80
        self.logger = util.logger

        self.username = 'powerman'
        self.password = '13141314abc'

    def GetToken(self):

        user = self.username.encode("utf-8")
        pwd = self.password.encode("utf-8")

        path = "/httpApi.do?action=loginIn&uid=" + user + "&pwd=" + pwd
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        time.sleep(1)
        response = conn.getresponse()

        if response.status == 200:
            data = response.read()
            if data.startswith("powerman|"):
                token = data.split('|')[1]
                return token
            else:
                return self.GetToken()

        else:
            return self.GetToken()

    def GetPhoneNumber(self, pid, phoneNum=None, times=0):
        round = times + 1
        if round > 30:
            return None
            # raise 'SUMA has tried 3 minutes'
        token = self.GetToken()
        uid = self.username
        count = 10  # 获取号码数量(1<=count<=10)
        self.logger.info("pid_%s" % pid)
        self.logger.info("token_%s" % token)
        path = "/httpApi.do?action=getMobilenum&pid=%s&uid=%s&token=%s&size=%s" % (pid, uid, token, count)
        if phoneNum is not None:
            path = "%s&mobile=%s" % (path, phoneNum)
        try:
            # self.logger.info("===SUMA URL:%s" % path)
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
        except Exception as e:
            self.logger.error(traceback.format_exc())
            return self.GetPhoneNumber(pid, phoneNum,round)
        if response.status == 200:
            data = response.read().decode('GBK')
            self.logger.info("===SUMA RESTURN:%s" % data)

            import string
            if string.find(data, u'单个用户获取数量不足') != -1:
                self.ReleaseAllPhone()
            if u'Session 过期' in data or u'Session过期' in data:
                self.GetToken(False)
            if u'暂时没有此项目号码，请等会试试'  in data:
                return None

            if data.endswith('|'+token):
                time.sleep(3)
                numbers = data.split("|")[0]
                if ";" in numbers:
                    numbers = numbers.split(";")
                    return numbers
                else:
                    return numbers
            else:
                return self.GetPhoneNumber(pid, phoneNum, round)
        else:
            # data = response.read().decode('GBK')
            data = response.read().decode( 'UTF-8' )
            self.logger.info("===Failed SUMA RESTURN:%s" % data)
            return self.GetPhoneNumber(pid, phoneNum,round)

    def GetCode(self, number, type=0, pid=None): # 0是获取验证码不继续使用号码，1是获取验证码继续使用号码
        # http://api.eobzz.com/httpApi.do?action=getVcodeAndReleaseMobile&uid=用户名&token=登录时返回的令牌&mobile=获取到的手机号码&author_uid=软件开发者用户名(可选, 可得10%的消费分成)
        #action=getVcodeAndHoldMobilenum&uid=用户&token=登录时返回的令牌&mobile=获取到的手机号码&next_pid=下个要接收的项目
        token = self.GetToken()
        uid = self.username
        try:
            i = 0
            while True:
                i += 1
                if type == 0:
                    path = "/httpApi.do?action=getVcodeAndReleaseMobile&uid=%s&token=%s&mobile=%s"%(uid, token, number)
                else:
                    path = "/httpApi.do?action=getVcodeAndHoldMobilenum&uid=%s&token=%s&mobile=%s&next_pid%s" % (uid, token, number,pid)

                conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                conn.request("GET", path)
                response = conn.getresponse()
                if response.status == 200:
                    data = response.read().decode('UTF-8')
                    print(data)
                    if u'Session 过期' in data or u'Session过期' in data:
                        self.GetToken()
                        return None
                    if data.startswith(number+"|"):
                        msg = data.split("|")[1]
                        code = re.findall(r"\d+\.?\d*", msg)[0]
                        return code

                    time.sleep(3)
                    if i == 3:
                        return None

                else:
                    return None

        except Exception:
            self.logger.error(traceback.format_exc())
            return None

    def defriendPhoneNumber(self, phoneNumber, pid):
        # http://api.eobzz.com/httpApi.do?action=addIgnoreList&uid=用户名&token=登录时返回的令牌&mobiles=号码1,号码2,号码3&pid=项目ID
        token = self.GetToken()
        uid = self.username
        try:
            path = "/httpApi.do?action=addIgnoreList&uid=%s&token=%s&mobiles=%s&pid=%s" % (uid, token, phoneNumber, pid)
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)

            response = conn.getresponse()
        except Exception:
            return 'ok'


        if response.status == 200:
            data = response.read()
        else:
            return 'ok'



if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    suma = client_suma()
    phone = suma.GetPhoneNumber(8858)
    code = suma.GetCode(phone)
    suma.defriendPhoneNumber(phone,8858)





