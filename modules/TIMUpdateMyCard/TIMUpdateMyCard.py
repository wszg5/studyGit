# coding:utf-8
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice


class TIMUpdateMyCard:
    def __init__(self):

        self.repo = Repo()

    def action(self, d, z, args):
        z.toast( "准备执行TIM修改我的名片模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM修改我的名片" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
        z.heartbeat( )

        if d( text='消息' ).exists:  # 到了通讯录这步后看号有没有被冻结
            z.toast( "卡槽TIM状态正常，继续执行" )
        else:
            z.toast( "卡槽TIM状态异常，跳过此模块" )
            return
        z.heartbeat( )
        while True:                          #由于网速慢或手机卡可能误点
            if d( index=1, className='android.widget.ImageView' ).exists:
                # d(index=0,className="android.widget.RelativeLayout").child( index=1,resourceId="com.tencent.tim:id/name", className='android.widget.ImageView' ).click()
                z.heartbeat( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,className="android.widget.RelativeLayout" ).click( )
                # d( index=2, className="android.widget.FrameLayout" ).child( index=0,className="android.widget.RelativeLayout" ).child( index=1, className='android.widget.ImageView' ).click()
            if d(text="加好友").exists:    #由于网速慢或手机卡可能误点
                d(text="加好友").click()
                d(text="返回",className="android.widget.TextView").click()
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,className="android.widget.RelativeLayout" ).click( )
            z.sleep( 3 )
            if d( text='我的名片夹', resourceId='com.tencent.tim:id/name', className="android.widget.TextView" ).exists:
                z.heartbeat( )
                d( text='我的名片夹', resourceId='com.tencent.tim:id/name' ).click( )
                break
        z.sleep(1)

        if d(text="设置我的名片").exists:
            z.heartbeat( )
            d( text="设置我的名片" ).click()
            z.sleep( 1 )
            d(text="添加我的名片").click()
            z.sleep(1)
        else:
            z.heartbeat( )
            d(text="我的名片").click()
            z.sleep( 1 )
            d(index=2,text="编辑").click()
            z.heartbeat( )
            z.sleep( 2 )
            d(descriptionContains="名片图片").click()
            z.sleep( 2 )
            d( descriptionContains="显示更多" ).click( )
            z.sleep(2)
            if d(descriptionContains="显示更多").exists:
                z.toast("暂时无法更换名片")
                return
        d( text='从相册选择', resourceId='com.tencent.tim:id/action_sheet_button' ).click( )
        z.sleep( 3 )
        obj = d( index=0, className="com.tencent.widget.GridView",
                 resourceId="com.tencent.tim:id/photo_list_gv" ).child( index=0,
                                                                        className="android.widget.RelativeLayout" )
        if obj.exists:
            obj.click( )
            z.sleep( 3 )
            d( text='确定', resourceId='com.tencent.tim:id/name' ).click( )
            while d( text='正在识别' ).exists:
                time.sleep( 2 )
            z.heartbeat( )
        if d( text="重选" ).exists:
            d( text="重选" ).click( )
            d( index=0, className="com.tencent.widget.GridView",
               resourceId="com.tencent.tim:id/photo_list_gv" ).child( index=0,
                                                                      className="android.widget.RelativeLayout" ).click( )
            d( text='确定', resourceId='com.tencent.tim:id/name' ).click( )
            while d( text='正在识别' ).exists:
                time.sleep( 2 )
        z.sleep(2)
        d(text="完成").click()

def getPluginClass():
    return TIMUpdateMyCard

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

