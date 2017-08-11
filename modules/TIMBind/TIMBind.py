# coding:utf-8
import colorsys
import datetime
import os
import random
import time
import uuid

from PIL import Image

import util
from Repo import *
from imageCode import imageCode
from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from zservice import ZDevice

class TIMBind:
    def __init__(self):
        self.type = 'mobileqq'
        self.repo = Repo( )

    def action(self, d, z, args):
        z.toast( "准备执行TIM通讯录绑定" )
        z.sleep( 1 )
        z.heartbeat( )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM通讯录绑定" )
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

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        while True:                          #由于网速慢或手机卡可能误点
            if d( index=1, className='android.widget.ImageView' ).exists:
                z.heartbeat( )
                d( index=1, className="android.widget.FrameLayout" ).child( index=0,className="android.widget.RelativeLayout" ).click( )
            if d(text="加好友").exists:    #由于网速慢或手机卡可能误点
                d(text="加好友").click()
                d(text="返回",className="android.widget.TextView").click()
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,className="android.widget.RelativeLayout" ).click( )
            z.sleep( 2 )
            # if  d(textContains="通讯录").exists:
            d.swipe( width / 2 , height / 2, width / 2, 0, 5 )
            if d( index=10, resourceId="com.tencent.tim:id/group_item_layout",className="android.widget.RelativeLayout" ).child(
                    index=1,resourceId="com.tencent.tim:id/group_name",className="android.view.View").exists:
                z.heartbeat( )
                d( index=10, resourceId="com.tencent.tim:id/group_item_layout",
                   className="android.widget.RelativeLayout" ).child(index=1,resourceId="com.tencent.tim:id/group_name",className="android.view.View").click( )
                break
        while d( text='验证手机号码' ).exists:

            PhoneNumber = None
            j = 0
            z.heartbeat( )
            while PhoneNumber is None:
                j += 1
                PhoneNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )  # 获取接码平台手机号码
                z.heartbeat( )
                if j > 2:
                    z.toast( '取不到手机号码' )
                    if (args["time_delay"]):
                        z.sleep( int( args["time_delay"] ) )
                    return

            if not d( textContains='+86' ).exists:
                d( description='点击选择国家和地区' ).click( )
                if d( text='中国' ).exists:
                    d( text='中国' ).click( )
                else:
                    str = d.info  # 获取屏幕大小等信息
                    height = str["displayHeight"]
                    width = str["displayWidth"]
                    d.click( width * 5 / 12, height * 5 / 32 )
                    z.sleep( 1.5 )
                    z.input( '中国' )
                    z.sleep( 2 )
                    d( text='+86' ).click( )

            z.input( PhoneNumber )
            z.sleep( 1.5 )
            if d( text='下一步' ).exists:
                d( text='下一步' ).click( )
                z.sleep( 3 )

            e = 0
            while d( text='正在发送请求' ).exists:
                e += 1
                if e == 1:
                    z.sleep( 15 )
                else:
                    break
            z.heartbeat( )
            if d( text='确定' ).exists:
                d( text='确定' ).click( )
            z.sleep( 2 )
            z.heartbeat()
            code = self.scode.GetVertifyCode( PhoneNumber, self.scode.QQ_CONTACT_BIND, '4' )  # 获取接码验证码
            self.scode.defriendPhoneNumber( PhoneNumber, self.scode.QQ_CONTACT_BIND )
            if code == '':
                z.toast( PhoneNumber + '手机号,获取不到验证码' )
                if d( text='返回' ).exists:
                    d( text='返回' ).click( )
                if not d( textContains='中国' ).exists:
                    if d( text='返回' ).exists:
                        d( text='返回' ).click( )
                if d( className='android.view.View', descriptionContains='删除' ).exists:
                    d( className='android.view.View', descriptionContains='删除' ).click( )
                continue
            z.heartbeat( )
            z.input( code )
            if d( text='完成' ).exists:
                d( text='完成' ).click( )
            z.sleep( 1 )
            break

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return TIMBind

if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "HT54VSK01061" )
    z = ZDevice( "HT54VSK01061" )
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # d.dump(compressed=False)
    args = {"repo_material_id": "8", "StartIndex": "0", "EndIndex": "7", "time_delay": "3"};
    # z.server.install( )
    # z = 0
    o.action(d,z, args)