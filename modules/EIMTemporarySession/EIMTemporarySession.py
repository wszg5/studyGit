# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class EIMTemporarySession:
    def __init__(self):
        self.repo = Repo()




    def action(self, d,z, args):

        totalNumber = int(args['totalNumber'])  # 要给多少人发消息

        cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        numbers = self.repo.GetNumber(cate_id, 0, totalNumber)  # 取出totalNumber条两小时内没有用过的号码
        if len(numbers)==0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\""%cate_id).communicate()
            time.sleep(10)
            return

        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)
        # d.server.adb.cmd("shell", "am force-stop com.tencent.eim").communicate()  # 强制停止   3001369923  Bn2kJq5l
        # d.server.adb.cmd("shell","am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(15)

        for i in range (0,totalNumber,+1):
            cate_id = args["repo_material_cate_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                time.sleep(10)
                return
            material = Material[0]['content']  # 取出验证消息的内容


            numbers = list[i]['number']
            time.sleep(1)

            d.server.adb.cmd("shell",
                             'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=crm\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"' % numbers)  # 临时会话
            time.sleep(2)

            if d(text='企业QQ').exists:
                d(text='企业QQ').click()
                time.sleep(0.5)
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()

            if d(textContains='沟通的权限').exists:
                d.server.adb.cmd("shell",
                                 'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=crm\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"' % numbers)  # 临时会话
                time.sleep(1)
                if d(text='企业QQ', resourceId='android:id/text1').exists:
                    d(text='企业QQ', resourceId='android:id/text1').click()
                    if d(text='仅此一次', resourceId='android:id/button_once').exists:
                        d(text='仅此一次', resourceId='android:id/button_once').click()

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
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")


    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_number_cate_id":"119","repo_material_cate_id":"39","totalNumber":"20","time_delay":"3"};    #cate_id是仓库号，length是数量
    # z.openQQChat(154343346)   QQTemporarySession

    o.action(d, z,args)

