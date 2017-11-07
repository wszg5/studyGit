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


class MMCQQAddGroupByNumber:
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

    def Gender(self, d, z):
        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        obj = d( resourceId='com.tencent.tim:id/name', className='android.widget.ImageView' )
        if obj.exists:
            z.heartbeat( )
            obj = obj.info
            obj = obj['bounds']  # 验证码处的信息
            left = obj["left"]  # 验证码的位置信息
            top = obj['top']
            right = obj['right']
            bottom = obj['bottom']

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
                z.heartbeat( )
                score = (saturation + 0.1) * count
                if score > max_score:
                    max_score = score
                    dominant_color = (r, g, b)
            # print("---------------------------------------------------------------------------")
            # print(dominant_color)
            z.heartbeat( )
            if None == dominant_color:
                return '不限'
            red = dominant_color[0]
            blue = dominant_color[2]

            if red > blue:
                # print('女')
                return '女'
            else:
                # print('男')
                return '男'
        else:  # 没有基本资料的情况
            return '不限'

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
        z.toast( "准备执行MMS版QQ搜索加群模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ加群(搜索查找)" )
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
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d( resourceId='com.tencent.mobileqq:id/name', description='快捷入口' ).click( )
        z.sleep( 1 )
        z.heartbeat( )
        if d( textContains='加好友' ).exists:
            d( textContains='加好友' ).click( )
        else:
            d( resourceId='com.tencent.mobileqq:id/name', description='快捷入口' ).click( )
            d( textContains='加好友' ).click( )
        z.sleep( 2 )
        d( text='找群' ).click( )
        z.sleep( 1 )
        add_count = int( args['add_count'] )  # 要添加多少人
        cate_id = int( args["repo_number_id"] )  # 得到取号码的仓库号
        repo_material_cate_id = args["repo_material_cate_id"]
        i = 0
        while i < add_count :
            Material = self.repo.GetMaterial( repo_material_cate_id, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % repo_material_cate_id ).communicate( )
                z.sleep( 10 )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            message = Material[0]['content']  # 取出验证消息的内容

            numbers = self.repo.GetNumber( cate_id, 120, 1,"normal","NO" )  # 取出add_count条两小时内没有用过的号码
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % cate_id ).communicate( )
                z.sleep( 10 )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            QQgroup = numbers[0]['number']
            d( textContains='QQ号/手机号' ).click( )
            z.input( QQgroup )
            # z.input("605234073")
            d( textContains='找群:' ).click( )
            z.sleep( 2 )
            if d( textContains='没有找到相关结果' ).exists:
                d( description='清空' ).click( )
                continue

            d( text='申请加群' ).click( )
            z.sleep( 3 )
            if d( text='申请加群' ).exists:
                if d(resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft",description="返回按钮").exists:
                    d( resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft", description="返回按钮" ).click()
                    z.sleep(0.5)
                    if d( description='清空' ).exists:
                        d( description='清空' ).click()

                    continue
            if d(resourceId="com.tencent.mobileqq:id/ivTitleBtnRightImage",className="android.widget.ImageView",description="群资料卡").exists:
                if i + 1>=add_count:
                    break
                if d(className="android.widget.LinearLayout",description="返回消息").exists:
                    d( className="android.widget.LinearLayout", description="返回消息" ).click()
                    z.sleep(1)
                    d( resourceId='com.tencent.mobileqq:id/name', description='快捷入口' ).click( )
                    z.sleep( 1 )
                    z.heartbeat( )
                    if d( textContains='加好友' ).exists:
                        d( textContains='加好友' ).click( )
                    else:
                        d( resourceId='com.tencent.mobileqq:id/name', description='快捷入口' ).click( )
                        d( textContains='加好友' ).click( )
                    z.sleep( 2 )
                    d( text='找群' ).click( )
                    i = i + 1
                    continue
            obj = d( className='android.widget.EditText' ).info  # 将之前消息框的内容删除
            obj = obj['text']
            lenth = len( obj )
            m = 0
            while m < lenth:
                d.press.delete( )
                m = m + 1
            z.input( message )
            d( text='发送' ).click( )
            z.sleep( 3 )
            if d( text='发送' ).exists:
                z.toast( '操作频繁，程序结束' )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            if i + 1 >= add_count:
                break
            i = i + 1
            z.sleep( 2 )
            d( text='关闭' ).click( )
            d( description='清空' ).click( )
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCQQAddGroupByNumber

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"time_delay":"3","set_timeStart":"1","set_timeEnd":"1","startTime":"0","endTime":"8",
            "repo_number_id":"119","repo_material_cate_id":"39","add_count":"5"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
