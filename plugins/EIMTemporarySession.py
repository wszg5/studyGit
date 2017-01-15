# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class EIMTemporarySession:
    def __init__(self):
        self.repo = Repo()




    def action(self, d,z, args):

        totalNumber = int(args['totalNumber'])  # 要给多少人发消息

        cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        wait = 1
        while wait == 1:
            numbers = self.repo.GetNumber(cate_id, 0, totalNumber)  # 取出totalNumber条两小时内没有用过的号码
            lenth = len(numbers)
            if "Error" in numbers:  # 没有取到号码的时候
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"QQ号码%s号仓库为空，等待中\""%cate_id).communicate()
                time.sleep(20)
                continue
            elif lenth == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"QQ号码%s号仓库为空，等待中\""%cate_id).communicate()
                time.sleep(20)
                continue
            wait = 0

        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)


        for i in range (0,totalNumber,+1):
            cate_id = args["repo_material_cate_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            wait = 1  # 判断素材仓库里是否由素材
            while wait == 1:
                try:
                    material = Material[0]['content']  # 取出验证消息的内容
                    wait = 0
                except Exception:
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"消息素材%s号仓库为空，没有取到消息\""%cate_id).communicate()
                    time.sleep(20)

            numbers = list[i]
            time.sleep(1)

            z.openQQChat(numbers)       #唤起浏览器临时会话
            time.sleep(1)

            if d(text='企业QQ', resourceId='android:id/text1').exists:
                d(text='企业QQ', resourceId='android:id/text1').click()
                if d(text='仅此一次',resourceId='android:id/button_once').exists:
                    d(text='仅此一次',resourceId='android:id/button_once').click()

            if d(resourceId='com.tencent.eim:id/input', className='android.widget.EditText').exists:
                d(resourceId='com.tencent.eim:id/input', className='android.widget.EditText').click()
                z.input(material)

            d(text='发送', resourceId='com.tencent.eim:id/fun_btn').click()


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return EIMTemporarySession

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT55TSK00815")
    z = ZDevice("HT55TSK00815")


    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_number_cate_id":"37","repo_material_cate_id":"34","totalNumber":"4","time_delay":"3"};    #cate_id是仓库号，length是数量
    # z.openQQChat(154343346)   QQTemporarySession

    o.action(d, z,args)

