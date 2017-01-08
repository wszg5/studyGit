# coding:utf-8
import threading
import time
from PIL import Image
from uiautomator import Device
import os,re,subprocess
from Repo import *
from zservice import ZDevice
import time, datetime, random
class EIMAddFriends:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):


        add_count = int(args['add_count'])  # 要添加多少人

        repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        wait = 1
        while wait == 1:
            numbers = self.repo.GetNumber(repo_number_cate_id, 120, add_count)  # 取出add_count条两小时内没有用过的号码
            if len(numbers)==0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到号码\"").communicate()
                time.sleep(5)
                continue

            wait = 0

        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)


        d.server.adb.cmd("shell", "am force-stop com.tencent.eim").communicate()  # 强制停止   3001369923  Bn2kJq5l
        d.server.adb.cmd("shell", "am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(6)
        if d(resourceId='com.tencent.eim:id/name',description='发起多人聊天等功能').exists:
            d(resourceId='com.tencent.eim:id/name',description='发起多人聊天等功能').click()
        else:
            return 2
        d(text='加好友',resourceId='com.tencent.eim:id/name').click()
        d(text='添加好友',resourceId='com.tencent.eim:id/name').click()

        for i in range(0,add_count,+1):
            repo_material_cate_id = args["repo_material_cate_id"]
            Material = self.repo.GetMaterial(repo_material_cate_id, 0, 1)
            wait = 1  # 判断素材仓库里是否由素材
            while wait == 1:
                try:
                    material = Material[0]['content']  # 取出验证消息的内容
                    wait = 0
                except Exception:
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到验证消息\"").communicate()


            numbers = list[i]
            d(resourceId='com.tencent.eim:id/name',className='android.widget.EditText').set_text(numbers)
            d(text='查找',resourceId='com.tencent.eim:id/name',className='android.widget.Button').click()
            time.sleep(2)

            if d(text='查找',resourceId='com.tencent.eim:id/name',className='android.widget.Button').exists:            #该号码不存在的情况
                obj = d(className='android.widget.EditText', resourceId='com.tencent.eim:id/name').info                 #将文本框已有的东西删除重来
                obj = obj['text']
                lenth = len(obj)
                t = 0
                while t < lenth:
                    d.press.delete()
                    t = t + 1
                    continue
                continue

            d(text='加好友',resourceId='com.tencent.eim:id/txt').click()
            time.sleep(1)
            if d(text='加好友',resourceId='com.tencent.eim:id/txt').exists:                                             #拒绝被添加的情况
                d(text='返回',resourceId='com.tencent.eim:id/name').click()
                obj = d(resourceId='com.tencent.eim:id/name', className='android.widget.EditText').info
                obj = obj['text']
                lenth = len(obj)
                t = 0
                while t < lenth:
                    d.press.delete()
                    t = t + 1
                    continue
                continue

            if d(text='必填',resourceId='com.tencent.eim:id/name').exists:
                d(text='返回',resourceId='com.tencent.eim:id/ivTitleBtnLeft').click()
                d(text='返回',resourceId='com.tencent.eim:id/name').click()
                obj = d(className='android.widget.EditText', resourceId='com.tencent.eim:id/name').info  # 将文本框已有的东西删除重来
                obj = obj['text']
                lenth = len(obj)
                t = 0
                while t < lenth:
                    d.press.delete()
                    t = t + 1
                    continue
                continue



            obj = d(resourceId='com.tencent.eim:id/name',className='android.widget.EditText').info             #删除之前文本框的验证消息
            obj = obj['text']
            lenth = len(obj)
            t = 0
            while t<lenth:
                d.press.delete()
                t = t + 1
            time.sleep(1)
            d(className='android.widget.EditText',text='请输入验证信息').click()            #验证信息
            z.input(material)
            d(text='下一步',resourceId='com.tencent.eim:id/ivTitleBtnRightText').click()
            d(text='发送',resourceId='com.tencent.eim:id/ivTitleBtnRightText').click()
            d(text='添加好友', resourceId='com.tencent.eim:id/name').click()


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))
def getPluginClass():
    return EIMAddFriends

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell","ime set com.zunyun.qk/.ZImeService").communicate()

    # d.dump(compressed=False)
    args = {"repo_number_cate_id":"49","repo_material_cate_id":"33","add_count":"6","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)