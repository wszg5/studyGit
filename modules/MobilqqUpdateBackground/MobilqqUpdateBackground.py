# coding:utf-8
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice


class MobilqqUpdateBackground:
    def __init__(self):

        self.repo = Repo()

    def action(self, d, z, args):
        z.toast( "准备执行QQ修改资料(背景图片)模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ修改背景图片" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.mobileqq" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
        z.heartbeat( )

        if d( text='消息' ).exists:  # 到了通讯录这步后看号有没有被冻结
            z.toast( "卡槽QQ状态正常，继续执行" )
        else:
            z.toast( "卡槽QQ状态异常，跳过此模块" )
            return
        z.heartbeat( )
        while True:  # 由于网速慢或手机卡可能误点
            z.heartbeat( )
            if d( resourceId="com.tencent.mobileqq:id/conversation_head", index=0,className='android.widget.ImageView' ).exists:  # 点击ＱＱ头像.exists:
                # d(index=0,className="android.widget.RelativeLayout").child( index=1,resourceId="com.tencent.tim:id/name", className='android.widget.ImageView' ).click()
                z.heartbeat( )
                d( resourceId="com.tencent.mobileqq:id/conversation_head", index=0,
                   className='android.widget.ImageView' ).click( )  # 点击ＱＱ头像
                z.heartbeat( )
                d( index=1, resourceId='com.tencent.mobileqq:id/head', className='android.widget.ImageView' ).click( )
                break
            if d( text="加好友" ).exists:  # 由于网速慢或手机卡可能误点
                d( text="加好友" ).click( )
                d( text="返回", className="android.widget.TextView" ).click( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,
                                                                            className="android.widget.RelativeLayout" ).click( )
            z.sleep( 3 )
        d( className='android.widget.FrameLayout', resourceId='com.tencent.mobileqq:id/name',descriptionContains="点击更换背景" ).click( )
        z.heartbeat( )
        z.sleep(1)
        d(text="从手机相册选择").click()
        obj = d( index=0, className="com.tencent.widget.GridView",resourceId="com.tencent.mobileqq:id/photo_list_gv" ).child( index=0,className="android.widget.RelativeLayout" )
        if obj.exists:
            obj.click( )
            z.sleep( 3 )
            d( text='完成', resourceId='com.tencent.mobileqq:id/name' ).click( )
            while d( text='上传中' ).exists:
                time.sleep( 2 )
            z.heartbeat( )

def getPluginClass():
    return MobilqqUpdateBackground

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    # material=u'有空聊聊吗'
    z = ZDevice("HT54VSK01061")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {}
    o.action(d, z, args)

