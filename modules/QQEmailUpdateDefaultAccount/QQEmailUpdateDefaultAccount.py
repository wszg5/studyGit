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


class QQEmailUpdateDefaultAccount:
    def __init__(self):

        self.repo = Repo()

    def action(self, d, z, args):
        z.toast( "准备执行QQ邮箱修改默认发信帐号" )
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
            if d( textContains="收件箱​",resourceId="com.tencent.androidqqmail:id/t0" ).exists:
                z.toast( "状态正常，继续执行" )
                break
            else:
                if d( text="温馨提示​", className="android.widget.TextView" ).exists:
                    d( text="确定", className="android.widget.Button" ).click( )
                    z.sleep( 1 )
                    break
                elif d( text='密码错误，请重新输入' ).exists:
                    z.toast("密码错误，状态不正常")
                    return
                elif d(text="收件人：",resourceId="com.tencent.androidqqmail:id/nd").exists and d(text="写邮件",resourceId="com.tencent.androidqqmail:id/ac").exists:
                    flag1 = True
                    break
                elif d(index=1,text="写邮件​",resourceId="com.tencent.androidqqmail:id/ac",className="android.widget.TextView").exists:
                    while not d( text="离开", className="android.widget.Button" ).exists:
                        d.press.back( )
                        z.sleep( 1 )
                    if d( text="离开", className="android.widget.Button" ).exists:
                        d( text="离开", className="android.widget.Button" ).click( )
                    break
                else:
                    if t>=1:
                        z.toast( "状态异常，跳过此模块" )
                        return
                    else:
                        d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
                        d.server.adb.cmd( "shell","am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                        time.sleep(5)

        if d( description="写邮件和设置等功能" ).exists:
            d( description="写邮件和设置等功能" ).click( )
            z.sleep( 0.5 )
            if d( text="设置", resourceId="com.tencent.androidqqmail:id/w1" ).exists:
                d( text="设置", resourceId="com.tencent.androidqqmail:id/w1" ).click( )
                z.sleep( 0.5 )

        if d(textContains="@qq.com​",className="android.widget.TextView").exists:
            d( textContains="@qq.com​", className="android.widget.TextView" ).click()
            z.sleep(1)

        objName = d( index=2, className="android.widget.LinearLayout" ).child( index=1,
                                                                               className="android.widget.TextView" )
        account = ""
        if objName.exists:
            account = objName.info["text"]
        this_type = account.split( "@" )[1].encode("utf-8")
        account = account.split("@")[0]

        account_type = args["account_type"]
        if account_type=="英文或foxmail":
            account_type = random.choice(["英文","foxmail"])
        if account_type=="数字":
            if this_type == "qq.com​":
                try:
                    num = int(account)
                    z.toast( "不需要修改默认发信帐号" )
                    return
                except:
                    pass
            objName.click( )
        elif account_type=="英文":
            if this_type=="qq.com​":
                try:
                    num = int(account)
                except:
                    z.toast( "不需要修改默认发信帐号" )
                    return
            objName.click()
        elif account_type=="foxmail":
            if this_type=="foxmail.com​":
                z.toast( "不需要修改默认发信帐号" )
                return
            # print this_type
            objName.click()
        for index in [2,1,0]:
            obj = d(index=index, className="android.widget.LinearLayout").child(index=0, className="android.widget.LinearLayout").child(index=0, className="android.widget.TextView")
            if obj.exists:
                info = obj.info["text"]
                if info:
                    account2 = info.split("@")[0]
                    this_type2 = info.split("@")[1].encode("utf-8")
                    # try:
                    #     account2 = int(account2)
                    #     obj.click( )
                    #     for i in range( 2 ):
                    #         time.sleep( 1 )
                    #         d.press.back( )
                    #     break
                    # except:
                    #     pass
                    if account_type == "数字":
                        if this_type2 == "qq.com​":
                            try:
                                num = int( account2 )
                                obj.click( )
                                for i in range( 2 ):
                                    time.sleep( 1 )
                                    d.press.back( )
                                break
                            except:
                                pass
                        else:
                            print this_type2
                    elif account_type == "英文":
                        if "qq.com​" in this_type2:
                            try:
                                num = int( account2 )
                            except:
                                obj.click( )
                                for i in range( 2 ):
                                    time.sleep( 1 )
                                    d.press.back( )
                                break
                    elif account_type == "foxmail":
                        if "foxmail.com" in this_type2:
                            obj.click( )
                            for i in range( 2 ):
                                time.sleep( 1 )
                                d.press.back( )
                            break


        z.toast("模块完成")
        return

    def input(self,z,height,text):
        if height>888:
            z.input(text)
        else:
            z.cmd( "shell", "am broadcast -a ZY_INPUT_TEXT --es text \\\"%s\\\"" % text )


def getPluginClass():
    return QQEmailUpdateDefaultAccount

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49XSK01916")
    z = ZDevice("HT49XSK01916")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"time_delay": "5","account_type":"英文或foxmail"}

    o.action(d, z, args)
