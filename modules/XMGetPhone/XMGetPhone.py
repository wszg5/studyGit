# coding:utf-8
from uiautomator import Device
from Repo import *
from smsCode import smsCode
import time, string, random
from zservice import ZDevice
from slot import Slot


class XMGetPhone:
    def __init__(self):
        self.repo = Repo()
        self.xm = None
        self.cache_phone_key = 'cache_phone_key'

    def action(self, d,z, args):
        z.heartbeat()
        d.press.home( )
        self.scode = smsCode(d.server.adb.device_serial())
        runLock = int(args['run_lock'])
        cateId = args['repo_number_id']
        totalList = self.repo.GetNUmberNormalTotal(cateId)
        normalTotal = int(totalList[0]['total'])

        if normalTotal < runLock:
            z.toast('库内未使用号码低于'+args['run_lock']+'，开始拉号码')
        else:
            z.toast( '库内未使用号码大于' + args['run_lock'] + '，模块无法运行' )

        count = 1
        while normalTotal < runLock:
            if count > int(args['get_amount']):
                z.toast('成功拉取'+args['get_amount'])
                break
            PhoneNumber = self.scode.GetPhoneNumber( self.scode.WECHAT_REGISTER )  # 获取接码平台手机号码
            z.sleep(5)
            self.scode.defriendPhoneNumber( PhoneNumber, self.scode.WECHAT_REGISTER )#拉黑
            self.repo.uploadPhoneNumber(PhoneNumber, cateId)#入库
            if (args["time_delay"]):
                z.sleep(int(args["time_delay"]))
            count = count + 1;





def getPluginClass():
    return XMGetPhone

if __name__ == "__main__":
    import sys
    reload( sys )
    sys.setdefaultencoding( 'utf8' )

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A1SK02114")#INNZL7YDLFPBNFN7
    z = ZDevice("HT4A1SK02114")
    # z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id": "280", "run_lock":"500","get_amount":"100","time_delay":"10"}  # cate_id是仓库号，发中文问题
    o.action(d,z, args)









