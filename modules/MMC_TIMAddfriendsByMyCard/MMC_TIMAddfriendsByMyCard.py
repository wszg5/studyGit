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


class MMCTIMAddfriendsByMyCard:
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
        z.toast( "准备执行MMS版TIM我的名片夹加好友模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM加好友(我的名片夹)" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
        z.heartbeat( )

        if d( text="消息", resourceId="com.tencent.tim:id/ivTitleName" ).exists and not d( text="马上绑定",className="android.widget.Button" ).exists:
            z.toast( "登录状态正常，继续执行" )
        else:
            if d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).exists:
                d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).click( )
                z.sleep( 1 )
            elif d( text="消息", className="android.widget.TextView" ).exists and d( text="马上绑定",className="android.widget.Button" ).exists:
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

        add_count = int( args['add_count'] )  # 要添加多少人
        repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
        switch_card = args["switch_card"]
        z.heartbeat( )
        z.sleep( 8 )
        # while True:  # 由于网速慢或手机卡可能误点
        #     if d( index=1, className='android.widget.ImageView' ).exists:
        #         # d(index=0,className="android.widget.RelativeLayout").child( index=1,resourceId="com.tencent.tim:id/name", className='android.widget.ImageView' ).click()
        #         z.heartbeat( )
        #         d( index=2, className="android.widget.FrameLayout" ).child( index=0,
        #                                                                     className="android.widget.RelativeLayout" ).click( )
        #         # d( index=2, className="android.widget.FrameLayout" ).child( index=0,className="android.widget.RelativeLayout" ).child( index=1, className='android.widget.ImageView' ).click()
        #     if d( text="加好友" ).exists:  # 由于网速慢或手机卡可能误点
        #         d( text="加好友" ).click( )
        #         d( text="返回", className="android.widget.TextView" ).click( )
        #         d( index=2, className="android.widget.FrameLayout" ).child( index=0,
        #                                                                     className="android.widget.RelativeLayout" ).click( )
        #     z.sleep( 3 )
        #     if d( text='我的名片夹', resourceId='com.tencent.tim:id/name', className="android.widget.TextView" ).exists:
        #         z.heartbeat( )
        #         d( text='我的名片夹', resourceId='com.tencent.tim:id/name' ).click( )
        #         break
        # z.sleep( 1 )
        if d(index=1,className="android.widget.RelativeLayout").child(index=0,className="android.widget.ImageView").exists:
            d( index=1, className="android.widget.RelativeLayout" ).child( index=0,
                                                                           className="android.widget.ImageView" ).click()
        z.sleep(1)
        if d(description="名片夹").exists:
            d( description="名片夹" ).click()
            z.sleep(0.5)
        else:
            if d( index=1, className="android.widget.RelativeLayout" ).child( index=0,
                                                                              className="android.widget.ImageView" ).exists:
                d( index=1, className="android.widget.RelativeLayout" ).child( index=0,
                                                                               className="android.widget.ImageView" ).click( )
            z.sleep( 1 )
            if d( description="名片夹" ).exists:
                d( description="名片夹" ).click( )
            else:
                z.toast("可能你用的不是最新版本")
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return


        count = 0
        i = 0
        num = 0  # 请求失败的次数
        repo_material_cate_id = args["repo_material_cate_id"]
        # for i in range(0, add_count, +1):  # 总人数
        flag = True
        while count < add_count:
            numbers = self.repo.GetNumber( repo_number_cate_id, 60, 1 )  # 取出totalNumber条一小时内没有用过的号码
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"号码%s号仓库为空，等待中\"" % repo_number_cate_id ).communicate( )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            list = numbers  # 将取出的号码保存到一个新的集合
            Material = self.repo.GetMaterial( repo_material_cate_id, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % repo_material_cate_id ).communicate( )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            material = Material[0]['content']
            if flag:
                z.sleep( 1 )
                if d( text="添加第一张名片" ).exists:
                    z.heartbeat( )
                    d( text="添加第一张名片" ).click( )
                    z.sleep( 1 )
                else:
                    z.heartbeat( )
                    d( index=0, className="android.widget.RelativeLayout", resourceId="com.tencent.tim:id/name" ).child(index=1, className="android.widget.RelativeLayout" ).child(index=1, className="android.widget.ImageView", resourceId="com.tencent.tim:id/name" ).click( )
                    z.sleep( 1 )
                    d( index=2, text="编辑" ).click( )
                    z.sleep(1)
                    if d(text="重新扫描",className="android.widget.TextView").exists:
                        d( text="重新扫描", className="android.widget.TextView" ).click()
                        z.sleep(2)
                    z.heartbeat( )

                while d( index=3, className="android.widget.Button" ).exists:
                    z.heartbeat( )
                    d( index=3, className="android.widget.Button" ).click( )
                z.sleep( 1 )
                obj = d( index=0, className="com.tencent.widget.GridView",
                         resourceId="com.tencent.tim:id/photo_list_gv" ).child( index=0,
                                                                                className="android.widget.RelativeLayout" )
                if obj.exists:
                    obj.click( )
                    z.sleep( 1 )
                    d( text='确定', resourceId='com.tencent.tim:id/name' ).click( )
                    z.heartbeat( )
                    z.sleep( 4 )
                    flag = False

            obj = d( index=0, className="android.widget.LinearLayout", resourceId="com.tencent.tim:id/name" ).child(
                index=0, className="android.widget.EditText" )
            if obj.exists:
                obj.click( )
                z.heartbeat( )
                obj = obj.info['text']
                lenth = len( obj )
                t = 0
                while t < 11:
                    z.heartbeat( )
                    d.press.delete( )
                    t = t + 1
                z.input( list[0]['number'] )

            z.heartbeat( )
            z.sleep( 1 )
            i = 0
            d( text="完成" ).click( )
            z.sleep( 2 )
            Str = d.info  # 获取屏幕大小等信息
            height = Str["displayHeight"]
            width = Str["displayWidth"]

            # for index in range( 0, 3 ):
            z.heartbeat( )
            d.swipe( width / 2 + 20, height / 2, width / 2 + 20, 0, 5 )
            z.sleep( 1 )
            obj = d(  text="加好友",className="android.widget.Button")
            if obj.exists:
                z.heartbeat( )
                obj.click( )
                z.sleep( 1 )
            else:
                d.swipe( width / 2, height * 1 / 6, width / 2, height * 5 / 6 )
                continue
            if d(  text="加好友",className="android.widget.Button").exists:  # 请求失败活拒绝
                z.heartbeat( )
                num = num + 1  # 请求失败的次数＋１
                d.swipe( width / 2, height * 1 / 6, width / 2, height * 5 / 6 )
                continue
            if d( text="风险提示" ).exists:  # 风险提示
                z.heartbeat( )
                z.sleep( 1 )
                d( text="取消" ).click( )
                z.sleep( 1 )
                z.heartbeat( )
                d( text="返回", className="android.widget.TextView" ).click( )
                d.swipe( width / 2, height * 1 / 6, width / 2, height * 5 / 6 )
                continue
            if d( text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText' ).exists:  # 可直接添加为好友的情况
                z.heartbeat( )
                d( text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText' ).click( )
                if d( text="请求发送失败" ).exists:
                    z.toast("发送请求失败")
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
                elif d( resourceId='com.tencent.tim:id/name', text='添加失败，请勿频繁操作' ).exists:  # 操作过于频繁的情况
                        # z.sleep( 1 )
                        # z.heartbeat( )
                        # d(text = "确定",className="android.widget.TextView").click()
                        # z.sleep( 1 )
                        # z.heartbeat( )
                        # d(text="返回",className="android.widget.TextView").click()
                        z.toast( "频繁操作,跳出模块" )
                        return
            if d( text='必填', resourceId='com.tencent.tim:id/name' ).exists:  # 需要验证时
                z.heartbeat( )
                d( text="返回", className="android.widget.TextView" ).click( )
                num = 0
                d.swipe( width / 2, height * 1 / 6, width / 2, height * 5 / 6 )
                continue
            num = 0
            z.heartbeat( )
            obj = d( className='android.widget.EditText',
                     resourceId='com.tencent.tim:id/name' ).info  # 将之前消息框的内容删除
            obj = obj['text']
            lenth = len( obj )
            t = 0
            while t < lenth:
                z.heartbeat( )
                d.press.delete( )
                t = t + 1
            time.sleep( 1 )
            z.heartbeat( )
            d( className='android.widget.EditText',
               resourceId='com.tencent.tim:id/name' ).click( )  # 发送验证消息  material
            z.sleep( 1 )
            z.heartbeat( )
            z.input( material )
            if "是" in switch_card:
                if d( index=2, className="android.widget.CompoundButton", resourceId="com.tencent.tim:id/name" ).exists:
                    d( index=2, className="android.widget.CompoundButton",
                       resourceId="com.tencent.tim:id/name" ).click( )
                else:
                    if d( text="设置我的名片" ).exists:
                        d( text="设置我的名片" ).click( )
                        while True:
                            z.sleep( 3 )
                            z.heartbeat( )
                            d.dump( compressed=False )
                            if d( text="添加我的名片" ).exists:
                                d( text="添加我的名片" ).click( )
                            d( index=3, resourceId="com.tencent.tim:id/name",
                               className="android.widget.Button" ).click( )
                            z.sleep( 2 )
                            obj = d( index=0, className="com.tencent.widget.GridView",
                                     resourceId="com.tencent.tim:id/photo_list_gv" ).child(
                                index=0, className="android.widget.RelativeLayout" )
                            if obj.exists:
                                z.sleep( 1 )
                                z.heartbeat( )
                                obj.click( )
                                z.sleep( 3 )
                                d( text='确定', resourceId='com.tencent.tim:id/name' ).click( )
                                time.sleep( 3 )
                                z.heartbeat( )
                                d( text="完成" ).click( )
                                z.sleep( 1 )
                                z.heartbeat( )
                                d( text="返回" ).click( )
                                break
                            if d( index=0, resourceId="com.tencent.tim:id/name",
                                  className="android.widget.ImageButton" ).exists:
                                d( index=0, resourceId="com.tencent.tim:id/name",
                                   className="android.widget.ImageButton" ).click( )
                                d( text="退出" ).click( )
            d( text='下一步', resourceId='com.tencent.tim:id/ivTitleBtnRightText' ).click( )
            z.heartbeat( )
            z.sleep( 1 )
            d( text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText' ).click( )
            time.sleep( 1 )
            if d( text="请求发送失败" ).exists:
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            elif d( resourceId='com.tencent.tim:id/name', text='添加失败，请勿频繁操作' ).exists:  # 操作过于频繁的情况
                # d( text="确定", className="android.widget.TextView" ).click( )
                # z.sleep( 1 )
                # d( text="返回", className="android.widget.TextView" ).click( )
                z.toast( "频繁操作,跳出模块" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            count = count + 1
            if count == add_count:
                break
            if num > 3:  # 一直请求失败,跳出循环
                z.heartbeat( )
                print("该ＱＱ好暂时无法通过我的名片夹加好友，请切换账号或者执行其他操作")
                z.toast( "该ＱＱ好暂时无法通过我的名片夹加好友，请切换账号或者执行其他操作" )
                z.sleep( 5 )
                break
        z.sleep( 1 )
        z.toast( "模块完成" )
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCTIMAddfriendsByMyCard

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
            "repo_number_cate_id":"190","repo_material_cate_id":"39","add_count":"5","switch_card":"是"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
