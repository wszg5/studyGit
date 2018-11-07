# coding=utf-8
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *


class TIMUpdateAddStyle:
    def __init__(self):
        self.repo = Repo( )

    def action(self, d, z, args):
        z.toast( "准备执行TIM修改头像模块" )
        z.sleep( 1 )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
        z.heartbeat( )

        if d( text="消息", resourceId="com.tencent.tim:id/ivTitleName" ).exists and not d( text="马上绑定",
                                                                                         className="android.widget.Button" ).exists:
            z.toast( "登录状态正常，继续执行" )
        else:
            if d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).exists:
                d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).click( )
                z.sleep( 1 )
            elif d( text="消息", className="android.widget.TextView" ).exists and d( text="马上绑定",
                                                                                   className="android.widget.Button" ).exists:
                d( text="消息", className="android.widget.TextView" ).click( )
                z.sleep( 1 )
            elif d( text="返回" ).exists:
                d( text="返回" ).click( )
                z.sleep( 1 )

            else:
                z.toast( "登录状态异常，跳过此模块" )
                return
        z.heartbeat( )

        while True:   # 防止存在误点
            if d( index=1, className='android.widget.ImageView' ).exists:
                z.heartbeat( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,
                                                                            className="android.widget.RelativeLayout" ).click( )

            if d( text="加好友" ).exists:  # 由于网速慢或手机卡可能误点
                d( text="加好友" ).click( )
                z.heartbeat( )
                d( text="返回", className="android.widget.TextView" ).click( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,
                                                                            className="android.widget.RelativeLayout" ).click( )
            z.sleep( 3 )
            if d( index=1, resourceId="com.tencent.tim:id/name", className="android.widget.ImageView" ).exists:
                z.heartbeat( )
                break
        d( index=1, resourceId="com.tencent.tim:id/name", className="android.widget.ImageView" ).click( )
        d( text="帐号管理" ).click( )
        time.sleep( 2 )
        obj = d( resourceId="com.tencent.tim:id/account" )
        account = obj.info["text"]
        d.press.back()
        time.sleep(1)
        d(text="联系人、隐私").click()
        time.sleep(1)
        z.heartbeat()
        d(text="加好友设置").click()
        time.sleep(10)
        while not d(description="允许任何人").exists:
            time.sleep(2)
        d(description="允许任何人").click()
        time.sleep(0.5)
        d.press.back()
        repo_account_id = args["repo_account_id"]
        self.repo.BackupInfo( repo_account_id, 'using', account, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber

def getPluginClass():
    return TIMUpdateAddStyle


if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "HT4BFSK02078" )
    z = ZDevice( "HT4BFSK02078" )
    z.server.install( )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).wait( )
    args = {"repo_account_id": "374"}
    o.action( d, z, args )
    # d(description="允许任何人").click()
    # time.sleep(0.5)
    # d.press.back()