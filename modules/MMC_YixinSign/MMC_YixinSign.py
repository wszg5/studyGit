# coding:utf-8
from __future__ import division
import base64
import logging
import re

from uiautomator import Device
from Repo import *
import os, time, datetime, random
import json

from zcache import cache
from zservice import ZDevice


class MMCYixinSign:
    def __init__(self):
        self.repo = Repo()

    def action(self, d, z,args):

        z.toast( "准备执行MMS版易信签到开宝箱" )
        # z.toast("先导入通信录")
        # numList = self.getAddressList(d,z,args)    #导入的通讯录
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：易信签到开宝箱" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop im.yixin" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell","am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        if d(textContains="停止运行").exists:
            if d(text="确定").exists:
                d( text="确定" ).click()
                d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
                z.sleep(5)
        z.heartbeat( )
        if d( text="发现", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            z.toast( "登录状态正常" )
            d( text="发现", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
        else:
            z.toast( "登录状态异常" )
            return
        if d(text="立即体验",resourceId="im.yixin:id/new_presented_resources_experience_btn").exists:
            d( text="立即体验", resourceId="im.yixin:id/new_presented_resources_experience_btn" ).click()
            z.sleep(1)
        if d(text="星币商城",resourceId="im.yixin:id/module_title").exists:
            d( text="星币商城", resourceId="im.yixin:id/module_title" ).click()
            z.sleep(5)
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.click( 102 / 720 * width, 1225 / 1280 * height )
        z.sleep(2)

        if d(index=2,description="签到").exists:
            d( index=2, description="签到" ).click()
            z.sleep(1)
            d.click( 638 / 720 * width, 451 / 1280 * height )
            z.sleep(2)
            if d(description="打开宝箱 Link").exists:
                d( description="打开宝箱 Link" ).click()

        else:
            z.toast("已签到")

        z.toast( "模块完成" )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCYixinSign

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
