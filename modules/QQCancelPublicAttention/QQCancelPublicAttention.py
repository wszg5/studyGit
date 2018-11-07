#coding=utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *

class QQCancelPublicAttention:
    def __init__(self):
        self.repo = Repo()

    def action(self,d,z,args):
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.mobileqq" ).wait( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).wait( )  # 将qq拉起来
        time.sleep(8)
        if d(text="消息",resourceId="com.tencent.mobileqq:id/ivTitleName",className="android.widget.TextView").exists:
            z.toast("登录状态正常")
        elif d( text='绑定手机号码' ).exists:
            while d( text='关闭' ).exists:
                d( text='关闭' ).click( )
                z.sleep(0.5)
            z.sleep( 1 )
        elif d( text='主题装扮' ).exists:
            while d( text='关闭' ).exists:
                d( text='关闭' ).click( )
                z.sleep(0.5)
        elif d( text='马上绑定' ).exists:
            while d( text='关闭' ).exists:
                d( text='关闭' ).click( )
                z.sleep(0.5)
        else:
            z.toast("登录状态异常,停止模块")
            return
        z.heartbeat( )
        d(index=2,text="联系人").click()

        Str = d.info  # 获取屏幕大小等信息
        height = Str["displayHeight"]
        width = Str["displayWidth"]
        z.sleep(1)
        if d(text="公众号").exists:
            z.heartbeat( )
            d(text="公众号" ).click()
            z.sleep(2)
        else:
            z.heartbeat( )
            d( text="通讯录" ).click( )
            z.heartbeat( )
            d.swipe( width/2+80, height / 2, 0, height / 2, 5 )
            z.sleep(2)
        i=0
        while i <5:
            obj = d(index=0,resourceId="com.tencent.mobileqq:id/name",className="android.widget.RelativeLayout").child(
                index=0,resourceId="com.tencent.mobileqq:id/name",className="android.widget.AbsListView").child(
                index=i,className="android.widget.FrameLayout").child(
                index=0,resourceId="com.tencent.mobileqq:id/name",className="android.widget.RelativeLayout")
            if obj.exists:
                z.heartbeat( )
                obj.click()
                time.sleep(3)
                z.heartbeat( )
                if d(descriptionContains="查看帐号资料",resourceId="com.tencent.mobileqq:id/ivTitleBtnRightImage").exists:
                    d( descriptionContains="查看帐号资料",
                       resourceId="com.tencent.mobileqq:id/ivTitleBtnRightImage" ).click( )
                    time.sleep(3)
                    if d( descriptionContains="查看帐号资料",
                          resourceId="com.tencent.mobileqq:id/ivTitleBtnRightImage" ).exists:
                        d( descriptionContains="查看帐号资料",
                           resourceId="com.tencent.mobileqq:id/ivTitleBtnRightImage" ).click( )
                        time.sleep( 3 )
                elif d(resourceId="com.tencent.mobileqq:id/ivTitleBtnRightImage", className="android.widget.ImageView").exists:
                    d( resourceId="com.tencent.mobileqq:id/ivTitleBtnRightImage", className="android.widget.ImageView" ).click()
                    time.sleep(4)

                z.heartbeat( )
                d( descriptionContains="更多操作", resourceId="com.tencent.mobileqq:id/ivTitleBtnRightImage" ).click( )
                z.sleep(2)
                if d(text="取消关注").exists:
                    z.heartbeat( )
                    d(text="取消关注").click()
                    d(text="不再关注").click()
                    z.sleep(3)
                    while d(text="正在取消关注…").exists:
                        time.sleep(2)
                    if d(text="联系人", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").exists:
                        d( text="联系人", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click()

                    i=i-1
                else:
                    z.heartbeat( )
                    d(text="取消").click()
                    d(text="返回").click()
                    z.sleep( 2 )
                    d(index= 0,resourceId="com.tencent.mobileqq:id/name",className="android.widget.ImageView").click()
            z.heartbeat( )
            i = i + 1
            time.sleep(2)

def getPluginClass():
    return QQCancelPublicAttention


if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "4c2bd3ad" )
    z = ZDevice( "4c2bd3ad" )
    z.server.install( )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).wait( )
    args = { }
    o.action( d, z, args )