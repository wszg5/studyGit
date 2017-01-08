# coding:utf-8
import httplib, json
import time
import re

class XunMa:

    def __init__(self):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}

        self.domain = "api.xunma.net"
        self.port = 8080

    def GetToken(self):
        path = "/Login?uName=powerman&pWord=13141314&Developer=apFsnhXLxQG5W0AWiDhr%2fg%3d%3d"
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            return  data
        else:
                return "Error Getting Account, Please check your repo"


    def GetPhoneNumber(self,res):
        path = "/getPhone?ItemId=144&token="+res+"&Count=1"
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            data = re.findall("\d{11}", str(data))
            data = data[0]
            return data
        else:
            return "Error Getting Account, Please check your repo"

    def GetCode(self,number,res):
        for i in range(0,32,+1):
            time.sleep(2)
            path = "/getQueue?token="+res+""
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
        res = re.findall(r"MSG&153&"+number+"&(.+?)\[End]", data)
        res = re.findall("\d{4}",res[0])
        print(res[0])
        return res[0]





if __name__ == '__main__':
    xunma = XunMa()
    # a = xunma.GetToken()
    # b = xunma.GetPhoneNumber(a)
    # a = xunma.GetCode(b,a)
    # result = repo.GetAccount("6", 120, 1)
    # result = repo.SetAccount("6", "ddkf", "1918697054")

    # result = repo.GetMaterial("8",120,1)
    # result = repo.GetNumber("13",0,1)              #意思是取13号仓库2小时内没有用过的号码，一次取16个
