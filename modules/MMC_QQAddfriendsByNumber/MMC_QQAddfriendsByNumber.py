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


class MMCQQAddfriendsByNumber:
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
        z.toast( "准备执行MMS版QQ搜索加好友模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ加好友(搜索查找)" )
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
        # loginStatusList = z.qq_getLoginStatus( d )
        # if loginStatusList is None:
        #     z.toast( "登陆新场景，现无法判断登陆状态" )
        #     now = datetime.datetime.now( )
        #     nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        #     cache.set( '%s_MMCQQAddfriendsByNumber_time' % d.server.adb.device_serial( ), nowtime,
        #                None )
        #     z.toast( '模块结束，保存的时间是%s' % nowtime )
        #     return
        # loginStatus = loginStatusList['success']
        # if loginStatus:
        #     z.toast( "卡槽QQ状态正常，继续执行" )
        # else:
        #     z.toast( "卡槽QQ状态异常，跳过此模块" )
        #     now = datetime.datetime.now( )
        #     nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        #     cache.set( '%s_MMCQQAddfriendsByNumber_time' % d.server.adb.device_serial( ), nowtime,
        #                None )
        #     z.toast( '模块结束，保存的时间是%s' % nowtime )
        #     return
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

        d( description='快捷入口' ).click( )
        z.sleep( 2 )
        if not d( text='扫一扫' ).exists:
            d( description='快捷入口' ).click( )
            z.sleep( 1 )
        z.heartbeat( )
        if d( textContains='加好友' ).exists:
            d( textContains='加好友' ).click( )
        else:
            d( resourceId='com.tencent.mobileqq:id/name', description='快捷入口' ).click( )
            d( textContains='加好友' ).click( )
        z.sleep( 1 )
        d( className='android.widget.EditText', index=0 ).click( )  # 刚进来时点击 QQ号/手机号/群/公众号
        z.sleep( 1 )
        # d(className='android.widget.EditText',index=0).click()   #QQ号/手机号/群/公众号
        # d(className='android.widget.EditText').set_text(list[0]['number'])  # 第一次添加的帐号 list[0]
        cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
        numbers = self.repo.GetNumber( cate_id, 120, 1 )  # 取出add_count条两小时内没有用过的号码
        if len( numbers ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % cate_id ).communicate( )
            z.sleep( 10 )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        z.heartbeat( )
        numbers = numbers[0]['number']
        z.input( numbers )
        time.sleep( 0.5 )
        d( text='找人:', resourceId='com.tencent.mobileqq:id/name' ).click( )
        z.sleep( 3 )
        add_count = int(args["add_count"])
        cate_id1 = args["repo_material_cate_id"]
        z.heartbeat( )
        for i in range( 1, add_count + 1, +1 ):  # 给多少人发消息
            Material = self.repo.GetMaterial( cate_id1, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id1 ).communicate( )
                z.sleep( 10 )
                if (args["time_delay"]):
                    z.sleep( int( args["time_delay"] ) )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            message = Material[0]['content']  # 取出验证消息的内容

            cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
            numbers = self.repo.GetNumber( cate_id, 120, 1 )  # 取出add_count条两小时内没有用过的号码
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % cate_id ).communicate( )
                z.sleep( 10 )
                if (args["time_delay"]):
                    z.sleep( int( args["time_delay"] ) )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            z.heartbeat( )
            numbers = numbers[0]['number']
            print(numbers)
            z.sleep( 1 )
            if d( text='没有找到相关结果', className='android.widget.TextView' ).exists:  # 没有这个人的情况
                time.sleep( 0.5 )
                d( resourceId='com.tencent.mobileqq:id/ib_clear_text', description='清空' ).click( )
                obj = d( className='android.widget.EditText', index=0 )  # QQ号/手机号/群/公众号
                if obj.exists:
                    obj.set_text( numbers )  # 下次要添加的号码
                obj = d( text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword' )
                if obj.exists:
                    obj.set_text( numbers )  # 下次要添加的号码
                d( textContains='找人' ).click( )
                while d( text='正在搜索…', index=1 ).exists:  # 网速不行的情况，让它不停等待
                    z.sleep( 1 )
                continue
            z.sleep( 1 )
            z.heartbeat( )
            # d.swipe(width / 2, height * 4 / 6, width / 2, height / 6);
            d( text='加好友' ).click( )
            z.sleep( 3 )
            if d( text="风险提示" ).exists:  # 风险提示
                d( text="取消" ).click( )
                z.sleep( 1 )
                d( text='返回', resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft' ).click( )
                d( resourceId='com.tencent.mobileqq:id/ib_clear_text', description='清空' ).click( )
                obj = d( className='android.widget.EditText', index=0 )
                if obj.exists:
                    obj.set_text( numbers )  # 要改为从库里取------------------------------
                obj = d( text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword' )
                if obj.exists:
                    obj.set_text( numbers )
                z.sleep( 1 )
                d( textContains='找人' ).click( )
                while d( text='正在搜索…', index=1 ).exists:
                    z.sleep( 1 )
                continue

            if d( text='加好友' ).exists:  # 拒绝被添加为好友的情况
                z.sleep( 1 )
                d( text='返回', resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft' ).click( )
                d( resourceId='com.tencent.mobileqq:id/ib_clear_text', description='清空' ).click( )
                obj = d( className='android.widget.EditText', index=0 )
                if obj.exists:
                    obj.set_text( numbers )  # 要改为从库里取------------------------------
                obj = d( text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword' )
                if obj.exists:
                    obj.set_text( numbers )
                z.sleep( 1 )
                d( textContains='找人' ).click( )
                while d( text='正在搜索…', index=1 ).exists:
                    z.sleep( 1 )
                continue
            time.sleep( 0.5 )


            z.heartbeat( )
            if d( text='必填', resourceId='com.tencent.mobileqq:id/name' ).exists:  # 要回答问题的情况
                d( text='返回', resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft' ).click( )
                z.sleep( 1 )
                d( text='返回', resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft' ).click( )
                d( resourceId='com.tencent.mobileqq:id/ib_clear_text', description='清空' ).click( )
                obj = d( className='android.widget.EditText', index=0 )
                if obj.exists:
                    obj.set_text( numbers )  # 下次要添加的号码-
                obj = d( text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword' )
                if obj.exists:
                    obj.set_text( numbers )
                z.sleep( 1 )
                d( textContains='找人' ).click( )
                while d( text='正在搜索…', index=1 ).exists:
                    z.sleep( 1 )
                continue

            z.heartbeat( )
            if d( textContains='问题' ).exists:  # 要回答问题的情况
                d( text='取消' ).click( )
                z.sleep( 0.5 )
                d( text='返回' ).click( )
                d( resourceId='com.tencent.mobileqq:id/ib_clear_text', description='清空' ).click( )
                obj = d( className='android.widget.EditText', index=0 )
                if obj.exists:
                    obj.set_text( numbers )  # 下次要添加的号码-
                obj = d( text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword' )
                if obj.exists:
                    obj.click( )
                    z.input( numbers )
                z.sleep( 1 )
                d( textContains='找人' ).click( )
                while d( text='正在搜索…', index=1 ).exists:
                    z.sleep( 1 )
                continue

            z.heartbeat( )
            z.sleep( 0.5 )
            obj = d( className='android.widget.EditText',
                     resourceId='com.tencent.mobileqq:id/name' ).info  # 将之前消息框的内容删除
            obj = obj['text']
            lenth = len( obj )
            t = 0
            while t < lenth:
                d.press.delete( )
                t = t + 1
            if d( className='android.widget.EditText', index=4 ).exists:
                z.input( message )
            obj = d( text='发送' )  # 不需要验证可直接添加为好友的情况
            if obj.exists:
                z.heartbeat( )
                obj.click( )
                if d( text='添加失败，请勿频繁操作', resourceId='com.tencent.mobileqq:id/name' ).exists:
                    if (args["time_delay"]):
                        z.sleep( int( args["time_delay"] ) )
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    cache.set( '%s_MMCQQAddfriendsByNumber_time' % d.server.adb.device_serial( ), nowtime,
                               None )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
                d( text='返回' ).click( )
                if add_count == i + 1:
                    if (args["time_delay"]):
                        z.sleep( int( args["time_delay"] ) )
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
                d( description='清空' ).click( )
                obj = d( className='android.widget.EditText', index=0 )
                if obj.exists:
                    obj.set_text( numbers )  # 要改为从库里取-------------------------------
                obj = d( text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword' )
                if obj.exists:
                    obj.set_text( numbers )
                d( textContains='找人' ).click( )
                while d( text='正在搜索…', index=1 ).exists:
                    z.sleep( 1 )
                continue
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        return
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCQQAddfriendsByNumber

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
            "repo_number_cate_id":"119","repo_material_cate_id":"39",'gender':"男","add_count":"5"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
