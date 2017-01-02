# coding:utf-8
from uiautomator import Device
from Repo import *
from XunMa import *
import os, uuid, datetime, random
import time
import math
import json
from uiautomator import Device, AutomatorDeviceUiObject
import traceback

class QQLiteStrUseAddressList:
    def __init__(self):
        self.repo = Repo()
        self.xuma = XunMa()



    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        d(resourceId='android:id/tabs',className='android.widget.TabWidget').child(className='android.widget.FrameLayout',index='1').click()
        d(text='启用').click()
        token = self.xuma.GetToken()
        GetBindNumber = self.xuma.GetBindNumber(token)
        print(GetBindNumber)
        d(text='请输入你的手机号码',resourceId='com.tencent.qqlite:id/0').set_text(GetBindNumber)
        d(text='下一步',resourceId='com.tencent.qqlite:id/0').click()
        code = self.xuma.GetCode(GetBindNumber,token)
        d(text='请输入短信验证码',resourceId='com.tencent.qqlite:id/0').set_text(code)



        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return QQLiteStrUseAddressList

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    # d.dump(compressed=False)
    args = {"repo_material_id":"8","StartIndex":"0","EndIndex":"7","time_delay":"3"};
    z = 0
    o.action(d,z, args)