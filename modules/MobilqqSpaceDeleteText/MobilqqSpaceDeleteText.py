# coding=utf-8
from __future__ import division
import colorsys
import os

from PIL import Image

from smsCode import smsCode
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *


class MobilqqSpaceDeleteText:
    def __init__(self):
        self.repo = Repo( )

    def action(self, d, z, args):
        z.toast( "准备执行QQ空间删除所有说说" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ空间删除所有说说" )
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
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
        z.heartbeat( )

        if d( text='消息' ).exists:  # 到了通讯录这步后看号有没有被冻结
            z.toast( "卡槽状态正常，继续执行" )
        else:
            z.toast( "卡槽状态异常，跳过此模块" )
            return
        z.heartbeat( )
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        z.heartbeat( )
        if d( text='绑定手机号码' ).exists:
            d( text='关闭' ).click( )
        if d( textContains='匹配' ).exists:
            d.press.back( )              #等同于按返回键
        while not d( text='相册', className="android.widget.TextView" ).exists:
            if d( index=2, text="动态", className="android.widget.TextView" ).exists:
                d( index=2, text="动态", className="android.widget.TextView" ).click( )
            z.sleep( 1 )
            z.heartbeat( )
            if d( index=1, text="好友动态", className="android.widget.TextView" ).exists:
                z.sleep( 1 )
                z.heartbeat( )
                d( index=1, text="好友动态", className="android.widget.TextView" ).click( )
                z.sleep( random.randint( 1, 3 ) )
        z.heartbeat()
        while not d(text="说说",className='android.widget.TextView').exists:
            z.sleep(1)
        if d(text="说说",className='android.widget.TextView').exists:
            d( text="说说", className='android.widget.TextView' ).click()
            # z.sleep(1)
            z.sleep(2)
        x1 = 516 / 540
        y1 = 173 / 888
        obj = d(index=6,className="android.widget.RelativeLayout",resourceId="com.tencent.mobileqq:id/name").child(
            index=2,className="android.widget.ImageView",resourceId="com.tencent.mobileqq:id/name")
        while obj.exists:
            z.sleep(1)
            z.heartbeat()
            d.click(x1*width,y1*height)
            z.sleep(2)
            z.heartbeat()
            if d(text="删除",className='android.widget.TextView'):
                d(text="删除",className='android.widget.TextView').click()
                z.sleep(1)
                z.heartbeat()
                while d(text='确认',resourceId="com.tencent.mobileqq:id/dialogRightBtn").exists:
                    d( text='确认', resourceId="com.tencent.mobileqq:id/dialogRightBtn" ).click()
                    z.sleep(2)
        z.toast("模块完成")
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return MobilqqSpaceDeleteText


if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "HT524SK00685" )
    z = ZDevice( "HT524SK00685" )
    z.server.install( )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).wait( )
    args = {"time_delay": "3"}  # repo_name_id:QQ修改昵称仓库号，birthday_ xxx :年龄范围
    o.action( d, z, args )
    # a = o.WebViewBlankPages(d)
    # print(a)


