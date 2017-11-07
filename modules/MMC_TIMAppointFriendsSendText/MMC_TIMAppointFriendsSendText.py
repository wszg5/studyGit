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


class MMCTIMAppointFriendsSendText:
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
        cate_id = args["repo_material_cate_id"]
        sendTime = args["sendTime"]
        sendTime = sendTime.split( "-" )
        try:
            sendTimeStart = int( sendTime[0] )
            sendTimeEnd = int( sendTime[1] )
        except:
            z.toast( "发送间隔的参数格式有误" )
            return
        z.toast( "准备执行MMS版TIM指定好友互聊" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM指定好友互聊(唤醒)" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
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
        repo_number_cate_id = args["repo_number_cate_id"]
        add_count = int(args["add_count"])
        i = 0
        cate_id = args["repo_material_cate_id"]
        sendTime = args["sendTime"]
        sendTime = sendTime.split("-")
        try:
            sendTimeStart = int(sendTime[0])
            sendTimeEnd = int(sendTime[1])
        except:
            z.toast("发送间隔的参数格式有误")
            return
        meg_count = int(args["meg_count"])
        while i < add_count:
            numbers = self.repo.GetNumber( repo_number_cate_id, 0, 10000,"normal","NO" )
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell","am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % repo_number_cate_id ).communicate( )
                z.sleep( 5 )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            z.heartbeat( )
            QQnumber = numbers[random.randint(0,len(numbers)-1)]['number']  # 即将点赞的QQ号
            print(QQnumber)

            d.server.adb.cmd( "shell",'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=wpa\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"' % QQnumber )  # 临时会话  # qq名片页面
            z.sleep(6)
            if d( text="TIM" ).exists:
                d( text="TIM" ).click( )
                z.sleep( 2 )
                z.heartbeat( )
                if d( text="仅此一次" ).exists:
                    d( text="仅此一次" ).click( )
                    z.sleep( 2 )
                    z.heartbeat( )
            if d( description="快捷入口", className="android.widget.ImageView" ).exists:
                continue
            if d(text="加为好友",className="android.widget.TextView").exists:
                d( text="加为好友", className="android.widget.TextView" ).click()
                z.sleep(3)
                if d( text="加为好友", className="android.widget.TextView" ).exists:
                    z.toast("无法添加对方")
                    continue
                if d(text="下一步").exists:
                    d( text="下一步" ).click()
                    z.sleep(1)
                if d(text="发送").exists:
                    d( text="发送" ).click()
                    z.sleep(3)
                    # if d( text="发送" ).exists and not d(text="加为好友",className="android.widget.TextView").exists:
                    #     z.toast( "可能添加频繁了" )
                    #     now = datetime.datetime.now( )
                    #     nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    #     z.setModuleLastRun( self.mid )
                    #     z.toast( '模块结束，保存的时间是%s' % nowtime )
                    #     return
                    d.server.adb.cmd( "shell",
                                      'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=wpa\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"' % QQnumber )  # 临时会话  # qq名片页面
                    z.sleep( 6 )
                    if d( text="TIM" ).exists:
                        d( text="TIM" ).click( )
                        z.sleep( 2 )
                        z.heartbeat( )
                        if d( text="仅此一次" ).exists:
                            d( text="仅此一次" ).click( )
                            z.sleep( 2 )
                            z.heartbeat( )
                    if d( description="快捷入口", className="android.widget.ImageView" ).exists:
                        continue
                    if d( text="加为好友", className="android.widget.TextView" ).exists:
                        z.toast("等待对方同意添加")
                        continue
            flag = True
            if d(resourceId='com.tencent.tim:id/input',className="android.widget.EditText").exists:
                if flag:
                    d( resourceId='com.tencent.tim:id/input', className="android.widget.EditText" ).click()
                for j in range(0,random.randint(1,meg_count)):
                    Material = self.repo.GetMaterial( cate_id, 0, 1 )
                    if len( Material ) == 0:
                        d.server.adb.cmd( "shell",
                                          "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id ).communicate( )
                        z.sleep( 10 )
                        now = datetime.datetime.now( )
                        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                        z.setModuleLastRun( self.mid )
                        z.toast( '模块结束，保存的时间是%s' % nowtime )
                        return
                    message = Material[0]['content']  # 取出发送消息的内容
                    z.input(message)
                    z.sleep(1)
                    if d(text="发送",resourceId="com.tencent.tim:id/fun_btn").exists:
                        d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).click()
                        z.sleep(random.randint(sendTimeStart,sendTimeEnd))
                        flag = False
                i = i + 1
            z.sleep(random.randint(3,8))


        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        return


def getPluginClass():
    return MMCTIMAppointFriendsSendText

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"time_delay":"3","set_timeStart":"0","set_timeEnd":"0","startTime":"0","endTime":"8","repo_number_cate_id":"119",
            "repo_material_cate_id":"39","add_count":"5","sendTime":"5-8","meg_count":"4"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
