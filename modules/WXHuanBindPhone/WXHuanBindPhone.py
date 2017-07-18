# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXHuanBindPhone:

    def __init__(self):
        self.repo = Repo()

    def action(self, d, z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(15)
        if d(text='我').exists:
           for i in range(1,3):
               d(text='我').click()
        z.sleep(3)
        d(text='设置').click()
        z.sleep(3)
        d(textContains='帐号与安全').click()
        z.sleep(3)
        d(text='手机号').click()
        z.sleep(3)
        if d(text='绑定手机号').exists:
            z.heartbeat()

            d(text='更换手机号').click()
            cate_id = args["repo_cate_id"]
            time_limit = args['time_limit']
            numbers = self.repo.GetAccount(cate_id, time_limit, 1)
            if len(numbers) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码%s号仓库为空，等待中\"" % cate_id).communicate()
                z.sleep(10)
                return

            if (args["time_delay"]):
                z.sleep(int(args["time_delay"]))



def getPluginClass():
    return WXHuanBindPhone

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("9ef40375")
    z = ZDevice("9ef40375")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_cate_id": "132", "repo_bindQQ_id": "189", "time_limit": "0", "time_delay": "3"}   #cate_id是仓库号，length是数量
    o.action(d, z, args)