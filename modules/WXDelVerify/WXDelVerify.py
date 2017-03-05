# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXDelVerify:
    def __init__(self):
        self.repo = Repo()
    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(7)
        d(text='通讯录').click()
        d(className='android.widget.ListView').child(className='android.widget.RelativeLayout',index=1).child(className='android.widget.RelativeLayout',index=0).click()   #点击新的朋友

        obj = d(className='android.widget.RelativeLayout', index=1).child(index=1).child(className='android.widget.TextView', index=0)     #得到微信名
        while obj.exists:
            obj.long_click()
            d(text='删除').click()
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXDelVerify
if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()


    args = {"time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)