# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class TIMAddressCollectData:

    def __init__(self):
        self.repo = Repo()

    def scrollCell(self, d, args):
        while d(text='正在发送请求', className='android.widget.TextView').exists:
            time.sleep(2)

        info = d(index=0, className='android.widget.AbsListView').info
        bHeight = info["visibleBounds"]["bottom"] - info["visibleBounds"]["top"]
        bWidth = info["visibleBounds"]["right"] - info["visibleBounds"]["left"]
        # info = d(index=0, className='android.widget.AbsListView').child(index=2,className='android.widget.LinearLayout').info
        # lHeight = info["visibleBounds"]["bottom"] - info["visibleBounds"]["top"]
        count = d(index=0, className='android.widget.AbsListView').info['childCount']
        numberArr = []
        judge = True

        while judge==True:
            if judge == False:
                break
            for i in range(0, count):

                obj = d(index=0, className='android.widget.AbsListView').child(index=i,className='android.widget.LinearLayout')
                if obj.exists:
                    obj = obj.info["contentDescription"]
                    if obj in numberArr:
                        ok='ok'
                    else:
                        if obj.isdigit():
                            numberArr.append(obj)

                    if count == i + 1:
                        d.swipe(bWidth / 2, bHeight, bWidth / 2, 0)
                        nstr = d(index=0, className='android.widget.AbsListView').child(index=i,className='android.widget.LinearLayout').info["contentDescription"]
                        if nstr == numberArr[-1]:
                            judge = 'False'
                            break

                else:
                    if i==0:
                        continue
                    else:
                        judge = 'False'
                        break

        numberCateId = args["repo_numberCateId_id"]

        if len(numberArr) != 0:
            for i in range(0, len(numberArr)):
                self.repo.uploadPhoneNumber(numberArr[i], numberCateId)

    def action(self, d, z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(3)

        d(description='快捷入口', className='android.widget.ImageView').click()
        d(text = '加好友', className = 'android.widget.TextView').click()
        d(text='添加手机联系人', className='android.widget.TextView').click()
        time.sleep(2)

        self.scrollCell(d, args)

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
    args = {"repo_numberCateId_id":"108","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)
    # for i in range(0,10):
    #     obj = d(index=0, className='android.widget.AbsListView').child(index=i,className='android.widget.LinearLayout').child(
    #                 index=1, className='android.widget.TextView').info['text']
    #     print obj
