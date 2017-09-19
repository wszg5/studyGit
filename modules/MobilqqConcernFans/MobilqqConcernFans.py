# coding:utf-8
from __future__ import division
from uiautomator import Device
from Repo import *
import  time
from zservice import ZDevice

class MobilqqConcernFans:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z,args):
        z.toast( "准备执行QQ关注我的粉丝" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ关注我的粉丝" )
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
        if objtemp.exists:
            z.sleep( 1 )
            z.heartbeat( )
            objtemp.click( )
            if objtemp.exists:
                z.sleep( 1 )
                z.heartbeat( )
                objtemp.click( )

        forwait = 0
        while True:
            if d( text='附近点赞升级啦' ).exists:
                d( text='知道了' ).click( )
                break
            else:
                z.sleep( 1 )
                if forwait == 4:
                    break
                else:
                    forwait = forwait + 1

        while not d( text='编辑交友资料' ).exists:
            time.sleep( 2 )
        if d(index=1,textContains="粉丝",className="android.widget.TextView").exists:
            z.sleep(1)
            z.heartbeat()
            d(index=1,textContains="粉丝",className="android.widget.TextView").click()
            z.sleep(8)
        k = (300 - 160)/888 * height
        x = 69/540 * width
        y1 = 228/888 * height
        swipt = (888 - 114)/888 * height
        i = 0
        num = 0
        count = int(args["count"])
        objinfo = d(index=4,className="android.widget.LinearLayout").child(index=0,className="android.widget.LinearLayout").child(index=0,className="android.widget.TextView")
        listInfo = []
        while True:
            d.click(x,y1+i*k)
            z.sleep(2)
            if not d(text="更多",resourceId="com.tencent.mobileqq:id/ivTitleBtnRightText").exists:
                z.toast("已无粉丝可关注,停止模块")
                return
            if objinfo.exists:
                text = objinfo.info["text"]
                if text not in listInfo:
                    listInfo.append( text )
            if d(text="关注",className="android.widget.Button").exists:
                z.heartbeat()
                d( text="关注", className="android.widget.Button" ).click()
                z.sleep(2)
                z.heartbeat()
                if d( text="关注", className="android.widget.Button" ).exists:
                    z.toast("操作频繁,无法关注了")
                    return
                z.sleep(1)
                z.heartbeat()
                num = num +1

            d(text="返回",resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").click()
            i = i +1
            if num == count:
                z.toast( "已关注设定的粉丝数量,停止模块" )
                return
            if i==5:
                z.sleep(1)
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                z.sleep(3)
                d.click( x, y1 + (i-1) * k )
                z.sleep(2)
                if objinfo.exists:
                    text = objinfo.info["text"]
                    if text  in listInfo:
                        z.toast("到底了,停止模块")
                        return
                    else:
                        i = 0
                        d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click( )

def getPluginClass():
    return MobilqqConcernFans

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49YSK00272")
    z = ZDevice("HT49YSK00272")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"count":"7","time_delay":"3"}    #cate_id是仓库号，length是数量

    # d.server.adb.cmd( "shell", "pm clear com.tencent.mobileqq" ).communicate( )
    # d.server.adb.cmd( "shell",
    #                   "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )

    o.action(d,z, args)
    # d.server.adb.cmd( "shell",
    #                   'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=wpa\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"' % 3580277168 )