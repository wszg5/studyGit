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


class MMCQQConecrnMyParise:
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
        z.toast( "准备执行MMS版QQ关注我赞的人模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：MMS版QQ关注我赞的人模块" )
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
        # d(text='附近的人',className="android.widget.TextView").click()
        z.sleep(8)
        x = 0
        while (not d( text="去领心", className="android.widget.Button" ).exists) or (
        not d( text="附近的人", className="android.widget.TextView" ).exists):
            z.sleep( 2 )
            if x == 4:
                break
            x = x + 1
        if d(text="去领心",className="android.widget.Button").exists:
            d(index=0,className="android.widget.LinearLayout").child( index="2", className="android.widget.ImageView",resourceId="com.tencent.mobileqq:id/name").click()
            z.sleep(1)
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
        while objtemp.exists:
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
                if forwait == 3:
                    break
                else:
                    forwait = forwait + 1

        while not d( text='编辑交友资料' ).exists:
            time.sleep( 2 )
        d( descriptionContains='赞' ).child( className='android.view.View' ).click( )
        z.sleep( 3 )
        d( text='我赞过谁' ).click( )
        z.heartbeat( )
        z.sleep( 3 )
        obj3 = d( className='android.widget.AbsListView' ).child( className='android.widget.RelativeLayout', index=1 ) \
            .child( className='android.widget.RelativeLayout', index=1 ).child(
            className='android.widget.LinearLayout' )  # 用来点击的
        if not obj3.exists:
            # 我没赞过好友的情况
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        z.heartbeat( )
        set1 = set( )
        i = 1
        t = 1
        mmm = 0
        add_count = int( args['add_count'] )  # 要添加多少人
        while t < add_count + 1:
            obj = d( className='android.widget.AbsListView' ).child( className='android.widget.RelativeLayout',
                                                                     index=i ) \
                .child( className='android.widget.RelativeLayout', index=1 ).child(
                className='android.widget.LinearLayout' )  # 用来点击的
            obj1 = obj.child( className='android.widget.TextView' )
            if obj1.exists:
                z.heartbeat( )
                obj1 = obj1.info
                name = obj1['text']
                if name in set1:  # 判断是否已经关注过该联系人
                    i = i + 1
                    continue
                else:
                    time.sleep( 0.5 )
                    set1.add( name )
                    print(name)
                z.sleep( 1 )
                z.heartbeat( )
                obj.click( )
                while d( textContains='正在加载' ).exists:
                    z.sleep( 2 )
                z.heartbeat( )

                if d( text='关注' ).exists:
                    d( text='关注' ).click( )
                    z.sleep( 3 )
                if d( textContains='取消' ).exists:
                    d( text='取消' ).click( )
                if mmm == 0:
                    if d( text='关注' ).exists:  # 因为第一次会有个提醒页面，需要再点一次才能关注成功
                        d( text='关注' ).click( )
                        z.sleep( 1 )
                        z.heartbeat( )
                        if d( text='关注' ).exists:  # 因为第一次会有个提醒页面，需要再点一次才能关注成功
                            z.toast( '关注频繁，结束程序' )
                            now = datetime.datetime.now( )
                            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                            cache.set( '%s_MMCQQConecrnMyParise_time' % d.server.adb.device_serial( ), nowtime,
                                       None )
                            z.toast( '模块结束，保存的时间是%s' % nowtime )
                            return
                            # mmm = 1
                    # if d(text='关注').exists:
                    #     return

                    d.press.back( )
                    i = i + 1
                    t = t + 1
                else:
                    z.heartbeat( )
                    if d( text='关注' ).exists:
                        z.toast( '关注频繁，结束程序' )
                        now = datetime.datetime.now( )
                        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                        z.setModuleLastRun( self.mid )
                        z.toast( '模块结束，保存的时间是%s' % nowtime )
                        return
                    d.press.back( )
                    i = i + 1
                    continue
            else:
                if d( textContains='暂无更多' ).exists:
                    break
                if d( textContains='显示更多' ).exists:
                    d( textContains='显示更多' ).click( )
                d.swipe( width / 2, height * 4 / 5, width / 2, height / 5 )
                z.sleep( 2 )
                i = 1
                continue

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        return


def getPluginClass():
    return MMCQQConecrnMyParise

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("2400ba83db95")
    z = ZDevice("2400ba83db95")

    args = {"time_delay":"3","set_timeStart":"100","set_timeEnd":"120","startTime":"0","endTime":"8",
            "add_count":"5"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
