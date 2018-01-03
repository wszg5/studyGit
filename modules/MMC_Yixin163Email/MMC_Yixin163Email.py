# coding:utf-8
from __future__ import division
import base64
import colorsys
import logging
import re

from PIL import Image

from uiautomator import Device
from Repo import *
import os, time, datetime, random
import json

from zcache import cache
from zservice import ZDevice


class MMCYixin163Email:
    def __init__(self):
        self.repo = Repo()

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

    def action(self, d, z,args):
        z.toast( "准备执行MMS版易信189邮箱发信" )
        # z.toast("先导入通信录")
        # numList = self.getAddressList(d,z,args)    #导入的通讯录
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：易信189邮箱发信" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop im.yixin" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell","am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        if d(textContains="停止运行").exists:
            if d(text="确定").exists:
                d( text="确定" ).click()
                d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
                z.sleep(5)
        z.heartbeat( )
        if d( text="发现", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            z.toast( "登录状态正常" )
            d( text="发现", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
            z.sleep(1)
        else:
            z.toast( "登录状态异常" )
            return
        if d(text="立即体验",resourceId="im.yixin:id/new_presented_resources_experience_btn").exists:
            d( text="立即体验", resourceId="im.yixin:id/new_presented_resources_experience_btn" ).click()
            z.sleep(1)

        if d(text="更多功能").exists:
            d( text="更多功能" ).click()

        if d(text="邮箱提醒",resourceId="im.yixin:id/module_title").exists:
            d( text="邮箱提醒", resourceId="im.yixin:id/module_title" ).click()
            z.sleep(1)
        number = ""
        if d(textContains="@163.com",resourceId="im.yixin:id/plug_mail_list_account").exists:
            d(textContains="@163.com",resourceId="im.yixin:id/plug_mail_list_account").click()

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        repo_mail_cateId = int( args['repo_mail_cateId'] )
        repo_material_cateId = args["repo_material_cateId"]
        repo_material_cateId2 = args["repo_material_cateId2"]
        selectContent = args["selectContent"]
        count = int( args["count"] )

        for i in range(0,count):

            if d(text="写邮件").exists:
                d( text="写邮件").click()
            else:
                z.toast("没找到写邮件按钮")
                return


            emailType = args["emailType"]
            numbers = self.repo.GetNumber( repo_mail_cateId, 60, 1 )
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_mail_cateId ).communicate( )
                z.sleep( 10 )
                return
            Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_material_cateId ).communicate( )
                z.sleep( 10 )
                return
            message = Material[0]['content']

            Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
            if len( Material2 ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_material_cateId2 ).communicate( )
                z.sleep( 10 )
                return
            message2 = Material2[0]['content']

            d.click( 333 / 720 * width, 199 / 1280 * height )
            number = numbers[0]['number']
            if "@" not in number:
                z.toast( "%s仓库里的号码没有邮件类型,使用默认类型" % repo_mail_cateId )
                if emailType == "QQ邮箱":
                    z.input( number + "@qq.com " )
                elif emailType == "189邮箱":
                    z.input( number + "@189.cn " )
                elif emailType == "139邮箱":
                    z.input( number + "@139.com " )
                elif emailType == "163邮箱":
                    z.input( number + "@163.com " )
                elif emailType == "wo邮箱":
                    z.input( number + "@wo.cn " )
                else:
                    z.input( number + "@qq.com " )

            if selectContent == "只发主题" or selectContent == "主题内容都发":
                d.click( 303 / 720 * width, 354 / 1280 * height )
                z.input( message2.encode( "utf-8" ) )
                z.sleep( 0.5 )
                z.heartbeat( )

            if selectContent == "只发内容" or selectContent == "主题内容都发":
                d.click( 313 / 720 * width, 913 / 1280 * height )
                for i in range( 0, 21 ):
                    d.press.delete( )
                z.heartbeat( )
                z.input( message.encode( "utf-8" ) )


            if d(text="发送",resourceId="im.yixin:id/action_bar_right_clickable_textview").exists:
                d( text="发送", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).click()
                z.sleep(5)
                # if d( text="发送", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).exists:
                #     z.toast("发送失败,跳出模块")
                #     return
                top = 773 / 1280 * height
                left = 338 / 720 * width
                right = 380 / 720 * width
                bottom = 785 / 1280 * height
                color = self.WebViewBlankPages( d, top, left, right, bottom )
                if color != (21, 209, 165):
                    z.toast( "状态异常,停止模块" )
                    return
                else:
                    d.click(340 / 720 * width,780 / 1280 * height)
                    z.sleep(2)

        z.toast( "模块完成" )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCYixin163Email

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"time_delay":"3","repo_mail_cateId": "302", "repo_material_cateId": "39","count":"3","repo_material_cateId2":"255","selectContent":"只发内容","emailType":"QQ邮箱"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
