# coding:utf-8
import httplib, json

class Repo:

    def __init__(self):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}

        self.domain = "192.168.1.33"
        self.port = 8888


    def GetAccount(self, cateId, interval, limit):
        path = "/repo_api/account/pick?status=normal&cate_id=%s&interval=%s&limit=%s" % (cateId,interval,limit)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)

        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            numbers = json.loads(data)
            return  numbers
        else:
            return "Error Getting Account, Please check your repo"



    def GetMaterial(self, cateId, interval, limit):
        path = "/repo_api/material/pick?status=normal&cate_id=%s&interval=%s&limit=%s" % (cateId,interval,limit)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)

        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            numbers = json.loads(data)
            return  numbers
        else:
            return "Error Getting material, Please check your repo"



    def GetNumber(self, cateId, interval, limit):
        path = "/repo_api/number/pick?status=normal&cate_id=%s&interval=%s&limit=%s" % (cateId,interval,limit)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)

        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            numbers = json.loads(data)
            return  numbers
        else:
            return "Error Getting Number, Please check your repo"

    def SetAccount(self,cateId,status,QQNumber):
        path = "/repo_api/account/questionInfo?cate_id=%s&status=%s&QQNumber=%s" % (cateId,status,QQNumber)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET",path)



if __name__ == '__main__':
    repo = Repo()
    #result = repo.GetAccount("6", 120, 1)
    result = repo.SetAccount("6", "ddkf", "1918697054")

    # result = repo.GetMaterial("8",120,1)
    # result = repo.GetNumber("13",0,200)              #意思是取13号仓库2小时内没有用过的号码，一次取16个
    # print (result[0])
    # print  result[0]["content"]
    # print (result)
    # print (result[0]['number'])
    # print(result[0]["password"])