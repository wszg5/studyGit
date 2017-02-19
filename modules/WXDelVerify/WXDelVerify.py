# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class WXDelVerify:
    def __init__(self):
        self.repo = Repo()
    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()  # 将微信拉起来
        time.sleep(7)
        d(text='通讯录').click()
        if d(text='新的朋友').exists:
            d(text='新的朋友').click()
            time.sleep(1)
        else:
            d(text='群聊').up(className='android.widget.LinearLayout',index=0).click()     #效率较低，看是否有提升空间
            time.sleep(2)

        obj = d(className='android.widget.RelativeLayout', index=1).child(index=1).child(className='android.widget.TextView', index=0)     #得到微信名
        while obj.exists:
            obj.long_click()
            d(text='删除').click()
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXDelVerify
if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)