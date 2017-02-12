# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class WXBindQQ:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(4)
        d(text='我').click()
        d(text='设置').click()
        d(textContains='帐号与安全').click()
        d(text='QQ号').click()
        if d(text='QQ号').exists:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"该微信已绑定QQ号\"" ).communicate()
            return
        cate_id = args["repo_cate_id"]
        time_limit = args['time_limit']
        numbers = self.repo.GetAccount(cate_id, time_limit, 1)
        wait = 1
        while wait == 1:  # 判断仓库是否有东西
            try:
                QQNumber = numbers[0]['number']  # 即将登陆的QQ号
                wait = 0
            except Exception:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"QQ帐号库%s号仓库为空，等待中\"" % cate_id).communicate()
                time.sleep(30)
        QQPassword = numbers[0]['password']
        time.sleep(1)
        d(text='开始绑定').click()
        d(text='QQ号').set_text(QQNumber)
        d(className='android.widget.EditText', index=2).set_text(QQPassword)
        d(text='完成').click()
        time.sleep(3)
        if d(text='提示').exists:
            d(text='确定').click()
        if d(textContains='过于频繁').exists:
            return

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return WXBindQQ

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_cate_id": "59", "time_limit": "120", "time_delay": "3"};   #cate_id是仓库号，length是数量
    o.action(d,z, args)
