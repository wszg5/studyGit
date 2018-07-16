# coding:utf-8
from smsCode.client_suma import client_suma
from uiautomator import Device
from Repo import *
from smsCode import smsCode
import time, string, random
from zservice import ZDevice
from slot import Slot


class SMGetPhone:
    def __init__(self):
        self.repo = Repo()
        self.xm = None
        self.cache_phone_key = 'cache_phone_key'

    def action(self, d,z, args):
        self.scode = client_suma()
        runLock = int(args['run_lock'])
        cateId = args['repo_number_id']
        totalList = self.repo.GetNUmberNormalTotal(cateId)
        normalTotal = int(totalList[0]['total'])

        count = 1
        while normalTotal < runLock:
            if count > int(args['get_amount']):
                break
            PhoneNumber = self.scode.GetPhoneNumber(8336)  # 获取接码平台手机号码
            time.sleep(10)
            self.scode.defriendPhoneNumber(PhoneNumber, 8336)  # 拉黑
            self.repo.uploadPhoneNumber(PhoneNumber, cateId)  # 入库
            count = count + 1





def getPluginClass():
    return SMGetPhone

if __name__ == "__main__":
    import sys
    reload( sys )
    sys.setdefaultencoding( 'utf8' )

    clazz = getPluginClass()
    o = clazz()
    d = Device("465b4e4b")#INNZL7YDLFPBNFN7
    z = ZDevice("465b4e4b")
    # z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id": "361", "run_lock":"50000","get_amount":"50000","time_delay":"5"}  # cate_id是仓库号，发中文问题
    o.action(d,z, args)










