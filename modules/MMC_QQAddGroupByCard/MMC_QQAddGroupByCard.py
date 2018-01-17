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


class MMC_QQAddGroupByCard:
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
        z.toast( "准备执行MMS版QQ名片加群模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ加群(名片)" )
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
        z.heartbeat( )
        totalNumber = int( args['add_count'] )  # 要给多少人发消息

        cate_id = int( args["repo_number_id"] )  # 得到取号码的仓库号

        numbers = self.repo.GetNumber( cate_id, 60, totalNumber )  # 取出totalNumber条两小时内没有用过的号码
        if len( numbers ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % cate_id ).communicate( )
            z.sleep( 10 )
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)
        # z.sleep( 15 )
        z.heartbeat( )
        for i in range( 0, totalNumber, +1 ):
            cate_id = args["repo_material_cate_id"]
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

            QQnumber = list[i]['number']
            z.sleep( 2 )

            d.server.adb.cmd( "shell",'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=group&source=qrcode"' % QQnumber )  # 群页面
            z.sleep( 2 )
            z.heartbeat( )
            if d( text='QQ' ).exists:
                d( text='QQ' ).click( )
                time.sleep( 0.5 )
                if d( text='仅此一次' ).exists:
                    d( text='仅此一次' ).click( )

            obj = d( descriptionContains='群成员' ).child( className='android.widget.LinearLayout', index=1 ).child(
                className='android.widget.TextView' )
            if obj.exists:
                obj = obj.info
            else:
                continue
            z.heartbeat( )
            member = obj['text']
            member = filter( lambda ch: ch in '0123456789', member )
            member = int( member )
            if member == 0:
                continue
            d( text='申请加群' ).click( )
            z.sleep( 1 )
            if d( text='申请加群' ).exists:
                continue
            if d( resourceId="com.tencent.mobileqq:id/ivTitleBtnRightImage", className="android.widget.ImageView",description="群资料卡" ).exists:
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
            z.sleep(3)
            if d( text='发送' ).exists:
                z.toast("无法添加,停止模块")
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            z.heartbeat( )
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMC_QQAddGroupByCard

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"time_delay":"3","set_timeStart":"100","set_timeEnd":"120","startTime":"0","endTime":"8",
            "repo_number_id":"119","repo_material_cate_id":"39","add_count":"5"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
