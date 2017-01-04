# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class QQLiteBrowserSendText:
    def __init__(self):
        self.repo = Repo()




    def action(self, d,z, args):
        repo_material_cate_id = args["repo_material_cate_id"]
        Material = self.repo.GetMaterial(repo_material_cate_id, 0, 1)
        wait = 1  # 判断素材仓库里是否由素材
        while wait == 1:
            try:
                material = Material[0]['content']  # 取出验证消息的内容
                wait = 0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到验证消息\"")

        totalNumber = int(args['totalNumber'])  # 要给多少人发消息

        repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        wait = 1
        while wait == 1:
            numbers = self.repo.GetNumber(repo_number_cate_id, 120, totalNumber)  # 取出totalNumber条两小时内没有用过的号码
            lenth = len(numbers)
            if "Error" in numbers:  # 如果没有拿到号码的情况
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到号码\"")
                continue
            elif lenth==0:
                continue
            wait = 0

        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)

        d.server.adb.cmd("shell", "am force-stop com.android.chrome").wait()  # 强制停止
        for i in range(0, totalNumber, +1):
            numbers = list[i]
            time.sleep(1)
            # numbers = 1633232366+i      #测试用
            d.server.adb.cmd("shell",
                             "am start -a android.intent.action.VIEW -d http://www.jianli58.com/qq.html").wait()  # 拉起来
            time.sleep(1)
            d(className='android.widget.Button', index=2, description='清空号码').click()
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
            if d(className='android.widget.Button', index=3, description='开始聊天').exists:
                continue
            d(resourceId='com.tencent.qqlite:id/input', className='android.widget.EditText').click()
            z.input(material)
            d(text='发送', resourceId='com.tencent.qqlite:id/fun_btn').click()





def getPluginClass():
    return QQLiteBrowserSendText

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A3SK00853")
    z = ZDevice("HT4AVSK01106")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_number_cate_id":"49","repo_material_cate_id":"33","totalNumber":"9","time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
