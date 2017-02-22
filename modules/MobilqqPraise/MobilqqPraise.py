# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MobilqqPraise:
    def __init__(self):
        self.repo = Repo()




    def action(self, d,z,args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(8)

        add_count = int(args['add_count'])  # 要添加多少人
        repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号

        t = 0
        while True:            #总人数
            if t<add_count:
                numbers = self.repo.GetNumber(repo_number_cate_id, 120,1)  # 取出add_count条两小时内没有用过的号码
                if "Error" in numbers:  # 没有取到号码的时候
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到号码\"")
                    time.sleep(5)
                numbers = numbers[0]['number']
                time.sleep(0.5)
                d.server.adb.cmd("shell", 'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"'%numbers)  # qq名片页面
                time.sleep(2)
                if d(text='QQ').exists:
                    d(text='QQ').click()
                    time.sleep(0.5)
                    if d(text='仅此一次').exists:
                        d(text='仅此一次').click()

                while True:
                    if d(descriptionContains='赞').exists:
                        for z in range(0,10,+1):
                            d(descriptionContains='赞').click()
                        t = t+1
                        break
                    else:
                        time.sleep(3)
                        continue


            else:
                break


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqPraise

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_number_cate_id":"38","add_count":"3","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
