# coding:utf-8
from __future__ import division
import base64
import colorsys

import logging
import re

from PIL import Image

from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import os, time, datetime, random
import json

from zcache import cache
from zservice import ZDevice


class MMCTIMUpdateByMyCard:
    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )
    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def action(self, d, z,args):
        startTime = args["startTime"]
        endTime = args["endTime"]
        try:
            if self.repo.timeCompare( startTime, endTime ):
                z.toast( "该时间段不允许运行" )
                return
        except:
            z.toast( "输入的时间格式错误,请检查后再试" )
            return
        set_timeStart = int( args['set_timeStart'] )  # 得到设定的时间
        set_timeEnd = int( args["set_timeEnd"] )
        run_time = float( random.randint( set_timeStart, set_timeEnd ) )
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'锁定时间还差:%d分钟' % int( run_time - run_interval ) )
            z.sleep( 2 )
            return
        z.toast( "准备执行MMS版TIM修改我的名片夹加好友模块" )
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

        if d( text="消息", resourceId="com.tencent.tim:id/ivTitleName" ).exists and not d( text="马上绑定",className="android.widget.Button" ).exists:
            z.toast( "登录状态正常，继续执行" )
        else:
            if d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).exists:
                d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).click( )
                z.sleep( 1 )
            elif d( text="消息", className="android.widget.TextView" ).exists and d( text="马上绑定",className="android.widget.Button" ).exists:
                d( text="消息", className="android.widget.TextView" ).click( )
                z.sleep( 1 )
            elif d( text="返回" ).exists:
                d( text="返回" ).click( )
                z.sleep( 1 )

            else:
                z.toast( "登录状态异常，跳过此模块" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return

        z.heartbeat( )
        z.sleep( 8 )
        # while True:  # 由于网速慢或手机卡可能误点
        #     if d( index=1, className='android.widget.ImageView' ).exists:
        #         # d(index=0,className="android.widget.RelativeLayout").child( index=1,resourceId="com.tencent.tim:id/name", className='android.widget.ImageView' ).click()
        #         z.heartbeat( )
        #         d( index=2, className="android.widget.FrameLayout" ).child( index=0,
        #                                                                     className="android.widget.RelativeLayout" ).click( )
        #         # d( index=2, className="android.widget.FrameLayout" ).child( index=0,className="android.widget.RelativeLayout" ).child( index=1, className='android.widget.ImageView' ).click()
        #     if d( text="加好友" ).exists:  # 由于网速慢或手机卡可能误点
        #         d( text="加好友" ).click( )
        #         d( text="返回", className="android.widget.TextView" ).click( )
        #         d( index=2, className="android.widget.FrameLayout" ).child( index=0,
        #                                                                     className="android.widget.RelativeLayout" ).click( )
        #     z.sleep( 3 )
        #     if d( text='我的名片夹', resourceId='com.tencent.tim:id/name', className="android.widget.TextView" ).exists:
        #         z.heartbeat( )
        #         d( text='我的名片夹', resourceId='com.tencent.tim:id/name' ).click( )
        #         break
        # z.sleep( 1 )
        if d(index=1,className="android.widget.RelativeLayout").child(index=0,className="android.widget.ImageView").exists:
            d( index=1, className="android.widget.RelativeLayout" ).child( index=0,
                                                                           className="android.widget.ImageView" ).click()
        z.sleep(1)
        if d(description="名片夹").exists:
            d( description="名片夹" ).click()
            z.sleep(0.5)
        else:
            if d( index=1, className="android.widget.RelativeLayout" ).child( index=0,className="android.widget.ImageView" ).exists:
                d( index=1, className="android.widget.RelativeLayout" ).child( index=0,className="android.widget.ImageView" ).click( )
            z.sleep( 1 )
            if d( description="名片夹" ).exists:
                d( description="名片夹" ).click( )
            else:
                z.toast("可能你用的不是最新版本")
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return


        if d( text="设置我的名片" ).exists:
            z.heartbeat( )
            d( text="设置我的名片" ).click()
            z.sleep( 1 )
            d(text="添加我的名片").click()
            z.sleep(3)
        else:
            if d(index=0,description="我的名片",className="android.widget.FrameLayout").exists:
                d( index=0, description="我的名片", className="android.widget.FrameLayout" ).click()
                z.sleep(1)
                z.heartbeat()
                if d(text="编辑",resourceId="com.tencent.tim:id/ivTitleBtnRightText").exists:
                    d( text="编辑", resourceId="com.tencent.tim:id/ivTitleBtnRightText" ).click()
                    z.sleep(0.5)
                    if d(text="重新扫描",className="android.widget.TextView").exists:
                        d( text="重新扫描", className="android.widget.TextView" ).click()
                        z.sleep(1)

        while d(index=3,className="android.widget.Button").exists:
            z.heartbeat()
            d( index=3, className="android.widget.Button" ).click()
        z.sleep( 5 )
        obj = d( index=0, className="com.tencent.widget.GridView",
                 resourceId="com.tencent.tim:id/photo_list_gv" ).child( index=0,
                                                                        className="android.widget.RelativeLayout" )
        if obj.exists:
            obj.click( )
            z.sleep( 6 )
            d( text='确定', resourceId='com.tencent.tim:id/name' ).click( )
            num = 0              #休眠次数
            while not d( text='完成' ).exists:
                if num==2:
                    break
                else:
                    z.sleep(2)
                    num = num +1
            z.heartbeat( )
            if d(index=0,className="android.widget.ImageButton").exists and not d(text="完成").exists:
                z.sleep(1)
                z.heartbeat()
                # d( index=0, className="android.widget.ImageButton" ).click()
                z.toast("识别失败,请更改图片,停止模块")
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
        else:
            z.toast("没有图片可以上传,停止模块")
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        # if d( text="重选" ).exists:
        #     d( text="重选" ).click( )
        #     d( index=0, className="com.tencent.widget.GridView",
        #        resourceId="com.tencent.tim:id/photo_list_gv" ).child( index=0,
        #                                                               className="android.widget.RelativeLayout" ).click( )
        #     d( text='确定', resourceId='com.tencent.tim:id/name' ).click( )
        #     while d( text='正在识别' ).exists:
        #         time.sleep( 2 )
        z.sleep(2)
        while d(text="完成").exists:
            d(text="完成").click()
        z.sleep( 1 )
        z.toast( "模块完成" )
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCTIMUpdateByMyCard

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"time_delay":"3","set_timeStart":"1","set_timeEnd":"1","startTime":"0","endTime":"8"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
