# coding:utf-8
from RClient import *
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
from XunMa import *
import traceback
from PIL import Image
import colorsys
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MobilqqConcern:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z,args):
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(8)
        d(descriptionContains='帐户及设置').click()
        d(descriptionContains='等级').click()
        d(descriptionContains='赞').click()
        d(text='我赞过谁').click()
        set1 = set()
        i = 1
        t = 1
        add_count = int(args['add_count'])  # 要添加多少人
        while t < add_count + 1:
            obj = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i)\
                .child(className='android.widget.RelativeLayout',index=1).child(className='android.widget.LinearLayout')      #用来点击的
            obj1 = obj.child(className='android.widget.TextView')
            if obj1.exists:
                obj1 = obj1.info
                name = obj1['text']
                if name in set1:  # 判断是否已经关注过该联系人
                    i = i + 1
                    continue
                else:
                    set1.add(name)
                    print(name)
                obj.click()
                while d(textContains='正在加载').exists:
                    time.sleep(2)
                if d(text='关注').exists:
                    d(text='关注').click()
                    time.sleep(1)
                    if d(text='关注').exists:
                        return

                    d(text='返回').click()
                    i = i+1
                    t = t+1
                else:
                    d(text='返回').click()  #该好友已被关注的情况
                    i = i+1
                    continue
            else:
                if d(textContains='暂无更多').exists:
                    break
                if d(textContains='显示更多').exists:
                    d(textContains='显示更多').click()
                d.swipe(width / 2, height * 4 / 5, width / 2, height / 5)
                for g in range(0,12,+1):
                    obj2 = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=g) \
                        .child(className='android.widget.RelativeLayout', index=1).child(
                        className='android.widget.LinearLayout').child(className='android.widget.TextView')  # 用来点击的
                    if obj2.exists:
                        obj2 = obj2.info
                        Tname = obj2['text']
                        if Tname==name:
                            break
                i = g+1
                continue
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqConcern

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()

    args = {"add_count":"1000","time_delay":"3"}    #cate_id是仓库号，length是数量

    o.action(d,z, args)



















