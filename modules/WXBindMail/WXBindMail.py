# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class WXBindMail:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(4)
        d(text='我').click()
        d(text='设置').click()
        d(textContains='帐号与安全').click()
        d(text='邮件地址').click()
        cate_id = int(args["repo_cate_id"])  # 得到取号码的仓库号
        wait = 1
        while wait == 1:
            Mail = self.repo.GetNumber(cate_id, 120, 1)  # 取出add_count条两小时内没有用过的号码
            if "Error" in Mail:  #
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"第%s号号码仓库为空，等待中……\"" % cate_id).communicate()
                time.sleep(20)
                continue
            wait = 0
        d(className='android.widget.EditText').set_text(Mail)
        d(text='确定').click()


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXBindMail

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    d(className='android.widget.EditText').set_text('2375714387@qq.com')
    args = {"repo_cate_id": "59", "time_delay": "3"};   #cate_id是仓库号，length是数量
    o.action(d,z, args)
