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


class QQEmailUpdateNameZ:
    def __init__(self):

        self.repo = Repo()

    def action(self, d, z, args):
        z.toast( "准备执行QQ邮箱修改昵称" )
        # z.toast( "正在ping网络是否通畅" )
        # z.heartbeat( )
        # i = 0
        # while i < 200:
        #     i += 1
        #     ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
        #     print( ping )
        #     if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
        #         z.toast( "网络通畅。开始执行：QQ邮箱修改昵称" )
        #         break
        #     z.sleep( 2 )
        # if i > 200:
        #     z.toast( "网络不通，请检查网络状态" )
        #     if (args["time_delay"]):
        #         z.sleep( int( args["time_delay"] ) )
        #     return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        repo_material_cateId= args["repo_material_cateId"]
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
        Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
        if len( Material ) == 0:
            d.server.adb.cmd( "shell","am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_material_cateId ).communicate( )
            z.sleep( 10 )
            return
        message = Material[0]['content']

        if d( description="写邮件和设置等功能" ).exists:
            d( description="写邮件和设置等功能" ).click( )
            z.sleep( 0.5 )
            if d( text="设置", resourceId="com.tencent.androidqqmail:id/w1" ).exists:
                d( text="设置", resourceId="com.tencent.androidqqmail:id/w1" ).click( )
                z.sleep( 0.5 )

        if d(textContains="@qq.com​",className="android.widget.TextView").exists:
            d( textContains="@qq.com​", className="android.widget.TextView" ).click()
            z.sleep(1)

        objName = d( index=1, className="android.widget.LinearLayout" ).child( index=1,
                                                                               className="android.widget.TextView" )
        name = ""
        if objName.exists:
            name = objName.info["text"]


        if d(index=1,className="android.widget.LinearLayout").child(index=2,className="android.widget.ImageView").exists:
            d( index=1, className="android.widget.LinearLayout" ).child( index=2, className="android.widget.ImageView" ).click()
            z.sleep(2)
            z.heartbeat()
            nameLen = len( name )
            if nameLen==1:
                if d(text="默认发信昵称​",className="android.widget.TextView").exists:
                    d( text="默认发信昵称​", className="android.widget.TextView" ).click()
                    time.sleep(0.5)
                    z.input( message.encode( "utf-8" ) )
                    time.sleep(0.5)
                    if d( index=0, resourceId="com.tencent.androidqqmail:id/a6",
                          className="android.widget.ImageButton" ).exists:
                        d( index=0, resourceId="com.tencent.androidqqmail:id/a6",
                           className="android.widget.ImageButton" ).click( )
                        z.sleep( 1 )
            else:
                if d(text=name,className="android.widget.TextView").exists:
                    d( text=name, className="android.widget.TextView" ).click()
                    for i in range( 0, nameLen ):
                        d.press.delete( )
                    z.input(message.encode("utf-8"))
                    if d(index=0,resourceId="com.tencent.androidqqmail:id/a6",className="android.widget.ImageButton").exists:
                        d( index=0, resourceId="com.tencent.androidqqmail:id/a6", className="android.widget.ImageButton" ).click()
                        z.sleep(1)
        z.toast("模块完成")
        return

    def input(self,z,height,text):
        if height>888:
            z.input(text)
        else:
            z.cmd( "shell", "am broadcast -a ZY_INPUT_TEXT --es text \\\"%s\\\"" % text )

def getPluginClass():
    return QQEmailUpdateNameZ

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4AYSK00041")
    z = ZDevice("HT4AYSK00041")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_cateId": "139",
            "time_delay": "5"}

    o.action(d, z, args)
