# coding:utf-8
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice


class TIMSendMail19:
    def __init__(self):

        self.repo = Repo()


    def action(self, d, z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").communicate()  # 强制停止
        d.server.adb.cmd("shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(3)

        d(index=2, className='android.widget.FrameLayout').click()
        d(text='邮件', className='android.widget.TextView').click()
        time.sleep(1)
        if d(text='开通QQ邮箱', className='android.widget.Button').exists:
            d(text='开通QQ邮箱', className='android.widget.Button').click()

        while 1:
            if d(text='写邮件', className='android.widget.TextView').exists:
                d(text='写邮件', className='android.widget.TextView').click()
                break
            else:
                time.sleep(1)

        # while 1:
        #     if d(text='发送', className='android.widget.Button').exists:


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMSendMail19

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT52DSK00474")
    z = ZDevice("HT52DSK00474")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_mail_cateId": "121", "repo_material_cateId": "39", "time_delay": "3"};

    o.action(d, z, args)