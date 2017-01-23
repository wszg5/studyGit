# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WeiXinSetLabel:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()  # 将微信拉起来
        time.sleep(7)
        d(text='通讯录').click()
        if d(text='新的朋友').exists:
            print()
        else:
            d(text='通讯录').click()

        set1 = set()
        change = 0
        i = 1
        t = 1
        ending = 0     #用来判断是否到底
        EndIndex = int(args['EndIndex'])         #------------------
        while t < EndIndex + 1:

            time.sleep(1)
            obj = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=i).child(className='android.widget.LinearLayout').child(className='android.view.View')     #得到微信名
            if obj.exists:
                change = 1      #好友存在且未被添加的情况出现，change值改变
                obj1 = obj.info
                name = obj1['text']
                if name=='微信团队':
                    i = i+1
                    continue
                if name in set1:    #判断是否已经给该人发过消息
                    i = i+1
                    continue
                else:
                    set1.add(name)
                    print(name)
                obj.click()
                if d(text='标签').exists:
                    d(description='返回').click()
                    i = i + 1
                    t = t + 1
                    continue
                obj = d(className='android.widget.ImageView',index=1,resourceId='com.tencent.mm:id/abr')      #看性别是否有显示
                if obj.exists:
                    Gender = obj.info
                    Gender = Gender['contentDescription']
                    print(Gender)
                else:
                    Gender = '妖'
                if  d(textContains='备注和标签').exists:
                    d(textContains='备注和标签').click()
                else:
                    d(description='返回').click()    #点进去是自己的情况
                    i = i + 1
                    t = t + 1
                    continue
                d(textContains='添加标签').click()
                z.input(Gender)
                d(text='保存').click()
                d(text='完成').click()

                time.sleep(1)
                d(description='返回').click()
                i = i+1
                t = t+1
                continue

            else:
                if change==0:   #一次还没有点击到人
                    i = i+1
                    continue
                else:
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    time.sleep(3)

                    if ending == 1:     #结束条件
                        return
                    if d(textContains='位联系人').exists:
                        ending = 1

                    for g in range(0,12,+1):
                        time.sleep(0.5)
                        obj = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=g).child(className='android.widget.LinearLayout').child(className='android.view.View')  # 得到微信名
                        time.sleep(0.5)
                        obj = obj.info
                        Tname = obj['text']
                        if Tname==name:
                            break
                    i = g+1
                    continue



def getPluginClass():
    return WeiXinSetLabel

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()


    args = {'EndIndex':'100',"time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
