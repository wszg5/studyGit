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


class MMCQQConecrnMyFans:
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
        z.toast( "MMS版QQ关注我的粉丝模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：MMS版QQ关注我的粉丝模块" )
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
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        z.heartbeat( )
        if d( text='绑定手机号码' ).exists:
            d( text='关闭' ).click( )
        if d( textContains='匹配' ).exists:
            d.press.back( )
        z.heartbeat( )
        while not d( text='附近的人', className="android.widget.TextView" ).exists:
            if d( index=2, text="动态", className="android.widget.TextView" ).exists:
                d( index=2, text="动态", className="android.widget.TextView" ).click( )
            z.sleep( 1 )
            z.heartbeat( )
            if d( index=1, text="附近", className="android.widget.TextView" ).exists:
                z.sleep( 1 )
                z.heartbeat( )
                d( index=1, text="附近", className="android.widget.TextView" ).click( )
                z.sleep(8)
                z.heartbeat()
                break
        x = 0
        while (not d( text="去领心", className="android.widget.Button" ).exists) or (
        not d( text="附近的人", className="android.widget.TextView" ).exists):
            z.sleep( 2 )
            if x == 4:
                break
            x = x + 1
        if d( text="去领心", className="android.widget.Button" ).exists:
            d( index=0, className="android.widget.LinearLayout" ).child( index="2",
                                                                         className="android.widget.ImageView",
                                                                         resourceId="com.tencent.mobileqq:id/name" ).click( )
            z.sleep( 1 )
        # d(text='附近的人',className="android.widget.TextView").click()
        tempnum = 0
        objtemp = d( index=2, className="android.widget.LinearLayout" ).child( index=0,
                                                                               className="android.widget.LinearLayout",
                                                                               resourceId="com.tencent.mobileqq:id/name" ).child(
            index="0", className="android.widget.RelativeLayout" ).child( index=0, className="android.widget.ImageView",
                                                                          resourceId="com.tencent.mobileqq:id/icon" )
        while True:
            if objtemp.exists:
                z.sleep( 1 )
                break
            else:
                z.sleep( 2 )
                if tempnum == 4:
                    break
                else:
                    tempnum = tempnum + 1
        # d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=2).click()
        # z.sleep(5)
        if objtemp.exists:
            z.sleep( 1 )
            z.heartbeat( )
            objtemp.click( )
            if objtemp.exists:
                z.sleep( 1 )
                z.heartbeat( )
                objtemp.click( )

        forwait = 0
        while True:
            if d( text='附近点赞升级啦' ).exists:
                d( text='知道了' ).click( )
                break
            else:
                z.sleep( 1 )
                if forwait == 4:
                    break
                else:
                    forwait = forwait + 1

        while not d( text='编辑交友资料' ).exists:
            time.sleep( 2 )
        if d( textContains="粉丝", className="android.widget.TextView" ).exists:
            d.swipe( width / 2, height * 5 / 6, width / 2, height *5/ 6-200 )
            z.sleep( 1 )
            objNum = (d( textContains="粉丝", className="android.widget.TextView" ).info["text"].encode( "utf-8" ))
            try:
                objNum = int(objNum[3:][:-9])
                if objNum==0:
                    z.toast("粉丝数为0")
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
            except:
                pass
            z.heartbeat( )
            d( textContains="粉丝", className="android.widget.TextView" ).click( )
            z.sleep( 8 )
        else:
            d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
            if d( textContains="粉丝", className="android.widget.TextView" ).exists:
                z.sleep( 1 )
                z.heartbeat( )
                d( textContains="粉丝", className="android.widget.TextView" ).click( )
                z.sleep( 8 )
            else:
                z.toast("没找到粉丝")
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
        k = (300 - 160) / 888 * height
        x = 69 / 540 * width
        y1 = 228 / 888 * height
        swipt = (888 - 114) / 888 * height
        i = 0
        num = 0
        count = int( args["count"] )
        objinfo = d( index=1, className="android.widget.RelativeLayout" ).child( index=0,className="android.widget.LinearLayout" ).child( index=0,className="android.widget.LinearLayout" ).child(
            index=0, className="android.widget.TextView" )
        listInfo = []
        n = 0
        clickNum = 0
        while True:
            if n==3:
                z.toast("连续三个没法关注")
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            try:
                if clickNum==objNum:
                    z.toast("到底了")
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
            except:
                pass
            d.click( x, y1 + i * k )
            z.sleep( 2 )
            if not d( text="更多", resourceId="com.tencent.mobileqq:id/ivTitleBtnRightText" ).exists:
                z.toast( "已无粉丝可关注,停止模块" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            if objinfo.exists:
                text = objinfo.info["text"]
                if text not in listInfo:
                    listInfo.append( text )
                    try:
                        clickNum = clickNum + 1
                    except:
                        pass
            if d( text="关注", className="android.widget.Button" ).exists:
                z.heartbeat( )
                d( text="关注", className="android.widget.Button" ).click( )
                z.sleep( 2 )
                z.heartbeat( )
                if d( text="关注", className="android.widget.Button" ).exists:
                    z.toast( "操作频繁,无法关注了" )
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
                z.sleep( 1 )
                z.heartbeat( )
                num = num + 1
                n = 0
            else:
                n = n + 1
            d.press.back( )
            # d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click( )
            i = i + 1
            if num == count:
                z.toast( "已关注设定的粉丝数量,停止模块" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            if i == 5:
                z.sleep( 1 )
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                z.sleep( 3 )
                d.click( x, y1 + (i - 1) * k )
                z.sleep( 2 )
                if objinfo.exists:
                    text = objinfo.info["text"]
                    if text in listInfo:
                        z.toast( "到底了,停止模块" )
                        now = datetime.datetime.now( )
                        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                        z.setModuleLastRun( self.mid )
                        z.toast( '模块结束，保存的时间是%s' % nowtime )
                        return
                    else:
                        i = 0
                        d.press.back( )



def getPluginClass():
    return MMCQQConecrnMyFans

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
            "count":"50"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
