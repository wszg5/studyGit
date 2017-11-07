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


class MMC_QQAutoReply:
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
        cate_id = args["repo_material_cate_id"]
        sendTime = args["sendTime"]
        sendTime = sendTime.split( "-" )
        try:
            sendTimeStart = int( sendTime[0] )
            sendTimeEnd = int( sendTime[1] )
        except:
            z.toast( "发送间隔的参数格式有误" )
            return
        z.toast( "准备执行MMS版QQ监控自动回复" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：准备执行MMS版QQ监控自动回复" )
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
        add_count = int(args["add_count"])
        i = 0
        cate_id = args["repo_material_cate_id"]
        sendTime = args["sendTime"]
        sendTime = sendTime.split("-")
        try:
            sendTimeStart = int(sendTime[0])
            sendTimeEnd = int(sendTime[1])
        except:
            z.toast("发送间隔的参数格式有误")
            return
        meg_count = int(args["meg_count"])
        k = 0
        while i < add_count:
            if k == 10:
                z.toast("连续等待了100秒都没一条消息,停止模块")
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            if d(resourceId="com.tencent.mobileqq:id/no_chat",text="暂时没有新消息").exists:
                # d( resourceId="com.tencent.mobileqq:id/no_chat", text="暂时没有新消息" ).click()
                z.toast( "无消息,等待10秒" )
                z.sleep( 10 )
                z.heartbeat()
                k = k + 1
                continue
            k = 0
            obj = d( resourceId="com.tencent.mobileqq:id/recent_chat_list", index=0,
                     className="android.widget.AbsListView" ).child( index=1, className="android.widget.LinearLayout" )
            if obj.exists:
                z.heartbeat( )
                bounds = obj.info["bounds"]
                top = bounds["top"]
                bottom = bounds["bottom"]
                right = bounds["right"]

                obj2 = obj.child( index=0, resourceId="com.tencent.mobileqq:id/relativeItem",
                                  className="android.widget.RelativeLayout" ).child( index=1,
                                                                                     className="android.widget.RelativeLayout" ).child(
                    index=2, resourceId="com.tencent.mobileqq:id/unreadmsg", className="android.widget.TextView" )
                z.heartbeat( )
                if obj2.exists:
                    obj.child( index=0, resourceId="com.tencent.mobileqq:id/relativeItem",
                               className="android.widget.RelativeLayout" ).child( index=1,
                                                                                  className="android.widget.RelativeLayout" ).click( )
                    if (d( resourceId='com.tencent.mobileqq:id/input', className="android.widget.EditText" ).exists) and (not d(
                            resourceId="com.tencent.mobileqq:id/ivTitleBtnRightImage", description="群资料卡" ).exists):
                        if not d( text="QQ团队", resourceId="com.tencent.mobileqq:id/title" ).exists:
                            d( resourceId='com.tencent.mobileqq:id/input', className="android.widget.EditText" ).click( )
                            for j in range( 0, random.randint(1,meg_count) ):
                                Material = self.repo.GetMaterial( cate_id, 0, 1 )
                                if len( Material ) == 0:
                                    d.server.adb.cmd( "shell",
                                                      "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id ).communicate( )
                                    z.sleep( 10 )
                                    return
                                message = Material[0]['content']  # 取出发送消息的内容
                                z.input( message )
                                z.sleep( 1 )
                                if d( text="发送", resourceId="com.tencent.mobileqq:id/fun_btn" ).exists:
                                    d( text="发送", resourceId="com.tencent.mobileqq:id/fun_btn" ).click( )
                                    z.sleep( random.randint( sendTimeStart, sendTimeEnd ) )
                            i = i + 1

                    d.press.back()
                    z.sleep(2)
                    if obj2.exists:
                        i = i + 1
                        continue
                    if not obj.exists:
                        d.press.back( )
                        z.sleep(1)
                    z.heartbeat( )
                    d.swipe( right - 50, bottom - (bottom - top) / 2, right / 2, bottom - (bottom - top) / 2, 5 )
                    z.sleep( 1 )
                    if d( resourceId="com.tencent.mobileqq:id/name", description="删除" ).exists:
                        d( resourceId="com.tencent.mobileqq:id/name", description="删除" ).click( )
                        z.sleep( 1 )
                    else:
                        d.swipe( right - 50, bottom - (bottom - top) / 2, right / 2, bottom - (bottom - top) / 2,
                                 5 )
                        z.sleep( 1 )
                        if d( resourceId="com.tencent.mobileqq:id/name", description="删除" ).exists:
                            d( resourceId="com.tencent.mobileqq:id/name", description="删除" ).click( )
                            z.sleep( 1 )
                else:
                    d.swipe( right - 50, bottom - (bottom - top) / 2, right / 2, bottom - (bottom - top) / 2,5 )
                    z.sleep( 1 )
                    if d( resourceId="com.tencent.mobileqq:id/name", description="删除" ).exists:
                        d( resourceId="com.tencent.mobileqq:id/name", description="删除" ).click( )
                        z.sleep( 1 )

            else:
                z.toast( "无消息" )
                z.sleep( 5 )

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        return


def getPluginClass():
    return MMC_QQAutoReply

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("cda0ae8d")
    z = ZDevice("cda0ae8d")

    args = {"time_delay":"3","set_timeStart":"0","set_timeEnd":"0","startTime":"0","endTime":"8",
            "repo_material_cate_id":"39","add_count":"5","sendTime":"1-3","meg_count":"4"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
