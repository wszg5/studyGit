# coding:utf-8
import os
import random
from zcache import cache
from uiautomator import Device
from Repo import *

from zservice import ZDevice


class OpenFlightMode:
    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )

    def action(self, d, z, args):
        z.toast( "开始执行：打开飞行模式模块" )

        d.server.adb.cmd( "shell", "settings put global airplane_mode_on 1" ).communicate( )
        d.server.adb.cmd( "shell",
                          "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true" ).communicate( )
        z.sleep( 3 )
        d.server.adb.cmd("shell", "settings put global airplane_mode_on 0").communicate()
        d.server.adb.cmd("shell",
                          "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false").communicate()
        z.sleep(3)

        z.setModuleLastRun_new(self.mid)
        z.toast('模块结束，保存的时间是%s' % datetime.datetime.now().now.strftime('%Y-%m-%d %H:%M:%S'))

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))



def getPluginClass():
    return OpenFlightMode

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("7HQWC6U8A679SGAQ")
    z = ZDevice("7HQWC6U8A679SGAQ")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"time_delay": "3"}
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












