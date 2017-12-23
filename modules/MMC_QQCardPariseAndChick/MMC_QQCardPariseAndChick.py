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


class MMC_QQCardPariseAndChick:
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
        z.toast( "准备执行MMS版QQ名片检测是否可点赞" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：MMS版QQ名片检测是否可点赞" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.mobileqq" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        z.heartbeat( )
        if d( text="消息", resourceId="com.tencent.mobileqq:id/ivTitleName", className="android.widget.TextView" ).exists:
            z.toast( "登录状态正常" )
        elif d( text='绑定手机号码' ).exists:
            while d( text='关闭' ).exists:
                d( text='关闭' ).click( )
                z.sleep( 0.5 )
            z.sleep( 1 )
        elif d( text='主题装扮' ).exists:
            while d( text='关闭' ).exists:
                d( text='关闭' ).click( )
                z.sleep( 0.5 )
        elif d( text='马上绑定' ).exists:
            while d( text='关闭' ).exists:
                d( text='关闭' ).click( )
                z.sleep( 0.5 )
        else:
            z.toast( "登录状态异常,停止模块" )
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return

        while True:                          #由于网速慢或手机卡可能误点
            z.heartbeat( )
            if d(index=1,className="android.widget.RelativeLayout").child( index=0, className='android.widget.Button',description="帐户及设置" ).exists:  # 点击ＱＱ头像.exists:
                z.sleep(1)
                z.heartbeat()
                d(index=1,className="android.widget.RelativeLayout").child( index=0, className='android.widget.Button',description="帐户及设置" ).click()
                z.heartbeat( )
                # d( resourceId="com.tencent.mobileqq:id/name", index=0,className='android.widget.RelativeLayout' ).child(
                #     index=0, className='android.widget.FrameLayout').child(resourceId="com.tencent.mobileqq:id/head", index=1,className='android.widget.ImageView').click( )  # 点击ＱＱ头像
                z.heartbeat( )
            if d( index=1, resourceId='com.tencent.mobileqq:id/head', className='android.widget.ImageView' ).exists:
                d( index=1, resourceId='com.tencent.mobileqq:id/head', className='android.widget.ImageView' ).click( )
                break
            if d(text="加好友").exists:    #由于网速慢或手机卡可能误点
                d(text="加好友").click()
                d(text="返回",className="android.widget.TextView").click()
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,className="android.widget.RelativeLayout" ).click( )
            z.sleep( 3 )
            z.heartbeat()
        for i in range(0,4):
            obj = d( index=0, className='android.widget.LinearLayout', resourceId="com.tencent.mobileqq:id/name" ).child(
                index=0, className="android.widget.LinearLayout" ).child(
                index=1, resourceId="com.tencent.mobileqq:id/info", className="android.widget.TextView" )
            if obj.exists:
                myAccount = obj.info["text"].encode( "utf-8" )
                z.sleep(0.5)
                break
            else:
                if d(text="返回",resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").exists:
                    d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click()
                    z.sleep(0.5)
                    if d( index=1, resourceId='com.tencent.mobileqq:id/head', className='android.widget.ImageView' ).exists:
                        d( index=1, resourceId='com.tencent.mobileqq:id/head',
                           className='android.widget.ImageView' ).click( )
        else:
            z.toast("获取不到自己的账号")
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        try:
            xxx = int(myAccount)
        except:
            z.toast("获取的账号不为数字")
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        i = 0
        repo_info_cate_id = args["repo_info_cate_id"]
        # time_limit1 = int( args["time_limit1"] )
        repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
        while True:
            numbers = self.repo.GetNumber( repo_number_cate_id, 0, 1 )

            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % repo_number_cate_id ).communicate( )
                z.sleep( 5 )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            z.heartbeat( )
            QQnumber = numbers[0]['number']  # 即将点赞的QQ号
            print(QQnumber)
            z.sleep( 1 )

            z.cmd( "shell",
                   'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"' % QQnumber )  # qq名片页面
            z.sleep( random.randint(5,7))
            if d( text='QQ', resourceId="android:id/text1" ).exists:
                z.heartbeat( )
                d( text='QQ', resourceId="android:id/text1" ).click( )
                z.sleep( 2 )
                z.heartbeat( )
                while d( text='仅此一次' ).exists:
                    z.heartbeat( )
                    d( text='仅此一次' ).click( )
            z.sleep( 1 )
            objtext1 = ""
            obj = d( descriptionContains="当前有" ).child( index=0,
                                                        className='android.widget.LinearLayout' ).child(
                index=1, className="android.widget.TextView" )
            if obj.exists:
                objtext1 = obj.info["text"].encode( "utf-8" )
            else:
                z.toast("这个获取不到点赞数")
                continue
            if obj.exists:
                # objtext = obj.info["text"].encode("utf-8")
                if d( descriptionContains="当前有" ).exists:
                    d( descriptionContains="当前有" ).click( )
                    z.sleep( 1 )
                    # d.dump( compressed=False )
            else:
                z.toast( "对方拒绝赞" )
                continue

            z.cmd( "shell",'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"' % QQnumber )  # qq名片页面
            z.sleep( random.randint( 5, 7 ) )
            if d( text='QQ', resourceId="android:id/text1" ).exists:
                z.heartbeat( )
                d( text='QQ', resourceId="android:id/text1" ).click( )
                z.sleep( 2 )
                z.heartbeat( )
                while d( text='仅此一次' ).exists:
                    z.heartbeat( )
                    d( text='仅此一次' ).click( )
            z.sleep( 1 )
            if objtext1 == "":
                z.toast( "获取不到点赞数" )
                continue
            obj = d( descriptionContains="当前有" ).child( index=0,className='android.widget.LinearLayout' ).child(
                index=1, className="android.widget.TextView" )
            if obj.exists:
                objtext3 = obj.info["text"].encode( "utf-8" )
                if int(objtext3)>int(objtext1):
                    z.toast("可以点赞")
                    break
                else:
                    z.toast("点赞无用")
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
            else:
                z.toast("获取不到点赞数")

        para = {"phoneNumber": myAccount, 'x_01': "QQ点赞","x_02":"活跃"}
        self.repo.PostInformation( repo_info_cate_id, para )
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        return



def getPluginClass():
    return MMC_QQCardPariseAndChick

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"time_delay":"3","set_timeStart":"0","set_timeEnd":"0","startTime":"0","endTime":"8",
            "repo_number_cate_id":"244","repo_info_cate_id":"271"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
