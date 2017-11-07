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


class MMC_QQMatcherLoveMe:
    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )

    def WebViewBlankPages(self, d, top, left, right, bottom):
        # z.toast( "判断图片是否正常" )
        # Str = d.info  # 获取屏幕大小等信息
        # height = float( Str["displayHeight"] )
        # width = float( Str["displayWidth"] )

        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        # if i >= 0:
        #     getobj = d( index=2, className="android.widget.HorizontalScrollView" ).child(
        #         index=0, className="android.widget.LinearLayout", resourceId="com.tencent.mobileqq:id/name" ).child(
        #         index=i, className="android.widget.FrameLayout" )
        # else:
        #     getobj = d( index=0, className="android.widget.LinearLayout" ).child( index=0,
        #                                                                           resourceId="com.tencent.mobileqq:id/name",
        #                                                                           className="android.widget.RelativeLayout" ).child(
        #         index=1, resourceId="com.tencent.mobileqq:id/name", className="android.widget.RelativeLayout" )
        # if getobj.exists:
        # getobj = getobj.info["bounds"]
        # top = 827/1280 * height
        # left = 194/720 * width
        # right = 494/720 * width
        # bottom = 879/1280 * height
        d.screenshot( sourcePng )  # 截取整个输入验证码时的屏幕

        img = Image.open( sourcePng )
        box = (left, top, right, bottom)  # left top right bottom
        region = img.crop( box )  # 截取验证码的图片
        # show(region)    #展示资料卡上的信息
        image = region.convert( 'RGBA' )
        # 生成缩略图，减少计算量，减小cpu压力
        image.thumbnail( (200, 200) )
        max_score = None
        dominant_color = None
        for count, (r, g, b, a) in image.getcolors( image.size[0] * image.size[1] ):
            # 跳过纯黑色
            if a == 0:
                continue
            saturation = colorsys.rgb_to_hsv( r / 255.0, g / 255.0, b / 255.0 )[1]
            y = min( abs( r * 2104 + g * 4130 + b * 802 + 4096 + 131072 ) >> 13, 235 )
            y = (y - 16.0) / (235 - 16)
            # 忽略高亮色
            if y > 0.9:
                continue

            score = (saturation + 0.1) * count
            if score > max_score:
                max_score = score
                dominant_color = (r, g, b)  # 红绿蓝
        # else:
        #     dominant_color = None
        return dominant_color


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
        z.toast( "准备执行MMS版QQ匹配喜欢我的人" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：MMS版QQ匹配喜欢我的人" )
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
        d.dump(compressed=False)
        if d( index=1, textContains="喜欢了你", className="android.widget.TextView" ).exists:
            z.sleep( 1 )
            z.heartbeat( )
            d( index=1,textContains="喜欢了你", className="android.widget.TextView" ).click( )
            z.sleep( 8 )
        else:
            d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
            if d( index=1, textContains="喜欢了你", className="android.widget.TextView" ).exists:
                z.sleep( 1 )
                z.heartbeat( )
                d( index=1,textContains="喜欢了你", className="android.widget.TextView" ).click( )
                z.sleep( 8 )
            else:
                z.toast("没找到有人喜欢你")
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
        textnum = args["textnum"]
        i = 0
        d.click(617/720*width,1105/1280*height)
        z.sleep(8)
        if d(index=0,className="android.widget.TextView").exists:
            d( index=0, className="android.widget.TextView" ).click()
            z.sleep(5)
        if d(text="去评分",className="android.widget.TextView").exists:
            d( text="去评分", className="android.widget.TextView" ).click()
            z.sleep(10)
        while i <textnum:
            colorResource2 = self.WebViewBlankPages( d, 1195 / 1280 * height, 294 / 720 * width, 424 / 720 * width,
                                                     1210 / 1280 * height )
            colorResource3 = self.WebViewBlankPages( d, 720 / 1280 * height, 326 / 720 * width, 482 / 720 * width,
                                                     735 / 1280 * height )
            if colorResource2 == (100, 100, 100):
                z.toast( "附近暂时没有更多的人" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            colorResource3 = self.WebViewBlankPages( d, 720 / 1280 * height, 326 / 720 * width, 482 / 720 * width,
                                                     735 / 1280 * height )
            if colorResource3 == (18, 183, 245):
                z.toast( "今日喜欢达到上限" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            colorResource = self.WebViewBlankPages( d, 338 / 1280 * height, 178 / 720 * width, 506 / 720 * width,
                                                    570 / 1280 * height )
            if colorResource == (236, 225, 226):
                z.sleep( 1 )
            else:
                # d.click( 540 / 720 * width, 1137 / 1280 * height )
                d.swipe( width / 5, height  / 2, width* 5 / 6, height / 2 )
                z.sleep( 1 )
                colorResource3 = self.WebViewBlankPages( d, 720 / 1280 * height, 326 / 720 * width, 482 / 720 * width,
                                                         735 / 1280 * height )
                if colorResource3 == (18, 183, 245):
                    z.toast( "今日喜欢达到上限" )
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
                # else:
                #     d.press.back( )
                #     z.sleep(1)
                #     d.press.back( )


        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        return


def getPluginClass():
    return MMC_QQMatcherLoveMe

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("cda0ae8d")
    z = ZDevice("cda0ae8d")

    args = {"time_delay":"3","set_timeStart":"100","set_timeEnd":"120","startTime":"0","endTime":"8",
            "textnum":"5"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
