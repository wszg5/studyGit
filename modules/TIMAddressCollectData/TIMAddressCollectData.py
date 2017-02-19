# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class TIMAddressCollectData:

    def __init__(self):
        self.repo = Repo()

    def action(self, d, z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(3)

        d(description='快捷入口', className='android.widget.ImageView').click()
        d(text = '加好友', className = 'android.widget.TextView').click()
        d(text='添加手机联系人', className='android.widget.TextView').click()
        time.sleep(2)

        info = d(index = 0, className = 'android.widget.AbsListView').info
        bHeight = info["visibleBounds"]["bottom"]-info["visibleBounds"]["top"]
        bWidth = info["visibleBounds"]["right"]-info["visibleBounds"]["left"]
        info = d(index=0, className='android.widget.AbsListView').child(index=2, className='android.widget.LinearLayout').info
        lHeight = info["visibleBounds"]["bottom"]-info["visibleBounds"]["top"]

        numberArr = []
        judge = True
        count = d(index=0, className='android.widget.AbsListView').info['childCount']
        i=-1
        while judge==True:
            i=i+1
            if judge==False:
                break
            for j in range(0,count):
                if i==0&j+2<count:
                    obj = d(index=0, className='android.widget.AbsListView').child(index=j+2,className='android.widget.LinearLayout').child(index=1,className='android.widget.TextView')
                    if obj.exists:
                        obj = obj.info["text"]
                        if obj in numberArr:
                            if count==j+3:
                                d.swipe(bWidth / 2, bHeight, bWidth / 2, lHeight * 2)
                                time.sleep(2)
                                if d(index=0, className='android.widget.AbsListView').child(index=j+2,className='android.widget.LinearLayout').child(index=1,
                                    className='android.widget.TextView').info["text"] in numberArr:
                                    judge = 'False'
                                    break
                                else:
                                    break
                        else:
                            numberArr.append(obj)
                    else:
                        d.swipe(bWidth / 2, bHeight, bWidth / 2, lHeight * 2)
                        time.sleep(2)
                        if d(index=0, className='android.widget.AbsListView').child(index=j+2,className='android.widget.LinearLayout').child(index=1,className='android.widget.TextView').exists:
                            break
                        else:
                            judge = 'False'
                            break
                elif i==0&j+2==count:
                    continue
                else:
                    obj = d(index=0, className='android.widget.AbsListView').child(index=j,className='android.widget.LinearLayout').child(index=1, className='android.widget.TextView')
                    if obj.exists:
                        obj = obj.info["text"]
                        if obj in numberArr:
                            if count==j+1:
                                d.swipe(bWidth / 2, bHeight, bWidth / 2, lHeight * 2)
                                time.sleep(2)
                                if d(index=0, className='android.widget.AbsListView').child(index=j,className='android.widget.LinearLayout').child(index=1,
                                    className='android.widget.TextView').info["text"] in numberArr:
                                    judge = 'False'
                                    break
                                else:
                                    break

                        else:
                            numberArr.append(obj)
                    else:
                        if j==0:
                            continue
                        d.swipe(bWidth / 2, bHeight, bWidth / 2, lHeight * 2)
                        time.sleep(2)
                        if d(index=0, className='android.widget.AbsListView').child(index=j,
                            className='android.widget.LinearLayout').child(index=1, className='android.widget.TextView').exists:
                            break
                        else:
                            judge = 'False'
                            break


        print numberArr

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMAddressCollectData

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT52DSK00474")
    z = ZDevice("HT52DSK00474")
    # print(d.dump(compressed=False))
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_collectData_id":"33","time_delay":"3","EndIndex":"8"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)