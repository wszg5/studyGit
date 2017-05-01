# coding:utf-8
import threading
import time
from PIL import Image
from uiautomator import Device
import re,subprocess
from Repo import *
from zservice import ZDevice
import time, datetime, random

class EIMAddGroupII:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.eim").communicate()  # 强制停止   3001369923  Bn2kJq5l
        d.server.adb.cmd("shell", "am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(6)
        add_count = int(args['add_count'])  # 要添加多少人

        cate_id = int(args["repo_number_id"])  # 得到取号码的仓库号
        numbers = self.repo.GetNumber(cate_id, 120, add_count)  # 取出add_count条两小时内没有用过的号码
        if len(numbers) == 0:
            d.server.adb.cmd("shell",
                             "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % cate_id).communicate()
            z.sleep(10)
            return
        list = numbers  # 将取出的号码保存到一个新的集合
        z.heartbeat()
        if d(description='发起多人聊天等功能').exists:
            d(description='发起多人聊天等功能').click()
        else:
            return 2
        d(text='加好友').click()

        z.heartbeat()
        d(text='查找群').click()
        for i in range(0,add_count,+1):
            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                z.sleep(10)
                return
            message = Material[0]['content']
            QQnumber = list[i]['number']
            z.input(QQnumber)   #QQnumber
            d(text='查找').click()
            z.sleep(2)
            z.heartbeat()
            if d(text='查找').exists:            #该号码不存在的情况
                obj = d(className='android.widget.EditText').info                 #将文本框已有的东西删除重来
                obj = obj['text']
                lenth = len(obj)
                t = 0
                while t < lenth:
                    d.press.delete()
                    t = t + 1
                    continue
                continue
            obj = d(className='android.widget.RelativeLayout', index=5).child(className='android.widget.TextView',
                                                                              index=1).info
            member = obj['text']
            member = filter(lambda ch: ch in '0123456789', member)
            member = int(member)
            if member == 0:
                continue
            d(text='加入该群').click()
            z.sleep(2)
            z.heartbeat()
            if d(text='加入该群').exists:  #不让加入的情况
                d(text='返回').click()
                obj = d(className='android.widget.EditText').info  # 将文本框已有的东西删除重来
                obj = obj['text']
                lenth = len(obj)
                t = 0
                while t < lenth:
                    d.press.delete()
                    t = t + 1
                    continue
                continue

            obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
            obj = obj['text']
            lenth = len(obj)
            m = 0
            while m < lenth:
                d.press.delete()
                m = m + 1
            z.input(message)
            d(text='发送').click()
            d(text='查找群').click()

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))
def getPluginClass():
    return EIMAddGroupII

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()

    d = Device("8HVSMZKBEQFIBQUW")
    z = ZDevice("8HVSMZKBEQFIBQUW")
    d.server.adb.cmd("shell","ime set com.zunyun.qk/.ZImeService").communicate()

    # d.dump(compressed=False)
    args = {"repo_number_id":"119","repo_material_id":"39","add_count":"13","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)