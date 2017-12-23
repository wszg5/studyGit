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


class MMCTIMEmailSendText:
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
    
    def action(self, d, z, args):
        set_timeStart = int( args['set_timeStart'] )  # 得到设定的时间
        set_timeEnd = int( args["set_timeEnd"] )
        run_time = float( random.randint( set_timeStart, set_timeEnd ) )
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'锁定时间还差:%d分钟' % int( run_time - run_interval ) )
            z.sleep( 2 )
            return
        z.toast( "MMC版TIM邮件发消息" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：MMC版TIM邮件发消息" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        repo_mail_cateId = int( args['repo_mail_cateId'] )
        repo_material_cateId = args["repo_material_cateId"]
        d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        z.heartbeat( )
        if d( text="消息", resourceId="com.tencent.tim:id/ivTitleName" ).exists and not d( text="马上绑定",
                                                                                         className="android.widget.Button" ).exists:
            z.toast( "登录状态正常，继续执行" )
        else:
            if d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).exists:
                d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).click( )
                z.sleep( 1 )
            elif d( text="消息", className="android.widget.TextView" ).exists and d( text="马上绑定",
                                                                                   className="android.widget.Button" ).exists:
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
        count = int( args["count"] )
        Str = d.info  # 获取屏幕大小等信息
        height = Str["displayHeight"]
        width = Str["displayWidth"]
        a = 0
        while True:
            if d( index=1, className='android.widget.ImageView' ).exists:
                z.heartbeat( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,
                                                                            className="android.widget.RelativeLayout" ).click( )
            if d( text="加好友" ).exists:  # 由于网速慢或手机卡可能误点
                d( text="加好友" ).click( )
                z.heartbeat( )
                d( text="返回", className="android.widget.TextView" ).click( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,
                                                                            className="android.widget.RelativeLayout" ).click( )
            z.sleep( 3 )
            if d( text='邮件' ).exists:
                z.heartbeat( )
                d( text='邮件' ).click( )
                break
            if a == 5:
                z.toast("此时状态可能异常,跳出模块")
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            else:
                a = a + 1
        time.sleep( 4 )
        n = 0
        if not d( text="开始写邮件" ).exists:
            while d( text='开通QQ邮箱', className='android.widget.Button' ).exists:
                z.heartbeat( )
                z.sleep( 1 )
                d( text='开通QQ邮箱', className='android.widget.Button' ).click( )
                if n == 3:
                    z.toast( "邮箱开通失败,停止模块" )
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
                else:
                    n = n + 1
            if d( text="QQ邮箱" ).exists:
                x = 73 / 540
                y = 272 / 888
                d.click( x * width, y * height )

            z.sleep( 2 )
            z.heartbeat( )
            b = 0
            while d( text="跳过", resourceId="com.tencent.tim:id/ivTitleBtnRightText",
                     className="android.widget.TextView" ).exists:
                d( text="跳过", resourceId="com.tencent.tim:id/ivTitleBtnRightText",
                   className="android.widget.TextView" ).click( )
                if b ==5:
                    z.toast( "此时状态可能异常,跳出模块" )
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
                else:
                    b = b + 1
        z.sleep( 3 )
        num = 0
        selectContent = args["selectContent"]
        repo_material_cateId2 = args["repo_material_cateId2"]
        sendCount = int(args["sendCount"])
        while num < count:
            numbers = self.repo.GetNumber( repo_mail_cateId, 120, count )
            Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
            if len( Material ) == 0:
                z.toast( "%s仓库为空" % repo_material_cateId )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            message = Material[0]['content']
            Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
            if len( Material2 ) == 0:
                z.toast( "%s仓库为空" % repo_material_cateId2 )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            message2 = Material2[0]['content']

            if d( text="开始写邮件" ).exists:
                d( text="开始写邮件" ).click( )
            if d(text="写邮件").exists:
                d( text="写邮件" ).click()
            # while not d(text="发送").exists:
            #     z.sleep(2)
            z.sleep( 14 )

            if selectContent == "只发主题" or selectContent == "主题内容都发":
                x2 = 266 / 720
                y2 = 371 / 1280
                d.click( x2 * width, y2 * height )  # 点击到编辑主题处
                z.heartbeat( )
                z.input( message2.encode( 'utf-8' ) )
                z.sleep( 2 )
            if selectContent == "只发内容" or selectContent == "主题内容都发":
                x3 = 80 / 540
                y3 = 430 / 888
                d.click( x3 * width, y3 * height )  # 点击到编辑消息处
                z.heartbeat( )
                z.input( message.encode( 'utf-8' ) )
                z.sleep( 2 )
            x1 = 260 / 540
            y1 = 156 / 888
            d.click( x1 * width, y1 * height )  # 点击到收件人
            z.heartbeat( )
            for i in range( 0, count ):
                QQEmail = numbers[i]['number']
                z.input( QQEmail + "@qq.com " )
                z.input(" ")
                print(QQEmail + "@qq.com")
            z.sleep( 2 )
            z.heartbeat( )

            z.heartbeat( )
            x3 = 270 / 540
            y3 = 850 / 888
            d.click( x3 * width, y3 * height )
            z.sleep( 5 )
            z.heartbeat( )
            if num == count:
                break
            top = 1213 / 1280 * height
            left = 130 / 720 * width
            right = 544 / 720 * width
            bottom = 1254 / 1280 * height
            color = self.WebViewBlankPages( d, top, left, right, bottom )
            if color == (127, 188, 255):
                z.toast( "状态异常,停止模块" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            if color == (0, 121, 255):
                z.toast( "状态异常,停止模块" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            if color != None:
                z.toast( "状态异常,停止模块" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            if d( text="邮件", resourceId="com.tencent.tim:id/ivTitleBtnLeft",
                  className="android.widget.TextView" ).exists:
                z.sleep( 1 )
                d( text="邮件", resourceId="com.tencent.tim:id/ivTitleBtnLeft",
                   className="android.widget.TextView" ).click( )

            else:
                z.toast( "非正常状态,停止模块" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
                # x4 = 431 / 540
                # y4 = 348 / 888
                # d.click(x4*width,y4*height)
                # z.sleep(1)
                # z.heartbeat()
                # d(text="邮件",resourceId="com.tencent.tim:id/ivTitleBtnLeft",className="android.widget.TextView").click()
                # while 1:
                #     if d(text='发送', className='android.widget.Button').exists:
            num = num + 1
        z.toast( "模块完成" )
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        if (args["time_delay"]):
            time.sleep( int( args["time_delay"] ) )


def getPluginClass():
    return MMCTIMEmailSendText

if __name__ == "__main__":

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")

    args = {"repo_mail_cateId": "119", "repo_material_cateId": "39", "time_delay": "3","count":"5",
            "set_timeStart":"0","set_timeEnd":"0","repo_material_cateId2":"255","selectContent":"只发主题","sendCount":"5"}    #cate_id是仓库号，length是数量
    o.action(d,z,args)


