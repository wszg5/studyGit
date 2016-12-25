# coding:utf-8
from uiautomator import Device
from Repo import *
import os, uuid, datetime, random
import time
import math
import json
from uiautomator import Device, AutomatorDeviceUiObject
import traceback

class QQLiteAddressList:
    def __init__(self):
        self.repo = Repo()




    def action(self, d, args):
        cate_id = args["repo_material_id"]
        numbers = self.repo.GetMaterial(cate_id, 0, 1)
        wait = 1
        while wait==1:
            try:
                repo_material_id = numbers[0]['content']        #从素材库取出的要发的材料
                wait = 0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到号码\"")
        str = d.info  # 获取屏幕大小等信息
        print (str)
        # info= json.loads(str)
        height = str["displayHeight"]
        width = str["displayWidth"]
        print (height)  # 屏幕的款
        print(width)  # 屏幕的高
        time.sleep(2)
        d.server.adb.cmd("shell", "am force-stop com.tencent.qqlite").wait()  # 将qq强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity").wait()  # 将qq拉起来
        # print(d.dump(compressed=False))
        time.sleep(3)
        d(text='联系人').click()
        d(text='通讯录').click()
        if d(text="启用").exists:
            return
        time.sleep(1)
        if d(text="匹配通讯录").exists:
            d(text="匹配通讯录").click()
            time.sleep(4)
            print (123)
        StartIndex = int(args["StartIndex"])
        EndIndex = int(args["EndIndex"])
        global list
        list = list()
        t = StartIndex
        i = StartIndex
        while i < EndIndex:
            if t < EndIndex:
                obj = d(descriptionContains="发消息", descriptionStartsWith='向')  # 定位作用
                # count = obj.count  # 统计当前屏幕上的人数
                # print(count)
                try:
                    obj1 = obj[i].info  # 打印出第i行联系人的信息,报错则滑动
                    obj1 = obj1["contentDescription"]  # 要保存的唯一属性，向×××号码发消息
                    print (obj1)
                    if obj1 in list:
                        i = i + 1
                        print (i)
                        continue
                    else:
                        list.append(obj1)
                        obj[i].click()  # 直接进入发消息页面(不知道为什么)不需要再点击发消息，
                        time.sleep(1)
                        # d(text='发消息').click()
                        d(resourceId='com.tencent.qqlite:id/input', className='android.widget.EditText').set_text(repo_material_id)  # 发中文问题
                        d(text='发送', resourceId='com.tencent.qqlite:id/fun_btn').click()
                        time.sleep(2)
                        i = i + 1
                        t = t + 1
                        d(resourceId='com.tencent.qqlite:id/ivTitleBtnLeft', description='向上导航').click()
                        time.sleep(1)
                except Exception:
                    if d(text='未启用通讯录的联系人', description='未启用通讯录的联系人', resourceId='com.tencent.qqlite:id/0'):
                        return  # 这个要改成结束方法
                    d.swipe(width / 2, height * 3 / 5, width / 2, height / 5)
                    d.swipe(width / 2, height * 3 / 5, width / 2, height / 5)
                    # EndIndex = EndIndex-i
                    i = 0
                    continue
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return QQLiteAddressList

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49PSK05055")
    # d.dump(compressed=False)
    args = {"repo_material_id":"8","StartIndex":"0","EndIndex":"7","time_delay":"3"};
    o.action(d, args)