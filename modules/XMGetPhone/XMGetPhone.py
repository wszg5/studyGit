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
        d.press.home()
        self.scode = smsCode( d.server.adb.device_serial( ) )
        while True:
            z.sleep(10)
            PhoneNumber = self.scode.GetPhoneNumber( self.scode.WECHAT_REGISTER )  # 获取接码平台手机号码
            self.scode.defriendPhoneNumber( PhoneNumber, self.scode.WECHAT_REGISTER )
            z.sleep(5)
            cateId = args['repo_number_id']
            self.repo.uploadPhoneNumber(PhoneNumber, cateId)




def getPluginClass():
    return XMGetPhone

if __name__ == "__main__":
    import sys
    reload( sys )
    sys.setdefaultencoding( 'utf8' )

    clazz = getPluginClass()
    o = clazz()
    d = Device("916c6fd5")#INNZL7YDLFPBNFN7
    z = ZDevice("916c6fd5")
    # z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    'dingdingdingdingdindigdingdingdingdingdingdingdingdingdingdingdingdignin'
    args = {"repo_number_id": "181",}  # cate_id是仓库号，发中文问题
    o.action(d,z, args)









