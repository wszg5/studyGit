# coding:utf-8
from uiautomator import Device
from Repo import *
from XunMa import *
import os, uuid, datetime, random
import time
import math
import json
from dbapi import *
from uiautomator import Device, AutomatorDeviceUiObject
from zservice import ZDevice

class QQLiteStrUseAddressList:
    def __init__(self):
        self.repo = Repo()
        self.xuma = XunMa()
        self.dbapi = dbapi()


    def action(self, d,z, args):
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        time.sleep(2)
        wait = 1
        while wait==1:
            time.sleep(5)
            obj =  d(resourceId='android:id/tabs', index=2).child(className='android.widget.FrameLayout', index=1).child(className='android.widget.RelativeLayout', index=0)
            if obj.exists:
                time.sleep(1)
                obj.click()
            else:
                d(resourceId='android:id/tabs', index=3).child(className='android.widget.FrameLayout', index=1).child(
                    className='android.widget.RelativeLayout', index=0).click()
            time.sleep(2)
            if d(text='联系人',resourceId='com.tencent.mobileqq:id/ivTitleName').exists:       #让它不停的点击
                wait = 0
        time.sleep(2)

        if d(resourceId='com.tencent.mobileqq:id/elv_buddies',index=1).child(index=10).exists:           #刚点进联系人界面看不到联系人的情况，需滑动
            d.swipe(width / 2, height * 2 / 4, width / 2, height / 4)
            d(resourceId='com.tencent.mobileqq:id/group_item_layout', index=10,className='android.widget.RelativeLayout').click()
        else:
            time.sleep(1)
            d(resourceId='com.tencent.mobileqq:id/group_item_layout',index=8,className='android.widget.RelativeLayout').click()




            newStart = 1
            while newStart == 1:
                token = self.xuma.GetToken()
                try:
                    GetBindNumber = self.xuma.GetBindNumber(token)

                except Exception:
                    continue

                print(GetBindNumber)
                time.sleep(2)
                d(resourceId='com.tencent.mobileqq:id/name',className='android.widget.EditText').set_text(GetBindNumber)

                time.sleep(1)
                d(text='下一步').click()
                time.sleep(1)
                if d(text='确定',resourceId='com.tencent.mobileqq:id/name',index='2').exists:
                    d(text='确定', resourceId='com.tencent.mobileqq:id/name', index='2').click()


                try:
                    code = self.xuma.GetBindCode(GetBindNumber, token)
                    newStart = 0
                except Exception:
                    continue
            d(resourceId='com.tencent.mobileqq:id/name',className='android.widget.EditText').set_text(code)
            d(text='完成',resourceId='com.tencent.mobileqq:id/name').click()




        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return QQLiteStrUseAddressList

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # d.dump(compressed=False)
    args = {"repo_material_id":"8","StartIndex":"0","EndIndex":"7","time_delay":"3"};
    z = 0
    o.action(d,z, args)