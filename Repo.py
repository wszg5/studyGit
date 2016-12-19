# coding:utf-8
import httplib, json

class Repo:

    def __init__(self):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}
        self.domain = "127.0.0.1"
        self.port = 8888

    @staticmethod
    def GetAccount(cateId, interval, limit):
        path = "/repo/account/get?cate_id=" + cateId + "&interval=" + interval + "&limit=" + limit;
        conn = httplib.HTTPConnection(Repo.domain)

        conn.request("GET", path, "", Repo.headers)
        response = conn.getresponse()
        if response.status == 200:
            usersdata = response.read()
            user = json.loads(usersdata)

        else:
            print "Error sending message,check your account"


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
