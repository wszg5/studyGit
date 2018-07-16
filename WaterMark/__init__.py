# coding:utf-8
import httplib, json
import urllib
import time, datetime

import logging

from const import const
class WaterMark:
    def __init__(self):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}
        self.domain = const.REPO_API_IP
        self.port = None

    def PostInformation(self, cateId, data):
        data["cateId"] = cateId
        path = "/repo_api/checkDeposit/checkDepositInfo"
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Connection": "Keep-Alive"};
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        params = urllib.urlencode( data )
        conn.request( method="POST", url=path, body=params, headers=headers )
        # 返回处理后的数据
        response = conn.getresponse( )
        # 判断是否提交成功
        # if response.status == 302:
        #     print ("发布成功!^_^!")
        # else:
        #     print ("发布失败\^0^/")
        #     # 关闭连接
        conn.close( )

    def GetTIMInfomation(self, cateId, data):  # TIM模块从治疗库获取数据
        data["cateId"] = cateId
        path = "/repo_api/TIMInformation/getInfoByNumAndX"
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Connection": "Keep-Alive"};
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        params = urllib.urlencode( data )
        conn.request( method="POST", url=path, body=params, headers=headers )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def PostStatus(self, cateId, status, Number):  # 仓库号，状态，QQ号，备注设备id_卡槽id
        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s" % (cateId, status, Number)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )

    def GetAccount(self,status, cateId, interval, limit):
        path = "/repo_api/account/pick?status=%s&cate_id=%s&interval=%s&limit=%s" % (status,cateId, interval, limit)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def GetMaterial(self, cateId, interval, limit, wid=''):  # wid是用来发微信朋友圈的
        path = "/repo_api/material/pick?status=normal&cate_id=%s&interval=%s&limit=%s&wid=%s" % (
        cateId, interval, limit, wid)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def GetNumber(self, cateId, interval, limit, status='normal', statusLock='YES', number=None, name=None):
        path = "/repo_api/number/pick?status=%s&cate_id=%s&interval=%s&limit=%s&statusLock=%s&number=%s&name=%s" % (
        status, cateId, interval, limit, statusLock, number, name)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def Getserial(self, cateId, cardslot):  # 根据卡槽号和设备号得到串号
        path = "/repo_api/account/IMEIInfo?status=normal&cate_id=%s&cardslot=%s" % (cateId, cardslot)
        print('地址是%s' % path)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def GetWXRegisterPhoneNumber(self, cateId):  # 微信注册从治疗库获取手机号码
        path = "/repo_api/WXInformation/getPhoneNumber?cate_id=%s" % (cateId)
        print('地址是%s' % path)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def getInformationByGender(self, cate_id, gender):  # 根据性别获取资料库素材
        path = "/repo_api/WXInformation/getInformationList?cate_id=%s&gender=%s" % (cate_id, gender)
        print('地址是%s' % path)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def BackupInfo(self, cateId, status, Number, IMEI, remark):  # 仓库号，状态，QQ号，备注设备id_卡槽id
        # path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (cateId,status,Number,IMEI,remark)
        # conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        # conn.request("GET",path)
        data = {"cate_id": cateId, "status": status, 'Number': Number, 'IMEI': IMEI, "cardslot": remark}
        path = "/repo_api/account/statusInfo"
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Connection": "Keep-Alive"};
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        params = urllib.urlencode( data )
        conn.request( method="POST", url=path, body=params, headers=headers )
        conn.close( )

    def UpdateYXsmsNumber(self, cateId, phoneNumber, smsNumber):  # 仓库号，易信帐号，免费短信数量
        # path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (cateId,status,Number,IMEI,remark)
        # conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        # conn.request("GET",path)
        data = {"cate_id": cateId, "phoneNumber": phoneNumber, 'smsNumber': smsNumber}
        path = "/repo_api/account/YXsmsNumber"
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Connection": "Keep-Alive"};
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        params = urllib.urlencode( data )
        conn.request( method="POST", url=path, body=params, headers=headers )
        conn.close( )

    def GetDesignationAccount(self, qqNumber, numberCateId):
        path = "/repo_api/account/getAccountNumber?QQNumber=%s&cate_id=%s" % (qqNumber, numberCateId)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def RegisterAccount(self, qqNumber, password, phoneNumber, numberCateId, status='normal', IMEI=None, remark=None):
        # path = "/repo_api/register/numberInfo?QQNumber=%s&QQPassword=%s&PhoneNumber=%s&cate_id=%s" % (qqNumber,password,phoneNumber,numberCateId)
        # conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        # conn.request("GET",path)
        data = {"QQNumber": qqNumber, "QQPassword": password, 'PhoneNumber': phoneNumber, 'cate_id': numberCateId,
                'status': status, 'IMEI': IMEI, "cardslot": remark}
        path = "/repo_api/register/numberInfo"
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Connection": "Keep-Alive"};
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        params = urllib.urlencode( data )
        conn.request( method="POST", url=path, body=params, headers=headers )
        conn.close( )

    def RegisterWOEMailAccount(self, qqNumber, password, phoneNumber, numberCateId, status='normal', IMEI=None,
                               remark=None):
        # path = "/repo_api/register/numberInfo?QQNumber=%s&QQPassword=%s&PhoneNumber=%s&cate_id=%s" % (qqNumber,password,phoneNumber,numberCateId)
        # conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        # conn.request("GET",path)
        data = {"QQNumber": qqNumber, "QQPassword": password, 'PhoneNumber': phoneNumber, 'cate_id': numberCateId,
                'status': status, 'IMEI': IMEI, "cardslot": remark}
        path = "/repo_api/register/numberInfo"
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Connection": "Keep-Alive"};
        conn = httplib.HTTPConnection( '192.168.1.51', '8686', timeout=30 )
        params = urllib.urlencode( data )
        conn.request( method="POST", url=path, body=params, headers=headers )
        conn.close( )

    def uploadPhoneNumber(self, phoneNumber, numberCateId, guolv='N'):
        path = "/repo_api/screen/numberInfo?PhoneNumber=%s&cate_id=%s&guolv=%s" % (phoneNumber, numberCateId, guolv)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )

    def uploadNumberALiPay(self, phoneNumber, numberCateId, status):  # 支付宝检测手机号模块专用接口
        path = "/repo_api/checkalipay/updateNumberInfo?PhoneNumber=%s&cate_id=%s&status=%s" % (
        phoneNumber, numberCateId, status)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )

    def savePhonenumberXM(self, phoneNumber, cateid, status, name=None):  # 迅码上传失效/有效的手机号
        path = "/repo_api/check/numberInfo?PhoneNumber=%s&cate_id=%s&status=%s&name=%s" % (
        phoneNumber, cateid, status, name)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )

    def GetInformation(self, cateId, phoneNumber=''):
        path = "/repo_api/WXInformation/getPhoneNumber?cate_id=%s&phoneNumber=%s" % (cateId, phoneNumber)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def GetInformationByDevice(self, cateId, deviceId=''):
        path = "/repo_api/WXInformation/getDeviceInfo?cate_id=%s&device_id=%s" % (cateId, deviceId)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def GetTrueAnswer(self, data):
        path = "/repo_api/WXInformation/getTrueAnswer"
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Connection": "Keep-Alive"};
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        params = urllib.urlencode( data )
        conn.request( method="POST", url=path, body=params, headers=headers );
        # 返回处理后的数据
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def GetNUmberNormalTotal(self, cateId, cateType='number'):
        path = "/repo_api/number/GetStatusTotal?cate_id=%s&cate_type=%s" % (cateId, cateType)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def GetPhantomJSTaskInfo(self,taskType):
        path = "/repo_api/InformationTaskCate/getInfoList?taskType=%s" % taskType
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def GetPhantomJSParamInfo(self,taskType):
        path = "/repo_api/InformationParamCate/getInfoList?taskType=%s" % taskType
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def GetSpecifiedPhantomJSTask(self, taskId,taskType):
        path = "/repo_api/InformationTaskCate/getSpecifiedTask?taskId=%s&taskType=%s" % (taskId,taskType)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def UpdateNumberStauts(self, number, cateId, status):
        path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (number, cateId, status)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )


    def AccountFrozenTimeDelay(self, number, cateId):
        path = "/repo_api/account/timeDelay?number=%s&cate_id=%s" % (number, cateId)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )



    def DeleteInformation(self, cateId, phoneNumber):
        path = "/repo_api/WXInformation/DelInformation?cate_id=%s&phoneNumber=%s" % (cateId, phoneNumber)
        conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        conn.request( "GET", path )

    def timeCompare(self, start_time, stop_time):
        nowtime = datetime.datetime.now( ).strftime( '%H:%M' )  # 将日期转化为字符串 datetime => string
        if start_time == "" or stop_time == "":
            return False
        if not ":" in start_time:
            start_time = start_time + ":00"
        if not ":" in stop_time:
            stop_time = stop_time + ":00"
        if time.strptime( start_time, '%H:%M' ) < time.strptime( stop_time, '%H:%M' ):
            if time.strptime( start_time, '%H:%M' ) < time.strptime( nowtime, '%H:%M' ) < time.strptime( stop_time,
                                                                                                         '%H:%M' ):
                return True
            else:
                return False
        else:
            if time.strptime( start_time, '%H:%M' ) < time.strptime( nowtime, '%H:%M' ) < time.strptime( "23:59",
                                                                                                         '%H:%M' ) or time.strptime(
                "00:00", '%H:%M' ) < time.strptime( nowtime, '%H:%M' ) < time.strptime( stop_time, '%H:%M' ):
                return True
            else:
                return False


if __name__ == '__main__':
    repo = Repo()
    repo.GetSpecifiedPhantomJSTask("8","290")
    # result = repo.PostInformation({"aaa":"aa"})
    # saveCate = '189'
    # phoneNumber = '13642744049'
    # trues = repo.GetTrueAnswer(saveCate,phoneNumber,'132','456','147','','365')
    # true = trues[0]['x07']
    #
    # para = {"phoneNumber": '13094702352', 'x_01': "not_exist", 'x_19': 'WXRegister'}
    # repo.PostInformation( saveCate, para )
    # result = repo.SetAccount("6", "ddkf", "1918697054")
    # result = repo.GetMaterial("8",120,1)
    #
    # print(result[0]["content"])
    # result1 = repo.GetNumber("13",0,10)              #意思是取13号仓库2小时内没有用过的号码，一次取16个
    # print(result1[0])
    print( '' )
    # print (result[0])
    # print  result[0]["content"]
    # print (result)
    # print (result[0]['number'])
    # print(result[0]["password"])