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


class MMCTIMAddGroupByCard:
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
        z.toast( "准备执行MMS版TIM搜索加群模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM加群(搜索查找)" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
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

        totalNumber = int( args['totalNumber'] )  # 要给多少人发消息

        repo_number_id = int( args["repo_number_id"] )  # 得到取号码的仓库号

        # numbers = self.repo.GetNumber( repo_number_id, 60, totalNumber, "normal","NO" )  # 取出t1条两小时内没有用过的号码
        # if len( numbers ) == 0:
        #     d.server.adb.cmd( "shell",
        #                       "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % repo_number_id ).communicate( )
        #     z.sleep( 10 )
        #     return
        # list = numbers  # 将取出的号码保存到一个新的集合
        # for i in range (0,totalNumber,+1):
        i = 0
        num = 1
        while True:
            numbers = self.repo.GetNumber( repo_number_id, 60, 1, "normal" )  # 取出t1条两小时内没有用过的号码
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库为空，等待中\"" % repo_number_id ).communicate( )
                z.sleep( 10 )
                return
            list = numbers  # 将取出的号码保存到一个新的集合
            # print( list )
            # z.sleep(15)
            z.sleep( 1 )
            z.heartbeat( )
            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial( cate_id, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            message = Material[0]['content']

            # QQnumber = list[i]['number']
            QQnumber = list[0]['number']
            print(QQnumber)
            z.toast( "准备唤醒的群号为" + QQnumber )
            z.sleep( 3 )
            z.heartbeat( )
            d.server.adb.cmd( "shell",
                              'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=group"' % QQnumber )  # 群页面
            z.sleep( 7 )
            z.heartbeat( )
            if d( text='TIM' ).exists:
                d( text='TIM' ).click( )
                time.sleep( 0.5 )
                while d( text='仅此一次' ).exists:
                    d( text='仅此一次' ).click( )

            if d( text='申请加群' ).exists:
                d( text='申请加群' ).click( )
                z.sleep( 10 )
            else:
                # i = i +1
                continue
            z.sleep( 1 )
            if d( text='申请加群' ).exists:
                # i = i +1
                continue
            # obj = d(descriptionContains='群成员').child(className='android.widget.LinearLayout',index=1).child(className='android.widget.TextView')
            # if obj.exists:
            #     obj = obj.info
            # else:
            #     d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
            #     if obj.exists:
            #         obj = obj.info
            #     else:
            #         i = i +1
            #         continue
            # z.heartbeat()
            # member = obj['text']
            # member = filter(lambda ch: ch in '0123456789', member)
            # member = int(member)
            # if member==0:
            #     i = i + 1
            #     continue
            switch = args["switch"]
            if switch == "是":
                obj = d( className='android.widget.EditText' ).info  # 将之前消息框的内容删除
                obj = obj['text']
                lenth = len( obj )
                m = 0
                while m < lenth:
                    d.press.delete( )
                    m = m + 1
                z.input( message )
            z.sleep( 2 )
            if d( text='发送' ).exists:
                d( text='发送' ).click( )
                z.sleep( 6 )
            if d( text='发送' ).exists:
                i = i + 1
                continue
            print(QQnumber + "发送成功")
            if num == totalNumber:
                z.toast( "模块完成" )
                break
            num = num + 1
            # i = i +1
            z.sleep( 2 )
            z.heartbeat( )

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCTIMAddGroupByCard

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
            "repo_number_id":"229","repo_material_id":"255","totalNumber":"5","switch":"否"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
