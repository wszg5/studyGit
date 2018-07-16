# coding:utf-8
import random
import string
from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from Repo import *
from zservice import ZDevice


class YiXinSignInAndOpenBox:
    def __init__(self):
        self.repo = Repo()
        self.type = 'yixin'

    def action(self, d, z, args):

        z.toast("正在ping网络是否通畅")
        while True:
            ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast("开始执行：易信签到开宝箱")
                break
            z.sleep(2)

        if not d(text='易信').exists and not d(text='发现').exists and not d(text='好友').exists and not d(text='我').exists:
            d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate()  # 拉起易信
            z.sleep(10)
            z.heartbeat()

        z.sleep(5)
        if d(text='立即更新').exists and d(text='下次再说').exists:
            d(text='下次再说').click()

        if d(text='易信').exists and d(text='发现').exists and d(text='好友').exists and d(text='我').exists:

            if d(text='发现').exists:
                d(text='发现').click()
                z.sleep(5)

            if d(text='星币商城').exists:
                d(text='星币商城').click()
                z.sleep(8)

            z.heartbeat()
            if not d(text='星币商城',className='android.widget.TextView').exists:
                z.sleep(8)
                z.heartbeat()

            if d(description='签到赚星币').exists:
                d(description='签到赚星币').click()
                z.sleep(8)

            if not d(text='签到赚星币',className='android.widget.TextView').exists:
                z.sleep(6)
                z.heartbeat()

            if d(description='签到', index=2).exists:
                d(description='签到').click()
                z.sleep(2)

            z.heartbeat()
            obj1 = d(description='签到规则').info["bounds"]
            obj2 = d(className='android.view.View', index=15).info["bounds"]
            x = obj1["right"] - (obj1["right"] - obj1["left"]) / 2
            y = obj2["top"] - (obj2["top"] - obj1["bottom"]) / 3

            d.click(x, y)
            z.sleep(2)

            if d(description='打开宝箱 Link').exists:
                d(description='打开宝箱 Link').click()
                z.sleep(2)

            if d(description='知道了').exists:
                d(description='知道了').click()

        if (args['time_delay']):
            z.sleep(int(args['time_delay']))



def getPluginClass():
    return YiXinSignInAndOpenBox

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("25424f9")
    z = ZDevice("25424f9")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"time_delay": "3"}
    o.action(d, z, args)

    # 易信语音测试　1000　＝　18/17秒语音
    # obj = d(resourceId='im.yixin:id/audioMessageLayout').info["bounds"]
    # x = (obj["right"] - obj["left"]) / 2 + obj["left"]
    # y = (obj["bottom"] - obj["top"]) / 2 + obj["top"]
    # d.swipe(x, y, x+10, y+10, 5000)

    # 卡槽测试
    # slot = Slot(d.server.adb.device_serial(),'yixin')
    # slot.clear(1)
    # slot.clear(2)
    # d.server.adb.cmd("shell", "pm clear im.yixin").communicate()  # 清除缓存
    # slot.restore(1)
    # d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate()  # 拉起易信

