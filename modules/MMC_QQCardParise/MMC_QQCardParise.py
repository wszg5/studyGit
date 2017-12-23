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


class MMCQQCardParise1:
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
        z.toast( "准备执行MMS版QQ名片点赞模块有锁" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：MMS版QQ名片点赞模块有锁" )
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
        count = int( args['count'] )  # 要添加多少人
        i = 0
        # time_limit1 = int( args["time_limit1"] )
        repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
        click_count = int( args["click_count"] )
        timeLock = args["timeLock"]
        switch = args["switch"]
        flag = True
        for i in range( 0, count ):  # 总人数
            numbers = self.repo.GetNumber( repo_number_cate_id, timeLock, 1 )

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
            objtext = ''
            objtext1 = ""
            obj = d( descriptionContains="当前有" ).child( index=0,
                                                        className='android.widget.LinearLayout' ).child(
                index=1, className="android.widget.TextView" )
            if obj.exists:
                objtext1 = obj.info["text"].encode( "utf-8" )
                objtext = objtext1
            else:
                if switch == "跳过":
                    z.toast( "这个获取不到点赞数,跳过" )
                    continue
                obj = d( descriptionContains="当前有" )
                flag = False
            if click_count >= 10:
                click_count = 10
            if obj.exists:
                # objtext = obj.info["text"].encode("utf-8")
                for j in range( 0, random.randint( 1, 5 ) ):
                    if d( descriptionContains="当前有" ).exists:
                        d( descriptionContains="当前有" ).click( )
                        z.sleep( 1 )
                        # d.dump( compressed=False )
                        if objtext != "":
                            objtext2 = d( descriptionContains="当前有" ).child( index=0,
                                                                             className='android.widget.LinearLayout' ).child(
                                index=1, className="android.widget.TextView" ).info["text"].encode( "utf-8" )
                            if objtext == objtext2:
                                z.toast( "今天无法继续赞了，停止模块" )
                                now = datetime.datetime.now( )
                                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                                z.setModuleLastRun( self.mid )
                                z.toast( '模块结束，保存的时间是%s' % nowtime )
                                return
                            objtext = objtext2
                        else:
                            z.toast( "这个获取不到点赞数,跳过" )
                            continue
            else:
                z.toast( "对方拒绝赞" )
                continue

            if flag:
                z.cmd( "shell",
                       'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"' % QQnumber )  # qq名片页面
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
                    z.toast( "这个获取不到点赞数,跳过" )
                    continue
                obj = d( descriptionContains="当前有" ).child( index=0, className='android.widget.LinearLayout' ).child(
                    index=1, className="android.widget.TextView" )
                if obj.exists:
                    objtext3 = obj.info["text"].encode( "utf-8" )
                    if int( objtext3 ) > int( objtext1 ):
                        z.toast( "可以点赞" )
                        i = i + 1
                    else:
                        z.toast( "点赞无用" )
                        break
                else:
                    z.toast( "这个获取不到点赞数,跳过" )
                    continue

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        return



def getPluginClass():
    return MMCQQCardParise1

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("c0e5994f")
    z = ZDevice("c0e5994f")

    args = {"time_delay":"3","set_timeStart":"100","set_timeEnd":"120","startTime":"0","endTime":"8",
            "repo_number_cate_id":"244","count":"10","click_count":"11","timeLock":"60","switch":"跳过"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
