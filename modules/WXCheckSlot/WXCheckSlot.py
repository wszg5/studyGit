# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXCheckSlot:

    def __init__(self):
        self.repo = Repo()

    def action(self,d,z,args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(7)
        d(text='我').click()
        d(text='设置').click()
        d(textContains='帐号与安全').click()
        d(text='邮件地址').click()
        z.heartbeat()
        if d(textContains='重新发送验证').exists:
            return
        if d(textContains='解绑').exists:
            return
        cate_id = int(args["repo_cate_id"])  # 得到取号码的仓库号

        Mail = self.repo.GetNumber(cate_id, 0, 1)  # 取出add_count条两小时内没有用过的号码
        if len(Mail) == 0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"第%s号号码仓库为空，等待中……\"" % cate_id).communicate()
            z.sleep(10)
            return
        BindMail = Mail[0]['number']
        d(className='android.widget.EditText').set_text(BindMail)
        d(text='确定').click()
        z.heartbeat()


        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXCheckSlot

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # d(className='android.widget.EditText').set_text('2375714387@qq.com')
    # d(textContains='搜索').set_text('')
    args = {"repo_cate_id": "121", "time_delay": "3"};   #cate_id是仓库号，length是数量
    o.action(d,z, args)
