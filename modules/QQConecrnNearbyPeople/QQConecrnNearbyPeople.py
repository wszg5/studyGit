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


class QQConecrnNearbyPeople:
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
        z.toast( "准备执行MMS版QQ附近的人关注" )
        z.sleep( 1 )
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
            return

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        z.heartbeat()
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
        if d(textContains='匹配').exists:
            d.press.back()
        z.heartbeat()
        z.heartbeat()
        if d( text="联系人", resourceId="com.tencent.mobileqq:id/name" ).exists:
            d( text="联系人", resourceId="com.tencent.mobileqq:id/name" ).click( )
            time.sleep( 1 )
            d( text="添加", resourceId="com.tencent.mobileqq:id/ivTitleBtnRightText" ).click( )
            time.sleep(1)
            d(text='查看附近的人').click()
            time.sleep(10)
        while d(textContains='附近内容正在加载中').exists:
            z.sleep(2)
        # x = 0
        # while (not d( text="去领心", className="android.widget.Button" ).exists) or (not d(text="附近的人",className="android.widget.TextView").exists):
        #     z.sleep(2)
        #     if x ==4:
        #         break
        #     x += 1
        if d( text="去领心", className="android.widget.Button" ).exists:
            d( index=0, className="android.widget.LinearLayout" ).child( index="2",
                                                                         className="android.widget.ImageView",
                                                                         resourceId="com.tencent.mobileqq:id/name" ).click( )
            z.sleep( 1 )

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

        getGender = args['gender']
        selectTime = args["selectTime"]
        # if getGender != '不限':
        d( resourceId='com.tencent.mobileqq:id/ivTitleBtnRightImage' ).click( )
        d( text='筛选附近的人' ).click( )
        if d( text=getGender ).exists:
            d( text=getGender ).click( )
            z.sleep(0.5)
            d(text=selectTime).click()
            d( text='完成' ).click( )
        while not d( textContains='等级' ).exists:
            z.sleep( 2 )
        z.heartbeat( )
        # prisenum = int( args['prisenum'] )
        concernnum = int( args['concernnum'] )
        # textnum = int( args['textnum'] )
        # count = max( prisenum, concernnum, textnum )
        t = 0
        i = 3
        nameList = []
        while t < concernnum:
            forClick = d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                                                                          index=i )
            if forClick.exists:
                z.heartbeat( )
                if forClick.child(index=0,className="android.widget.RelativeLayout").child(index=3,className="android.widget.LinearLayout").child( index=0,text='直播中' ).exists:
                    i = i + 1
                    continue
                if forClick.child(index=0,resourceId="com.tencent.mobileqq:id/icon",className="android.widget.ImageView").exists:
                    forClick.child(index=0,resourceId="com.tencent.mobileqq:id/icon",className="android.widget.ImageView").click( )
                else:
                    i = i + 1
                    continue

                while not d( textContains='关注' ).exists:
                    z.sleep( 2 )
                    if d( text='知道了' ).exists:
                        d( text='知道了' ).click( )

                obj = d(index=1,className="android.widget.RelativeLayout",resourceId="com.tencent.mobileqq:id/name").child(index=0,className="android.widget.LinearLayout").child(
                    index=0,className="android.widget.LinearLayout").child(index=0,className="android.widget.TextView")
                if obj.exists:
                    obj = obj.info["text"].encode("utf-8")
                    if obj in nameList:
                        i = i + 1
                        d.press.back( )
                        continue
                    else:
                        nameList.append(obj)
                z.sleep( 2 )
                if t < concernnum:
                    if d( text='关注' ).exists:
                        d( text='关注' ).click( )
                        if d( text='关注' ).exists:
                            d( text='关注' ).click( )
                            if d( text='关注' ).exists:
                                z.toast( "关注频繁,进行其他操作" )
                                now = datetime.datetime.now( )
                                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                                z.setModuleLastRun( self.mid )
                                z.toast( '模块结束，保存的时间是%s' % nowtime )
                                return
                        while d(text="返回",resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").exists:
                            d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click()
                        i = i + 1
                        continue
                # if d( index=1, resourceId='com.tencent.mobileqq:id/rlCommenTitle',
                #       className="android.widget.RelativeLayout" ).child( index=0,
                #                                                          className="android.widget.LinearLayout" ).child(
                #         index=0, className="android.widget.ImageView" ).exists:
                #     d( index=1, resourceId='com.tencent.mobileqq:id/rlCommenTitle',
                #        className="android.widget.RelativeLayout" ).child( index=0,
                #                                                           className="android.widget.LinearLayout" ).child(
                #         index=0,
                #         className="android.widget.ImageView" ).click( )
                i = i + 1
                t = t + 1


            elif d( className='android.widget.AbsListView' ).child( className='android.widget.RelativeLayout',
                                                                    index=i ).child(

                    index=2, className="android.widget.RelativeLayout" ).child( text="广告",
                                                                                className="android.widget.TextView" ).exists:
                i = i + 1
                continue
            else:
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                z.sleep( 2 )
                i = 1

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        return


def getPluginClass():
    return QQConecrnNearbyPeople

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("cc0e9474")
    z = ZDevice("cc0e9474")

    args = {"time_delay":"3","set_timeStart":"100","set_timeEnd":"120","startTime":"0","endTime":"8",
            "concernnum":"5","gender":"男","selectTime":"全部"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
