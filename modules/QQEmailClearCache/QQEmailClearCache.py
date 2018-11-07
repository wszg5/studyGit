# coding:utf-8
from __future__ import division

import os
import random

from smsCode import smsCode
import string
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice


class QQEmailClearCache:
    def __init__(self):

        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )

    def action(self, d, z, args):
        time_delay = int( args["time_delay"] )
        run_time = float( time_delay )
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'锁定时间还差:%d分钟' % int( run_time - run_interval ) )
            z.sleep( 2 )
            return
        z.toast( "准备执行QQ邮箱清除缓存" )
        z.heartbeat( )
        # d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
        # d.server.adb.cmd( "shell","am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
        # z.sleep( int( args["time_delay"] ) )
        z.heartbeat()
        Str = d.info  # 获取屏幕大小等信息
        height = int( Str["displayHeight"] )
        width = int( Str["displayWidth"] )
        z.heartbeat( )
        flag1 = False
        flag2 = False
        for t in range(2):
            d.dump( compressed=False )
            if d( text="收件箱​",className="android.widget.TextView" ).exists:
                if d(textContains="密码错误，请重新输入").exists:
                    z.toast("密码错误，请重新输入")
                    return
                else:
                    z.toast( "状态正常，继续执行" )
                    break
            else:
                if d( text="温馨提示​", className="android.widget.TextView" ).exists:
                    d( text="确定", className="android.widget.Button" ).click( )
                    z.sleep( 1 )
                    break
                elif d(text="收件人：").exists and d(text="写邮件").exists:
                    flag1 = True
                    break
                elif d(text="取消​",resourceId='com.tencent.androidqqmail:id/a5',index=0).exists:
                    d( text="取消​", resourceId='com.tencent.androidqqmail:id/a5',index=0 ).click()
                    time.sleep(1)
                    if d(text="离开",className="android.widget.Button").exists:
                        d( text="离开", className="android.widget.Button" ).click()
                        time.sleep(1)
                    if d( text="收件箱​", className="android.widget.TextView" ).exists:
                        if d( textContains="密码错误，请重新输入" ).exists:
                            z.toast( "密码错误，请重新输入" )
                            return
                        else:
                            z.toast( "状态正常，继续执行" )
                            break

                elif d(index=1,text="写邮件​",className="android.widget.TextView").exists:
                    d.click(60/720 * width,198/1280 * height)
                    flag1 = True
                    break
                else:
                    if t>=1:
                        z.toast( "状态异常，跳过此模块" )
                        return
                    else:
                        d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
                        d.server.adb.cmd( "shell",
                                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                        time.sleep( 5 )
        if d( text="收件箱​", className="android.widget.TextView" ).exists:
            if d( textContains="密码错误，请重新输入" ).exists:
                z.toast( "密码错误，请重新输入" )
                return
            else:
                z.toast( "状态正常，继续执行" )
        else:
            z.toast("状态不正常")
            return
        if d( description="写邮件和设置等功能" ).exists:
            d( description="写邮件和设置等功能" ).click( )
            z.sleep( 0.5 )
            if d( text="设置", resourceId="com.tencent.androidqqmail:id/w1" ).exists:
                d( text="设置", resourceId="com.tencent.androidqqmail:id/w1" ).click( )
                z.sleep( 0.5 )
                d.swipe( width / 2, height * 4 / 5, width / 2, height / 5 )
                time.sleep( 2 )
                if d(text="清理缓存​", className="android.widget.TextView").exists:
                    d( text="清理缓存​", className="android.widget.TextView" ).click()
                    time.sleep(2)
                    d(text="清理​",className="android.widget.TextView").click()
                    time.sleep(3)
                    while True:
                        obj = d( index=3, className="android.widget.LinearLayout" ).child( index=0,
                                                                                           className="android.widget.LinearLayout" ).child(
                            index=1, className="android.widget.TextView" )
                        if obj.exists:
                            text = obj.info["text"].encode("utf-8")
                            if "0.0M​" in text:
                                break
                            else:
                                time.sleep( 3 )
                        else:
                            time.sleep(3)
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast("模块完成")
        return


def getPluginClass():
    return QQEmailClearCache

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("0d12dd17")
    z = ZDevice("0d12dd17")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"time_delay": "5"}
    o.action(d, z, args)
