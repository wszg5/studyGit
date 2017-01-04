# coding:utf-8
import httplib, json
import time
import re


class XunMa640:

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
            return data
        else:
            return "Error Getting Account, Please check your repo"

        #ip = 640
    def GetPhoneNumber(self, token, ip):
        path = "/getPhone?ItemId="+ip+"&token=" + token + "&Count=1"
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

        # ip = 144
    def UploadPhoneNumber(self, number, token):

        path = "/getPhone?ItemId=144&token=" + token + "&Phone="+number+""
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            data = data.decode('GBK')
            if len(data) == 12:
                return data
            else:
                return 0
        else:
            return "Error Getting Account, Please check your repo"


    def GetCode(self, number, token):

        for i in range(0, 70, +1):
            time.sleep(1)
            path = "/getQueue?token=" + token + ""
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
        if data.startswith('MSG'):

            data = data.decode('GBK')
            res = re.findall(r"MSG&144&" + number + "&(.+?)\[End]", data)
            res = re.findall("\d{6}", res[0])
            return res[0]
        else:
            return ""





if __name__ == '__main__':
    xunma640 = XunMa640()