# coding:utf-8
from uiautomator import Device
from Repo import *
import  time
from zservice import ZDevice

class MobilqqConcernII:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z,args):
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(8)

        obj = d(className='android.widget.ImageView', resourceId='com.tencent.mobileqq:id/conversation_head')
        if obj.exists:
            obj.click()
        else:
            d.swipe(0, height / 2, width - 20, height / 2, 5)
        z.sleep(1.5)

        obj1 = d(className='android.widget.ImageView', resourceId='com.tencent.mobileqq:id/head')
        if obj1.exists:
            obj1.click()
        z.sleep(3)

        obj2 = d(descriptionContains='次赞，按钮')
        if obj2.exists:
            obj2.click()
        z.sleep(5)

        if d(text='我赞过谁').exists:
            d(text='我赞过谁').click()
        z.heartbeat()
        z.sleep(3)
        obj3 = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=1) \
            .child(className='android.widget.RelativeLayout', index=1).child(
            className='android.widget.LinearLayout')  # 用来点击的
        if not obj3.exists:
            z.toast("我没赞过好友") #我没赞过好友的情况
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
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

                if d(textContains='知道').exists:
                    d(textContains='知道').click()

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

                    d.press.back()
                    i = i+1
                    t = t+1
                else:
                    z.heartbeat()
                    if d(text='关注').exists:
                        z.toast('关注频繁，结束程序')
                        if (args["time_delay"]):
                            z.sleep( int( args["time_delay"] ) )
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
            z.sleep( int( args["time_delay"] ) )


def getPluginClass():
    return MobilqqConcernII

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A6SK01638")
    z = ZDevice("HT4A6SK01638")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"add_count":"1000","time_delay":"3"}    #cate_id是仓库号，length是数量

    o.action(d,z, args)




















