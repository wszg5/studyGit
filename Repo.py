# coding:utf-8
import httplib, json

class Repo:

    def __init__(self):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}

        self.domain = "192.168.1.51"
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
            print "Error Getting Account, Please check your repo"


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
            print "Error Getting material, Please check your repo"


    def GetNumber(self, cateId, interval, limit):
        path = "/repo_api/number/pick?status=normal&cate_id=%s&interval=%s&limit=%s" % (cateId,interval,limit)
        #path = "/repo/number/get?status=normal&cate_id=" + cateId + "&interval=" + interval + "&limit=" + limit;
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)

        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            numbers = json.loads(data)
            return  numbers
        else:
            print "Error Getting Number, Please check your repo"


if __name__ == '__main__':
    repo = Repo()
    # result = repo.GetAccount("36", 120, 2)
    # result = repo.GetMaterial("8",120,1)
    result = repo.GetNumber("13",0,200)              #意思是取13号仓库2小时内没有用过的号码，一次取16个
    print  result[0]
    # print  result[0]["content"]
    # print result[0]["number"]
    # print result[0]["password"]
    print result