# coding:utf-8
import os
import random
from zcache import cache
from uiautomator import Device
from Repo import *

from zservice import ZDevice


class OpenVPN:
    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath(__file__)

    def action(self, d, z, args):
        z.toast( u"开始执行：打开VPN模块" )

        d.server.adb.cmd( "shell", "am start -n com.expressvpn.vpn/.MainActivity" ).communicate( )  # 翻墙软件
        z.sleep(3)

        if d(resourceId='com.expressvpn.vpn:id/bob_power').exists:
            d(resourceId='com.expressvpn.vpn:id/bob_power').click()

        while not d( text='VPN is ON' ).exists:
            z.sleep( 3 )
            z.toast( u"等待翻墙成功。" )

        z.toast(u"成功翻墙。")
        z.setModuleLastRun_new(self.mid)
        z.toast(u'模块结束，保存的时间是%s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))



def getPluginClass():
    return OpenVPN

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("7HQWC6U8A679SGAQ")
    z = ZDevice("7HQWC6U8A679SGAQ")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"time_delay": "3"};
    o.action(d, z, args)
    # obj = d( className='android.widget.Button' )
    # if obj.exists:
    #     obj =  d( className='android.widget.Button' ).info["bounds"]
    #     left = obj["left"]
    #     bottom = obj["bottom"]
    #     top = obj["top"]
    #     d.click(left-88,bottom - (bottom - top)/2)
    #     if obj.exists:
    #         d( className='android.widget.Button' ).left( className="android.widget.EditText" ).click()
    #         z.input("123")
    # d.server.adb.cmd( "shell", "pm clear com.android.chrome" ).communicate( )  # 清除浏览器缓存
    #
    # d.server.adb.cmd( "shell", 'am start -a android.intent.action.VIEW -d  http://www.google.cn/' )












