# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class MobilqqPraiseII:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z,args):

        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(8)
        d(description='快捷入口').click()
        d(textContains='加好友').click()
        d(textContains='附近的人').click()
        while not d(textContains='等级').exists:
            time.sleep(2)
        count = int(args['add_count'])
        getGender = args['gender']
        if getGender !='不限':
            d(resourceId='com.tencent.mobileqq:id/ivTitleBtnRightImage').click()
            d(text='筛选附近的人').click()
            d(text=getGender).click()
            d(text='完成').click()
            while not d(textContains='等级').exists:
                time.sleep(2)
        t = 0
        i = 3
        while t<count:
            forClick = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i).child(className='android.widget.RelativeLayout')
            if forClick.exists:
                if forClick.child(text='直播中').exists:
                    i = i+1
                    continue

                forClick.click()
                while not d(text='关注').exists:
                    time.sleep(2)
                praise = 0
                while praise<10:
                    if d(descriptionContains='赞').exists:
                        d(descriptionContains='赞').click()
                        if d(text='取消').exists:      #当点赞够次超数的时候
                            d(text='取消').click()
                            praise = 10       #表明点赞已够次数，将点赞结束掉
                        praise = praise+1
                    else:
                        praise = 10  # 无法赞的情况
                        continue
                d(text='返回').click()
                i = i+1
                t = t+1
            elif d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i).child(text='广告').exists:
                i =i+1
                continue
            else:
                str = d.info  # 获取屏幕大小等信息
                width = str["displayWidth"]
                clickCondition = d(className='android.widget.AbsListView')
                obj = clickCondition.info
                obj = obj['visibleBounds']
                top = int(obj['top'])
                bottom = int(obj['bottom'])
                y = bottom - top
                d.swipe(width / 2, y, width / 2, 0)
                time.sleep(3)
                i = 1


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqPraiseII

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"add_count":"30",'gender':"女","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
