# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class TIMBrowserSendText:
    def __init__(self):
        self.repo = Repo()




    def action(self, d,z, args):
        totalNumber = int(args['totalNumber'])  # 要给多少人发消息

        repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        wait = 1
        while wait == 1:
            numbers = self.repo.GetNumber(repo_number_cate_id, 120, totalNumber)  # 取出add_count条两小时内没有用过的号码
            lenth = len(numbers)
            if "Error" in numbers:  #如果没有拿到号码的情况
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到号码\"").communicate()
                time.sleep(30)
                continue
            elif lenth==0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到号码\"").communicate()
                time.sleep(30)
                continue
            wait = 0

        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)

        # d.server.adb.cmd("shell", "pm clear com.android.chrome").wait()  # 清除缓存
        d.server.adb.cmd("shell", "am start -n com.android.chrome/com.google.android.apps.chrome.Main").communicate()  # 拉起来

        if d(description='清空号码',className='android.widget.Button').exists:
            for i in range (0,totalNumber,+1):
                repo_material_cate_id = args["repo_material_cate_id"]
                Material = self.repo.GetMaterial(repo_material_cate_id, 0, 1)
                wait = 1  # 判断素材仓库里是否由素材
                while wait == 1:
                    try:
                        material = Material[0]['content']  # 取出验证消息的内容
                        wait = 0
                    except Exception:
                        d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到验证消息\"").communicate()
                        time.sleep(30)
                        time.sleep(5)

                numbers = list[i]
                print(numbers)

                d(description='清空号码', className='android.widget.Button').click()
                time.sleep(1)
                d(className='android.widget.EditText',index=1,clickable='false').click()                     #点击输入框
                time.sleep(1)
                if d(className='android.widget.EditText',index=1,clickable='false').exists:              #看会不会弹出键盘
                    d(className='android.widget.EditText',index=1,clickable='false').set_text(numbers)
                else:
                    d.press.back()
                    d(className='android.widget.EditText',index=1,clickable='false').set_text(numbers)
                d(className='android.widget.Button',index=3,description='开始聊天').click()
                time.sleep(2)
                if d(className='android.widget.Button',index=3,description='开始聊天').exists:           #没有该ＱＱ的情况
                    continue
                time.sleep(1)
                d(resourceId='com.tencent.tim:id/input',className='android.widget.EditText').click()
                print(material)
                z.input(material)
                d(text='发送',resourceId='com.tencent.tim:id/fun_btn').click()
                d.server.adb.cmd("shell","am start -n com.android.chrome/com.google.android.apps.chrome.Main").communicate()  # 拉起来



        else:
            d.server.adb.cmd("shell","am start -a android.intent.action.VIEW -d http://www.jianli58.com/qq.html").communicate()  # 不在聊了页面时输入聊天页面地址
            for i in range(0, totalNumber, +1):
                repo_material_cate_id = args["repo_material_cate_id"]
                Material = self.repo.GetMaterial(repo_material_cate_id, 0, 1)
                wait = 1  # 判断素材仓库里是否由素材
                while wait == 1:
                    try:
                        material = Material[0]['content']  # 取出验证消息的内容
                        wait = 0
                    except Exception:
                        d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到验证消息\"").communicate()
                        time.sleep(30)
                        time.sleep(5)

                numbers = list[i]
                print(numbers)
                time.sleep(1)

                d(description='清空号码', className='android.widget.Button').click()
                time.sleep(1)
                d(className='android.widget.EditText', index=1, clickable='false').click()  # 点击输入框
                time.sleep(1)
                if d(className='android.widget.EditText', index=1, clickable='false').exists:  # 看会不会弹出键盘
                    d(className='android.widget.EditText', index=1, clickable='false').set_text(numbers)
                else:
                    d.press.back()
                    d(className='android.widget.EditText', index=1, clickable='false').set_text(numbers)
                d(className='android.widget.Button', index=3, description='开始聊天').click()
                time.sleep(2)
                if d(className='android.widget.Button', index=3, description='开始聊天').exists:  # 没有该ＱＱ的情况
                    continue
                time.sleep(1)
                d(resourceId='com.tencent.tim:id/input', className='android.widget.EditText').click()
                print(material)
                z.input(material)
                d(text='发送', resourceId='com.tencent.tim:id/fun_btn').click()
                d.server.adb.cmd("shell","am start -n com.android.chrome/com.google.android.apps.chrome.Main").communicate()  # 拉起来






        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMBrowserSendText

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_number_cate_id":"49","repo_material_cate_id":"33","totalNumber":"5","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, z,args)
