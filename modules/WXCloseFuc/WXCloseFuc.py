# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WeiXinMass:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()  # 将微信拉起来
        time.sleep(4)
        d(text='我').click()
        d(text='设置').click()
        d(text='通用').click()
        d(text='功能').click()
        if d(textContains='邮箱提醒').exists:
            d(textContains='邮箱提醒').click()
            d(text='停用').click()
            if d(text='清空').exists:
                d(text='清空').click()
                while d(textContains='正在停用').exists:
                    time.sleep(2)
            if d(text='停用').exists:
                d(text='停用').click()
            if d(text='清空').exists:
                d(text='清空').click()
                while d(textContains='正在停用').exists:
                    time.sleep(2)
            d(description='返回').click()
            if d(textContains='微信').exists:
                d(text='我').click()
                d(text='设置').click()
                d(text='通用').click()
                d(text='功能').click()

        if d(textContains='离线助手').exists:
            d(textContains='离线助手').click()
            d(text='停用').click()
            if d(text='清空').exists:
                d(text='清空').click()
                while d(textContains='正在停用').exists:
                    time.sleep(2)
            d(description='返回').click()
            if d(textContains='微信').exists:
                d(text='我').click()
                d(text='设置').click()
                d(text='通用').click()
                d(text='功能').click()
        if d(text='腾讯新闻').exists:
            d(text='腾讯新闻').click()
            d(text='停用').click()
            if d(text='清空').exists:
                d(text='清空').click()
                while d(textContains='正在停用').exists:
                    time.sleep(2)
            d(description='返回').click()
            if d(textContains='微信').exists:
                d(text='我').click()
                d(text='设置').click()
                d(text='通用').click()
                d(text='功能').click()

        if d(text='语音记事本').exists:
            d(text='语音记事本').click()
            d(text='停用').click()
            d(text='清空').click()
            while d(textContains='正在停用').exists:
                time.sleep(2)
            d(description='返回').click()
            if d(textContains='微信').exists:
                d(text='我').click()
                d(text='设置').click()
                d(text='通用').click()
                d(text='功能').click()



        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return WeiXinMass

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()


    args = {"repo_material_id": "36","time_delay":"3",'gender':"不限",}    #cate_id是仓库号，length是数量
    o.action(d,z, args)






