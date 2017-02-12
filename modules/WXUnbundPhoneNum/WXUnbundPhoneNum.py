# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class WXUnbundPhoneNum:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(4)
        d(text='我').click()
        d(text='设置').click()
        d(textContains='帐号与安全').click()
        d(text='手机号').click()
        d(description='更多').click()
        d(text='解绑手机号').click()
        d(text='解绑').click()
        if d(text='提示').exists:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"这是唯一绑定，无法解绑\"" ).communicate()
            d(text='确定').click()


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXUnbundPhoneNum

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"time_delay": "3"};   #cate_id是仓库号，length是数量
    o.action(d,z, args)
