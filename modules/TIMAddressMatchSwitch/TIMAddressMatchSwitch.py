# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class TIMAddressMatchSwitch:

    def __init__(self):
        self.repo = Repo()

    def action(self, d, z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(3)

        d(index=2, className='android.widget.FrameLayout').click()
        d(index=2, className='android.widget.ImageView').click()
        d(text='手机号码', className='android.widget.TextView').click()
        time.sleep(3)
        obj = d(index=3, className='android.widget.LinearLayout').child(index=0, className='android.widget.RelativeLayout').child(text='已启用', className='android.widget.TextView')
        if obj.exists:
            obj.click()
            d(index=2, className='android.widget.RelativeLayout').click()
            d(text='停用', className='android.widget.TextView').click()
            d(text='停用', className='android.widget.TextView').click()
            time.sleep(2)
            d(index=3, className='android.widget.LinearLayout').child(index=0,className='android.widget.RelativeLayout').child(
                text='启用', className='android.widget.Button').click()
            while 1:
                time.sleep(1)
                if d(index=3, className='android.widget.LinearLayout').child(index=0, className='android.widget.RelativeLayout').child(text='已启用', className='android.widget.TextView').exists:
                    break


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return TIMAddressMatchSwitch

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT52DSK00474")
    z = ZDevice("HT52DSK00474")
    # print(d.dump(compressed=False))
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_numberCateId_id": "108", "time_delay": "3"};  # cate_id是仓库号，length是数量
    o.action(d, z, args)