# coding:utf-8
from __future__ import division
from uiautomator import Device
from Repo import *
import  time
from zservice import ZDevice

class MobilqqFaceMatching:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z,args):
        z.toast( "准备执行QQ颜值匹配" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ颜值匹配" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.mobileqq" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        z.heartbeat( )
        if d( text="消息" ).exists:
            z.toast( "卡槽状态正常，继续执行" )
        else:
            z.toast( "卡槽状态异常，跳过此模块" )
            return

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        z.heartbeat( )
        if d( text='绑定手机号码' ).exists:
            d( text='关闭' ).click( )
        if d( textContains='匹配' ).exists:
            d.press.back( )
        z.heartbeat( )
        while not d( text='附近的人', className="android.widget.TextView" ).exists:
            if d( index=2, text="动态", className="android.widget.TextView" ).exists:
                d( index=2, text="动态", className="android.widget.TextView" ).click( )
            z.sleep( 1 )
            z.heartbeat( )
            if d( index=1, text="附近", className="android.widget.TextView" ).exists:
                z.sleep( 1 )
                z.heartbeat( )
                d( index=1, text="附近", className="android.widget.TextView" ).click( )
        # d(text='附近的人',className="android.widget.TextView").click()
        tempnum = 0
        objtemp = d( index=2, className="android.widget.LinearLayout" ).child( index=0,
                                                                               className="android.widget.LinearLayout",
                                                                               resourceId="com.tencent.mobileqq:id/name" ).child(
            index="0", className="android.widget.RelativeLayout" ).child( index=0, className="android.widget.ImageView",
                                                                          resourceId="com.tencent.mobileqq:id/icon" )
        while True:
            if objtemp.exists:
                z.sleep( 1 )
                break
            else:
                z.sleep( 2 )
                if tempnum == 4:
                    break
                else:
                    tempnum = tempnum + 1
        # d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=2).click()
        # z.sleep(5)
        if not d(text="颜值匹配").exists:
            z.toast("没有颜值匹配")
            return
        while d(text="颜值配对").exists:
            z.sleep( 1 )
            z.heartbeat( )
            d( text="颜值配对" ).click()
        forwait = 0
        while True:
            if d( text='我的' ).exists:
                # d( text='知道了' ).click( )
                break
            else:
                z.sleep( 1 )
                if forwait == 4:
                    break
                else:
                    forwait = forwait + 1
        z.sleep(8)
        if d(description="点这里立即聊天，回复率翻倍").exists:
            d( description="点这里立即聊天，回复率翻倍" ).click()
            z.sleep(2)
        if d(description="").exists:
            z.toast()











        # while not d( text='编辑交友资料' ).exists:
        #     time.sleep( 2 )
        # if d(index=1,textContains="粉丝",className="android.widget.TextView").exists:
        #     z.sleep(1)
        #     z.heartbeat()
        #     d(index=1,textContains="粉丝",className="android.widget.TextView").click()
        #
        #
        # d(descriptionContains='赞').child(className='android.view.View').click()
        # z.sleep(3)
        # d(text='我赞过谁').click()
        # z.heartbeat()
        # z.sleep(3)
        # obj3 = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=1) \
        #     .child(className='android.widget.RelativeLayout', index=1).child(
        #     className='android.widget.LinearLayout')  # 用来点击的
        # if not obj3.exists:
        #     #我没赞过好友的情况
        #     return
        # z.heartbeat()
        # set1 = set()
        # i = 1
        # t = 1
        # mmm = 0
        # add_count = int(args['add_count'])  # 要添加多少人
        # while t < add_count + 1:
        #     obj = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i)\
        #         .child(className='android.widget.RelativeLayout',index=1).child(className='android.widget.LinearLayout')      #用来点击的
        #     obj1 = obj.child(className='android.widget.TextView')
        #     if obj1.exists:
        #         z.heartbeat()
        #         obj1 = obj1.info
        #         name = obj1['text']
        #         if name in set1:  # 判断是否已经关注过该联系人
        #             i = i + 1
        #             continue
        #         else:
        #             time.sleep(0.5)
        #             set1.add(name)
        #             print(name)
        #         z.sleep(1)
        #         z.heartbeat()
        #         obj.click()
        #         while d(textContains='正在加载').exists:
        #             z.sleep(2)
        #         z.heartbeat()
        #
        #         if d(text='关注').exists:
        #             d(text='关注').click()
        #             z.sleep(3)
        #         if d(textContains='取消').exists:
        #             d(text='取消').click()
        #         if mmm==0:
        #             if d(text='关注').exists:     #因为第一次会有个提醒页面，需要再点一次才能关注成功
        #                 d(text='关注').click()
        #                 z.sleep(1)
        #                 z.heartbeat()
        #                 if d( text='关注' ).exists:  # 因为第一次会有个提醒页面，需要再点一次才能关注成功
        #                     z.toast( '关注频繁，结束程序' )
        #                     return
        #                 # mmm = 1
        #             # if d(text='关注').exists:
        #             #     return
        #
        #             d.press.back()
        #             i = i+1
        #             t = t+1
        #         else:
        #             z.heartbeat()
        #             if d(text='关注').exists:
        #                 z.toast('关注频繁，结束程序')
        #                 return
        #             d.press.back()
        #             i = i+1
        #             continue
        #     else:
        #         if d(textContains='暂无更多').exists:
        #             break
        #         if d(textContains='显示更多').exists:
        #             d(textContains='显示更多').click()
        #         d.swipe(width / 2, height * 4 / 5, width / 2, height / 5)
        #         z.sleep(2)
        #         i = 1
        #         continue
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqFaceMatching

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49YSK00272")
    z = ZDevice("HT49YSK00272")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"add_count":"5","time_delay":"3"}    #cate_id是仓库号，length是数量

    # d.server.adb.cmd( "shell", "pm clear com.tencent.mobileqq" ).communicate( )
    # d.server.adb.cmd( "shell",
    #                   "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )

    o.action(d,z, args)
    # d.server.adb.cmd( "shell",
    #                   'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=wpa\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"' % 3580277168 )