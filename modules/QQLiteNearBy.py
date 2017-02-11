# coding:utf-8
# wxApp.py
import math
import time
from uiautomator import Device
from Repo import *
import os, uuid, datetime, random


class QQLiteNearBy:
    def __init__(self):
        self.repo = Repo()


    def action(self, d, args):
        cate_id = args["repo_material_id"]
        numbers = self.repo.GetMaterial(cate_id, 0, 1)
        print(numbers)
        wait = 1
        while wait==1:                   #判断仓库是否有东西
            try:
                repo_material_content = numbers[0]['content']
                wait=0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到号码\"")
        import time
        str = d.info  # 获取屏幕大小等信息
        print (str)
        height = str["displayHeight"]
        width = str["displayWidth"]
        print (height)  # 屏幕的款
        print(width)  # 屏幕的高
        d.server.adb.cmd("shell", "am force-stop com.tencent.qqlite").wait()  # 将qq强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity").wait()  # 将qq拉起来
        time.sleep(1)
        d(text='我', index=0, className='android.widget.TextView').click()
        time.sleep(1)
        d(text='我', index=0, className='android.widget.TextView').click()
        d(text='附近的人').click()
        d(resourceId='com.tencent.qqlite:id/ivTitleBtnRightImage').click()
        time.sleep(1)
        d(text='筛选附近的人').click()


        Appeartime = args["Appeartime"]
        d(text=Appeartime).click()
        time.sleep(1)
        gender = args["gender"]
        print(gender)
        d(text='' + gender + '').click()  # 性别
        time.sleep(1)
        d(text='年龄').click()
        time.sleep(1)
        age = args["age"]
        if d(text=age).exists:  # True if exists, else Falsegit
            d(text=age).click()  # 由外界设定
            d(text='完成').click()
        else:
            d.swipe(width / 2, height * 1 / 2, width / 2, height / 4);
            time.sleep(1)
            d(text=age).click()  # 由外界设定
            d(text='完成').click()
            time.sleep(1)
        d(text='职业').click()
        time.sleep(2)
        profession = args["profession"]
        if d(text=profession, resourceId='com.tencent.qqlite:id/0').exists:
            time.sleep(2)
            d(text=profession, resourceId='com.tencent.qqlite:id/0').click()
            time.sleep(2)
        else:
            d.swipe(width / 2, height * 1 / 2, width / 2, height / 4, 10)
            time.sleep(2)
            d(text=profession, resourceId='com.tencent.qqlite:id/0').click()
        d(text='完成').click()
        time.sleep(3)
        global list
        list = list()
        StartIndex = int(args['StartIndex'])
        EndIndex = int(args['EndIndex'])
        i = StartIndex  # 点击第i个人
        t = StartIndex  # t是结束条件
        while i < EndIndex:
            if t < EndIndex:
                try:
                    d(className='android.widget.RelativeLayout', clickable='true', index=i).click()  # 点击屏幕的第i个人
                    obj = d(resourceId='com.tencent.qqlite:id/0', index=0,className='android.widget.TextView')  # 获得第i个人的所有信息
                    obj = obj.info
                    print (obj)
                    obj1 = obj["text"]  # 要保存到集合唯一标志
                    print (obj1)
                    if obj1 in list:
                        i = i + 1
                        print (i)
                        d(resourceId='com.tencent.qqlite:id/ivTitleBtnLeft', description='向上导航').click()
                        continue
                    else:
                        list.append(obj1)
                    d(text='发消息', className='android.widget.TextView').click()
                    d(resourceId='com.tencent.qqlite:id/input', className='android.widget.EditText',
                      description='文本框  连按两次来编辑').set_text(repo_material_content)  # 发中文问题
                    d(text='发送', resourceId='com.tencent.qqlite:id/fun_btn').click()
                    t = t + 1
                    i = i + 1
                    d(resourceId='com.tencent.qqlite:id/ivTitleBtnLeft', description='向上导航').click()
                    time.sleep(1)
                    d(resourceId='com.tencent.qqlite:id/ivTitleBtnLeft', description='向上导航').click()

                except Exception:
                    if d(text='显示更多', resourceId='com.tencent.qqlite:id/0').exists:
                        d(text='显示更多', resourceId='com.tencent.qqlite:id/0').click()
                        d.swipe(width / 2, height * 3 / 5, width / 2, height / 5)
                        d.swipe(width / 2, height * 3 / 5, width / 2, height / 5)
                        i = 1
                        time.sleep(3)
                    elif d(text='暂无更多附近的人', resourceId='com.tencent.qqlite:id/0'):
                         return  # 放到方法里要改为结束方法
                    else:
                        d.swipe(width / 2, height * 3 / 5, width / 2, height / 5)
                        d.swipe(width / 2, height * 3 / 5, width / 2, height / 5)
                        i = 1
                        time.sleep(2)
            else:
                return  # 放到代码里改为结束方法

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))
def getPluginClass():
    return QQLiteNearBy

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A3SK00853")
    # d.dump(compressed=False)              #显示详细信息
    args = {"repo_material_id":"8","gender":"全部","Appeartime":"4小时","age":"35岁以上","StartIndex":"1","EndIndex":"7","profession":"学生"} #别忘了加要发送的消息
    o.action(d, args)