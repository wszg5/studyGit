# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class NewMobilqqPraiseII:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z,args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(8)
        z.heartbeat()
        d(description='快捷入口').click()
        d(textContains='加好友').click()
        d(textContains='附近的人').click()
        while not d(textContains='等级').exists:
            z.sleep(2)
        getGender = args['gender']
        if getGender !='不限':
            d(resourceId='com.tencent.mobileqq:id/ivTitleBtnRightImage').click()
            d(text='筛选附近的人').click()
            d(text=getGender).click()
            d(text='完成').click()
            while not d(textContains='等级').exists:
                z.sleep(2)
        z.heartbeat()

        count = int(args['concernnum'])
        t = 0
        i = 3
        while t<count:
            forClick = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i).child(className='android.widget.RelativeLayout')
            if forClick.child(className='android.widget.LinearLayout',index=2).exists:
                z.heartbeat()
                if forClick.child(text='直播中').exists:
                    i = i+1
                    continue

                forClick.click()

                while not d(textContains='关注').exists:
                    z.sleep(2)
                    if d(text='知道了').exists:
                        d(text='知道了').click()

                for j in range( 0, 10 ):
                    if d( descriptionContains='赞' ).exists:
                        d( descriptionContains='赞' ).click()
                        if d(textContains='今日免费赞数已达').exists:
                            d(text='取消').click()
                            break
                z.sleep(2)

                if d(text='关注').exists:
                    d(text='关注').click()

                d(text='返回').click()
                i = i+1
                t = t+1
                continue

            elif d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i).child(text='广告').exists:  #被点击条件不存在的情况
                z.heartbeat()
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
                z.sleep(3)
                i = 1


        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return NewMobilqqPraiseII

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49RSK01046")
    z = ZDevice("HT49RSK01046")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"concernnum":"20",'gender':"男","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
