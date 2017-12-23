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


class MMCQQNearbyPeopleSendText:
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

        # condition = self.timeinterval(d, z, args )

        # if condition == 'end':
        #     z.sleep( 2 )
        #     return
        set_timeStart = int( args['set_timeStart'] )  # 得到设定的时间
        set_timeEnd = int( args["set_timeEnd"] )
        run_time = float( random.randint( set_timeStart, set_timeEnd ) )
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'锁定时间还差:%d分钟' % int( run_time - run_interval ) )
            z.sleep( 2 )
            return
        z.toast( "准备执行MMS版QQ附近的人发消息" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：MMS版QQ附近的人发消息" )
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
        # d(description='快捷入口').click()
        # d( descriptionContains='快捷入口' ).click( )
        # d(text='加好友/群').click()
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
                break
        x = 0
        while (not d( text="去领心", className="android.widget.Button" ).exists) or (not d(text="附近的人",className="android.widget.TextView").exists):
            z.sleep(2)
            if x ==4:
                break
            x = x + 1

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
        z.sleep(0.5)
        if d( text=getGender ).exists:
            d( text=getGender ).click( )
            z.sleep(0.5)
            d(text=selectTime).click()
            d( text='完成' ).click( )
        z.sleep(3)
        while not d( textContains='等级' ).exists:
            z.sleep( 2 )
        z.heartbeat( )
        # prisenum = int( args['prisenum'] )
        # concernnum = int( args['concernnum'] )
        textnum = int( args['textnum'] )
        # count = max( prisenum, concernnum, textnum )
        t = 0
        i = 4
        # if d(text='颜值匹配',className="android.widget.TextView").exists:
        #    i = 4
        # else:
        #     pass
        nameList = []
        while t < textnum:
            forClick = d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                                                                          index=i )
            if forClick.exists:
                z.heartbeat( )
                # if forClick.child(index=2,className="android.widget.RelativeLayout").child(text="广告",className="android.widget.TextView").exists:
                #     i = i + 1
                #     continue
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

                if t < textnum:
                    d( text='发消息' ).click( )
                    z.sleep( 1 )
                    if d( text='发消息' ).exists:
                        z.toast( '无法发消息' )
                        d.press.back( )
                        i = i + 1
                        continue

                    d( className='android.widget.EditText' ).click( )
                    cate_id = args["repo_material_id"]
                    Material = self.repo.GetMaterial( cate_id, 0, 1 )
                    if len( Material ) == 0:
                        d.server.adb.cmd( "shell",
                                          "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id ).communicate( )
                        z.sleep( 10 )
                        now = datetime.datetime.now( )
                        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                        z.setModuleLastRun( self.mid )
                        z.toast( '模块结束，保存的时间是%s' % nowtime )
                        return
                    message = Material[0]['content']
                    z.input( message )
                    d( text='发送' ).click( )

                # d(text='返回').click()
                if d( index=1, resourceId='com.tencent.mobileqq:id/rlCommenTitle',
                      className="android.widget.RelativeLayout" ).child( index=0,
                                                                         className="android.widget.LinearLayout" ).child(
                        index=0, className="android.widget.ImageView" ).exists:
                    d( index=1, resourceId='com.tencent.mobileqq:id/rlCommenTitle',
                       className="android.widget.RelativeLayout" ).child( index=0,
                                                                          className="android.widget.LinearLayout" ).child(
                        index=0,
                        className="android.widget.ImageView" ).click( )
                i = i + 1
                t = t + 1
            # elif d( className='android.widget.AbsListView' ).child( className='android.widget.RelativeLayout',
            #                                                         index=i ).child( text='广告' ).exists:  # 被点击条件不存在的情况
            #     z.heartbeat( )
            #     i = i + 1
            #     continue
            elif d( className='android.widget.AbsListView' ).child( className='android.widget.RelativeLayout',index=i ).child(
                        index=2,className="android.widget.RelativeLayout").child(text="广告",className="android.widget.TextView").exists:
                    i = i + 1
                    continue
            else:
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                z.sleep(2)
                # str = d.info  # 获取屏幕大小等信息
                # width = str["displayWidth"]
                # clickCondition = d( className='android.widget.AbsListView' )
                # obj = clickCondition.info
                # obj = obj['visibleBounds']
                # top = int( obj['top'] )
                # bottom = int( obj['bottom'] )
                # y = bottom - top
                # d.swipe( width / 2, y, width / 2, 0 )
                # z.sleep( 3 )
                i = 1

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        return


def getPluginClass():
    return MMCQQNearbyPeopleSendText

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("HT54WSK00081")
    z = ZDevice("HT54WSK00081")

    args = {"time_delay":"3","set_timeStart":"0","set_timeEnd":"0","startTime":"0","endTime":"8",
            "textnum":"20","gender":"男","selectTime":"1小时","repo_material_id":"39"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
