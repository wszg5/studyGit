# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class MobilqqPraise:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z,args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(8)

        add_count = int(args['add_count'])  # 要添加多少人
        repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号

        z.heartbeat()
        t = 0
        while True:            #总人数
            if t<add_count:
                numbers = self.repo.GetNumber(repo_number_cate_id, 120,1)  # 取出add_count条两小时内没有用过的号码
                if len(numbers) == 0:
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % repo_number_cate_id).communicate()
                    z.sleep(10)
                    return
                z.heartbeat()
                QQnumber = numbers[0]['number']
                time.sleep(0.5)
                d.server.adb.cmd("shell", 'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"'%QQnumber)  # qq名片页面
                z.sleep(2)
                if d(text='QQ').exists:
                    d(text='QQ').click()
                    time.sleep(0.5)
                    if d(text='仅此一次').exists:
                        d(text='仅此一次').click()
                z.heartbeat()
                while True:
                    if d(descriptionContains='赞').exists:
                        z.heartbeat()
                        for k in range(0,10,+1):
                            d(descriptionContains='赞').click()
                        t = t+1
                        break
                    else:
                        z.sleep(3)
                        continue
            else:
                break
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    return MobilqqPraise

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("9ddbd665")
    z = ZDevice("9ddbd665")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_cate_id":"119","add_count":"16","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
