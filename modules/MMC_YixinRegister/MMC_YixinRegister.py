# coding:utf-8
from uiautomator import Device
from zservice import ZDevice
from smsCode import smsCode
from Repo import *
import time
from slot import Slot


class MMCYixinRegister:

    def __init__(self):
        self.repo = Repo( )
        self.scode = None
        self.slot = Slot( 'yixin' )

    def registerWithSlot(self, d, z, args):

        self.scode = smsCode( d.server.adb.device_serial( ) )


        # phoneNumber = self.repo.GetNumber(scode_cateId,0,1)
        # if len(phoneNumber)==0:
        #     oh='oh'


        phoneNumber = self.scode.GetPhoneNumber( self.scode.QQ_REGISTER )
        print phoneNumber
        time.sleep( 2 )

        vertifyCode = self.scode.GetVertifyCode( phoneNumber, self.scode.QQ_REGISTER )  # 获取验证码

    def action(self, d, z, args):

        self.registerWithSlot(d,z,args)

    def swipe(self, d):
        time.sleep( 3 )
        for k in range( 1, 35 ):
            time.sleep( 1 )
            if d( className='android.widget.TextView', text='熟悉的QQ习惯' ).exists:
                str = d.info  # 获取屏幕大小等信息
                height = str["displayHeight"]
                width = str["displayWidth"]
                for i in range( 0, 2 ):
                    d.swipe( width * 0.75, height * 0.5, width * 0.05, height * 0.5, 10 )
                    time.sleep( 1 )
                d( className='android.widget.Button', text='立即体验' ).click( )
                break

        if k == 34:
            return False
        time.sleep( 2 )


def getPluginClass():
    return MMCYixinRegister

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"repo_cate_id":"113",'number_count':'20',"random_name":"是","clear":"是","time_delay":"3","set_timeStart":"0","set_timeEnd":"0","startTime":"0","endTime":"8",
            "repo_material_cate_id":"255","add_count":"100"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
