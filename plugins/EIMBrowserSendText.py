# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class EIMBrowserSendText:
    def __init__(self):
        self.repo = Repo()




    def action(self, d,z, args):

        totalNumber = int(args['totalNumber'])  # 要给多少人发消息

        cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        wait = 1
        while wait == 1:
            numbers = self.repo.GetNumber(cate_id, 120, totalNumber)  # 取出totalNumber条两小时内没有用过的号码
            if len(numbers)==0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"QQ%s号码库为空，等待中\""%cate_id).communicate()
                time.sleep(5)
                continue
            wait = 0

        list = numbers  # 将取出的号码保存到一个新的集合
        # d.server.adb.cmd("shell", "am force-stop com.android.chrome").communicate()  # 强制停止
        # d.server.adb.cmd("shell", "pm clear com.android.chrome").communicate()  # 清除缓存
        d.server.adb.cmd("shell", "am start -n com.android.chrome/com.google.android.apps.chrome.Main").communicate()  # 拉起来

        if d(description='清空号码',className='android.widget.Button').exists:

            for i in range (0,totalNumber,+1):
                cate_id = args["repo_material_cate_id"]
                Material = self.repo.GetMaterial(cate_id, 0, 1)
                wait = 1  # 判断素材仓库里是否由素材
                while wait == 1:
                    try:
                        material = Material[0]['content']  # 取出验证消息的内容
                        wait = 0
                    except Exception:
                        d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"%s号消息素材库为空，等待中\""%cate_id).communicate()
                        time.sleep(30)

                numbers = list[i]
                # d.server.adb.cmd("shell","am start -a android.intent.action.VIEW -d http://www.jianli58.com/qq.html").communicate()  # 拉起来
                d(description='清空号码', className='android.widget.Button').click()
                time.sleep(1)
                d(className='android.widget.EditText',index=1,clickable='false').click()

                if d(className='android.widget.EditText',index=1,clickable='false').exists:              #看会不会弹出键盘
                    d(className='android.widget.EditText',index=1,clickable='false').set_text(numbers)
                else:
                    d.press.back()
                    d(className='android.widget.EditText',index=1,clickable='false').set_text(numbers)
                d(className='android.widget.Button',index=3,description='开始聊天').click()
                time.sleep(1)
                if d(text='企业QQ',resourceId='android:id/text1').exists:
                    d(text='企业QQ', resourceId='android:id/text1').click()
                if d(text='仅此一次',resourceId='android:id/button_once').exists:
                    d(text='仅此一次', resourceId='android:id/button_once').click()

                if d(resourceId='com.tencent.eim:id/input', className='android.widget.EditText').exists:
                    d(resourceId='com.tencent.eim:id/input', className='android.widget.EditText').click()
                    z.input(material)
                else:
                    return 2
                d(text='发送',resourceId='com.tencent.eim:id/fun_btn').click()
                d.server.adb.cmd("shell","am start -n com.android.chrome/com.google.android.apps.chrome.Main").communicate()  # 拉起来


        else:
            d.server.adb.cmd("shell","am start -a android.intent.action.VIEW -d http://www.jianli58.com/qq.html").communicate()  # 不在聊了页面时输入聊天页面地址
            for i in range(0, totalNumber, +1):
                cate_id = args["repo_material_cate_id"]
                Material = self.repo.GetMaterial(cate_id, 0, 1)
                wait = 1  # 判断素材仓库里是否由素材
                while wait == 1:
                    try:
                        material = Material[0]['content']  # 取出验证消息的内容
                        wait = 0
                    except Exception:
                        d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"%s号消息素材库为空，等待中\""%cate_id).communicate()

                        time.sleep(5)

                numbers = list[i]
                # d.server.adb.cmd("shell","am start -a android.intent.action.VIEW -d http://www.jianli58.com/qq.html").communicate()  # 拉起来
                d(description='清空号码', className='android.widget.Button').click()
                time.sleep(1)
                d(className='android.widget.EditText', index=1, clickable='false').click()

                if d(className='android.widget.EditText', index=1, clickable='false').exists:  # 看会不会弹出键盘
                    d(className='android.widget.EditText', index=1, clickable='false').set_text(numbers)
                else:
                    d.press.back()
                    d(className='android.widget.EditText', index=1, clickable='false').set_text(numbers)
                d(className='android.widget.Button', index=3, description='开始聊天').click()
                time.sleep(1)
                if d(text='企业QQ', resourceId='android:id/text1').exists:
                    d(text='企业QQ', resourceId='android:id/text1').click()
                if d(text='仅此一次', resourceId='android:id/button_once').exists:
                    d(text='仅此一次', resourceId='android:id/button_once').click()
                if d(resourceId='com.tencent.eim:id/input', className='android.widget.EditText').exists:
                    d(resourceId='com.tencent.eim:id/input', className='android.widget.EditText').click()
                    z.input(material)
                else:
                    return 2
                d(text='发送', resourceId='com.tencent.eim:id/fun_btn').click()
                d.server.adb.cmd("shell",
                                     "am start -n com.android.chrome/com.google.android.apps.chrome.Main").communicate()  # 拉起来



        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return EIMBrowserSendText

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT58DSK00066")
    z = ZDevice("HT58DSK00066")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_cate_id":"49","repo_material_cate_id":"33","totalNumber":"4","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, z,args)
