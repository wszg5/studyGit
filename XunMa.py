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


    def GetToken(self, useCache):
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


    def GetPhoneNumber(self, token, itemId):
        path = "/getPhone?ItemId=%s&token=%s&Count=1"%(itemId, token)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()

            if data.startswith('False'):
                return 'False'
            data = re.findall("\d{11}", str(data))

            data = data[0]
            return data
        else:
            return "Error Getting Account, Please check your repo"

    def ReleaseToken(self, phoneNumber, token):
        path = "/releasePhone?token=%s&phoneList=%s-144" % (token, phoneNumber)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            print (data)
        else:
            print '释放失败'


    def GetCode(self,number,token):
        for i in range(0,32,+1):
            time.sleep(2)
            path = "/getQueue?token=%s"%token
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
            if response.status == 200:
                data = response.read()

                print data

                if data.startswith('MSG'):
                    break
            else:
                return "Error Getting Account, Please check your repo"
        data = data.decode('GBK')
        res = re.findall(r"MSG&144&"+number+"&(.+?)\[End]", data)
        res = re.findall("\d{6}",res[0])
        return res[0]

    def ReleaseToken(self, phoneNumber, token):
        path = "/releasePhone?token=%s&phoneList=%s-144"%(token, phoneNumber)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()

        else:
            print '释放失败'



    def GetTIMLittleCode(self, number, token):
        print (token)
        for i in range(0, 55, +1):
            time.sleep(2)
            path = "/getQueue?token=" + token + ""
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
            if response.status == 200:
                data = response.read()
                print (data)
                time.sleep(2)
                if data.startswith('MSG'):
                    break
            else:
                return "Error Getting Account, Please check your repo"
        if data is None:
            return 0;
        data = data.decode('GBK')
        res = re.findall(r"MSG&144&" + number + "&(.+?)\[End]", data)
        res = re.findall("\d{6}", res[0])
        return res




    def GetVertifyCode(self, number,token):
        for i in range(1, 60):
            time.sleep(1)
            code = cache.get(number)
            if not code==None:
                # self.dbapi.DelCache(number)
                print '居然取到了%s'%code
                return code

            # token = self.GetToken(True)
            path = "/getQueue?token=" + token + ""
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
            if response.status == 200:
                data = response.read()

                if data.startswith('MSG'):
                    data = data.decode('GBK')
                    targetNumber = re.findall(r'1\d{10}',data)
                    targetNumber = targetNumber[0]
                    print data
                    print 'MSG%s' % number
                    if targetNumber == number:
                        res = re.findall(r"MSG&144&" + number + "&(.+?)\[End]", data)
                        res = re.findall("\d{6}", res[0])
                        code = res[0]
                        return code
                        cache.set(number, code)
                        # self.dbapi.DelCache(number)


                    else:
                        res = re.findall(r"MSG&144&" + targetNumber + "&(.+?)\[End]", data)
                        res = re.findall("\d{6}", res[0])
                        code = res[0]

                        cache.set(targetNumber, code)


        return ""

    def GetBindNumber(self, res):
        path = "/getPhone?ItemId=153&token=" + res + "&Count=1"
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            data = re.findall("\d{11}", str(data))
            time.sleep(1)
            data = data[0]
            return data
        else:
            return "Error Getting Account, Please check your repo"



    def GetBindCode(self,number,res):
        for i in range(0,32,+1):
            time.sleep(2)
            path = "/getQueue?token="+res+""
            conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
            if response.status == 200:
                data = response.read()
                if data.startswith('MSG'):
                    break
            else:
                return "Error Getting Account, Please check your repo"
        data = data.decode('GBK')
        print(data)
        res = re.findall(r"MSG&153&"+number+"&(.+?)\[End]", data)
        res = re.findall("\d{4}",res[0])
        print(res[0])
        return res[0]


    def UploadPhoneNumber(self, number, token):
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
