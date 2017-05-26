# coding:utf-8
from uiautomator import Device
from Repo import *
import  time
from zservice import ZDevice

class MobilqqConcern:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z,args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(8)
        d(className='android.widget.TabWidget', index=2).child(className='android.widget.FrameLayout', index=2).child(
            className='android.widget.RelativeLayout', index=0).click()
        d(text='附近').click()
        z.heartbeat()
        while True:
            if d(text='新鲜事').exists:
                break
            else:
                z.sleep(2)
        d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout', index=2).child(
            className='android.widget.LinearLayout', index=0).click()  # 点击进入自己的主页

        forwait = 0
        while True:
            if d( text='知道了' ).exists:
                d( text='知道了' ).click( )
                break
            else:
                z.sleep( 2 )
                if forwait == 5:
                    break
                else:
                    forwait = forwait + 1
            z.sleep(1)
        d(descriptionContains='赞').child(className='android.view.View').click()
        # d(descriptionContains='帐户及设置').click()
        # d(descriptionContains='等级').click()
        # d(descriptionContains='赞').click()
        z.sleep(3)
        d(text='我赞过谁').click()
        z.heartbeat()
        z.sleep(3)
        obj3 = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=1) \
            .child(className='android.widget.RelativeLayout', index=1).child(
            className='android.widget.LinearLayout')  # 用来点击的
        if not obj3.exists:
            #我没赞过好友的情况
            return
        z.heartbeat()
        set1 = set()
        i = 1
        t = 1
        mmm = 0
        add_count = int(args['add_count'])  # 要添加多少人
        while t < add_count + 1:
            obj = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i)\
                .child(className='android.widget.RelativeLayout',index=1).child(className='android.widget.LinearLayout')      #用来点击的
            obj1 = obj.child(className='android.widget.TextView')
            if obj1.exists:
                z.heartbeat()
                obj1 = obj1.info
                name = obj1['text']
                if name in set1:  # 判断是否已经关注过该联系人
                    i = i + 1
                    continue
                else:
                    time.sleep(0.5)
                    set1.add(name)
                    print(name)
                obj.click()
                while d(textContains='正在加载').exists:
                    z.sleep(2)
                z.heartbeat()

                if d(text='关注').exists:
                    d(text='关注').click()
                    z.sleep(3)
                if d(textContains='取消').exists:
                    d(text='取消').click()
                if mmm==0:
                    if d(text='关注').exists:     #因为第一次会有个提醒页面，需要再点一次才能关注成功
                        d(text='关注').click()
                        z.sleep(1)
                        mmm = 1
                    # if d(text='关注').exists:
                    #     return

                    d.press.back()
                    i = i+1
                    t = t+1
                else:
                    z.heartbeat()
                    if d(text='关注').exists:
                        z.toast('关注频繁，结束程序')
                        return
                    d.press.back()
                    i = i+1
                    continue
            else:
                if d(textContains='暂无更多').exists:
                    break
                if d(textContains='显示更多').exists:
                    d(textContains='显示更多').click()
                d.swipe(width / 2, height * 4 / 5, width / 2, height / 5)
                z.sleep(2)
                i = 1
                continue
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqConcern

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4BLSK00255")
    z = ZDevice("HT4BLSK00255")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"add_count":"1000","time_delay":"3"}    #cate_id是仓库号，length是数量

    o.action(d,z, args)



















