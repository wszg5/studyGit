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



    def action(self, d, args):

        d.server.adb.cmd("shell", "am force-stop com.tencent.qqlite").wait()  # 将qq强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity").wait()  # 将qq拉起来
        d(text='联系人').click()
        d(text='通讯录').click()
        d(text='启用').click()
        token = self.xuma.GetToken()
        phoneNumber = self.xuma.QQLiteGetPhoneNumber(token)
        print(phoneNumber)
        d(text='请输入你的手机号码',resourceId='com.tencent.qqlite:id/0').set_text(phoneNumber)
        d(text='下一步',resourceId='com.tencent.qqlite:id/0').click()
        code = self.xuma.GetCode(phoneNumber,token)
        d(text='请输入短信验证码',resourceId='com.tencent.qqlite:id/0').set_text(code)



        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return QQLiteStrUseAddressList

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A3SK00853")
    # d.dump(compressed=False)
    args = {"repo_material_id":"8","StartIndex":"0","EndIndex":"7","time_delay":"3"};
    o.action(d, args)