# coding:utf-8
import httplib, json
from const import const



class Repo:

    def __init__(self):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}
        self.domain = const.REPO_API_IP
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



    def GetMaterial(self, cateId, interval,limit,wid=''):
        path = "/repo_api/material/pick?status=normal&cate_id=%s&interval=%s&limit=%s&wid=%s" % (cateId,interval,limit,wid)
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
            return None



    def BackupInfo(self,cateId,status,Number,remark):           #仓库号，状态，QQ号，备注设备id_卡槽id
        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&cardslot=%s" % (cateId,status,Number,remark)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET",path)


    def RegisterAccount(self,qqNumber,password,phomeNumber, numberCateId):
        path = "/repo_api/register/numberInfo?QQNumber=%s&QQPassword=%s&PhoneNumber=%s&cate_id=%s" % (qqNumber,password,phomeNumber,numberCateId)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET",path)


    def uploadPhoneNumber(self, phomeNumber, numberCateId):
        path = "/repo_api/screen/numberInfo?PhoneNumber=%s&cate_id=%s" % (phomeNumber, numberCateId)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)




if __name__ == '__main__':
    repo = Repo()
    result = repo.GetAccount("6", 120, 1)
    # result = repo.SetAccount("6", "ddkf", "1918697054")

    # result = repo.GetMaterial("8",120,1)
    print(result)
    # print(result[0]["content"])
    # result1 = repo.GetNumber("13",0,10)              #意思是取13号仓库2小时内没有用过的号码，一次取16个
    # print(result1[0])

    # print (result[0])
    # print  result[0]["content"]
    # print (result)
    # print (result[0]['number'])
    # print(result[0]["password"])