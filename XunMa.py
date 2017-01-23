# coding:utf-8
import httplib, json
import time
import re
from zcache import cache
class XunMa:
    def __init__(self):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}
        self.domain = "api.xunma.net"
        self.port = 8080
    def GetToken(self, useCache=True):
        from dbapi import dbapi
        dbapi = dbapi()
        if useCache :
            tokenCache = cache.get('XunMa') #讯码token有效期５分钟
            if tokenCache:
                return tokenCache
        rk = dbapi.GetCodeSetting()
        xm_user = rk["xm_user"]
        xm_pwd = rk["xm_pwd"]
        user =  xm_user.encode("utf-8")
        pwd = xm_pwd.encode("utf-8")
        # path = "/Login?uName=powerman&pWord=13141314&Developer=apFsnhXLxQG5W0AWiDhr%2fg%3d%3d"
        path = "/Login?uName="+user+"&pWord="+pwd+"&Developer=apFsnhXLxQG5W0AWiDhr%2fg%3d%3d"
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        time.sleep(1)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            cache.set('XunMa', data)
            return  data
        else:
            return "Error Getting Account, Please check your repo"
    def ReleaseAllPhone(self):
        token=self.GetToken()
        try:
            path = "/pubApi/ReleaseAllPhone?token=%s"%token
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
        except Exception:
            ok = 'ok'
    def GetPhoneNumber(self, itemId):
        token = self.GetToken()
        key = 'phone_%s'%itemId
        phone = cache.popSet(key)
        if phone:
            return phone
        lockKey = 'lock_get_phone_%s'%itemId
        if cache.get(lockKey):
            time.sleep(5)
            return self.GetPhoneNumber(itemId)
        else:
            cache.set(lockKey,True,30)
        try:
            path = "/getPhone?ItemId=%s&token=%s&Count=10" % (itemId, token)
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
        except Exception:
            ok = 'ok'


        if response.status == 200:
            data = response.read().decode('GBK')
            import string
            if string.find(data,'单个用户获取数量不足')!=-1 :
                self.ReleaseAllPhone()
            if string.find(data,'Session 过期')!=-1 :
                self.GetToken(False)
            if data.startswith('False'):
                time.sleep(3)
            numbers = data.split(";");
            for number in numbers:
                if re.search("\d{11}", str(number)):
                    cache.addSet(key, number)
            cache.set(lockKey,False)
            return self.GetPhoneNumber(itemId)
        else:
            cache.set(lockKey,False)
            return self.GetPhoneNumber(itemId)
    def ReleasePhone(self, phoneNumber):         #释放手机好
        token = self.GetToken()
        path = "/releasePhone?token=%s&phoneList=%s-144" % (token, phoneNumber)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
        else:
            ok = 'ok'







    def GetVertifyCode(self, number, itemId, length=6):
        key = 'verify_code_%s_%s'%(itemId,number)
        for i in range(1, 60):
            time.sleep(1)
            code = cache.get(key)
            if code:
                return code
            token = self.GetToken()
            try:
                path = "/getQueue?token=" + token + ""
                conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                conn.request("GET", path)
                response = conn.getresponse()
            except Exception:
                continue
            if response.status == 200:
                data = response.read().decode('GBK')
                print(data)
                if 'MSG' in data:
                # if data.startswith('MSG'):
                    targetNumber = re.findall(r'1\d{10}',data)
                    targetNumber = targetNumber[0]
                    '''
                    if targetNumber == number:
                        res = re.findall(r"MSG&144&" + number + "&(.+?)\[End]", data)
                        res = re.findall("\d{6}", res[0])
                        code = res[0]
                        return code
                    else:
                    '''

                    par = r"MSG&%s&%s&(.+?)\[End]"%(itemId, targetNumber)


                    #res = re.findall(r"MSG&144&" + targetNumber + "&(.+?)\[End]", data)
                    res = re.findall(par, data)
                    res = re.findall("\d{%s}"%length, res[0])
                    code = res[0]
                    sms_number_key = 'verify_code_%s_%s'%(itemId,targetNumber)
                    cache.set(sms_number_key, code)
                else:
                    return '失败'
        return ""
    def UploadPhoneNumber(self, number):
        token = self.GetToken()
        path = "/getPhone?ItemId=144&token=" + token + "&Phone="+number+""
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
    xunma = XunMa()
    a = xunma.GetToken()
    # b = xunma.GetPhoneNumber(a)
    # a = xunma.GetCode(b,a)
    # result = repo.GetAccount("6", 120, 1)
    # result = repo.SetAccount("6", "ddkf", "1918697054")
    # result = repo.GetMaterial("8",120,1)
    # result = repo.GetNumber("13",0,1)              #意思是取13号仓库2小时内没有用过的号码，一次取16个