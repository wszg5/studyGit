# coding:utf-8
from __future__ import division
import base64
import logging
import re

from uiautomator import Device
from Repo import *
import os, time, datetime, random
import json

from zcache import cache
from zservice import ZDevice


class MMCYixinAddFriendsByNumber:
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
        z.toast( "准备执行MMS版易信搜索加好友版模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：易信加好友版模块(搜索)" )
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
        z.heartbeat( )
        if d( text="好友", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            z.toast( "登录状态正常" )
            d( text="好友", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
        else:
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        if d(text="添加好友",resourceId="im.yixin:id/lblfuncname").exists:
            d( text="添加好友", resourceId="im.yixin:id/lblfuncname" ).click()
            z.sleep(1)
            if d(text="搜索手机或易信号",resourceId="im.yixin:id/add_friend_by_search_keyword").exists:
                d( text="搜索手机或易信号", resourceId="im.yixin:id/add_friend_by_search_keyword" ).click()
        add_count = int(args["add_count"])
        i = 0
        num = 0
        nameList = []
        repo_cate_id = args["repo_cate_id"]
        while True:
            if num == add_count:
                z.toast("加的好友达到设定的值了")
                break

            numbers = self.repo.GetNumber( repo_cate_id, 120, 1,"normal" )  # 取出add_count条两小时内没有用过的号码
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % repo_cate_id ).communicate( )
                z.sleep( 10 )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            QQNumber = numbers[0]['number']
            z.input(QQNumber)
            search = d( index=0, className="android.widget.LinearLayout" ).child( index=0,
                                                                                  className="android.widget.RelativeLayout" ).child(
                index=0, resourceId="im.yixin:id/add_friend_by_search_keyword" )
            if d(text="搜索",resourceId="im.yixin:id/add_friend_by_search_submit").exists:
                d( text="搜索", resourceId="im.yixin:id/add_friend_by_search_submit" ).click()
                z.sleep(3)
                if d(text="请检查你输入的帐号是否正确",resourceId="im.yixin:id/easy_dialog_message_text_view").exists:
                    d(text="确定",resourceId="im.yixin:id/easy_dialog_positive_btn").click()
                    if search.exists:
                        search.click()
                        for i in range(0,len(search.info["text"].encode("utf-8"))):
                            d.press.delete( )
                        continue

                if d(text="发消息",resourceId="im.yixin:id/yixin_profile_buddy_talk_btn").exists:
                    d.press.back( )
                    if search.exists:
                        search.click( )
                        for i in range( 0, len( search.info["text"].encode( "utf-8" ) ) ):
                            d.press.delete( )
                        continue

                if d(text="加为好友",resourceId="im.yixin:id/yixin_profile_add_btn").exists:
                    d( text="加为好友", resourceId="im.yixin:id/yixin_profile_add_btn" ).click()
                    z.sleep(4)
                    if d( text="发送验证申请等待对方通过", resourceId="im.yixin:id/add_friend_verify_content" ).exists:
                        d( text="发送验证申请等待对方通过", resourceId="im.yixin:id/add_friend_verify_content" ).click( )
                        cate_id1 = args["repo_material_cate_id"]
                        Material = self.repo.GetMaterial( cate_id1, 0, 1 )
                        if len( Material ) == 0:
                            z.toast( "%s仓库为空" % cate_id1 )
                            now = datetime.datetime.now( )
                            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                            z.setModuleLastRun( self.mid )
                            z.toast( '模块结束，保存的时间是%s' % nowtime )
                            return
                        message = Material[0]['content']  # 取出验证消息的内容
                        z.input( message )
                        if d( text="发送", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).exists:
                            d( text="发送", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).click( )
                            z.sleep( 3 )
                            if d( text="发送", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).exists:
                                z.toast( "可能操作频繁了" )
                                break
                            d.press.back( )
                    d.press.back()
                    if search.exists:
                        search.click( )
                        for i in range( 0, len( search.info["text"].encode( "utf-8" ) ) ):
                            d.press.delete( )
                        num = num + 1
                        continue


        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCYixinAddFriendsByNumber

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"repo_cate_id":"44",'number_count':'80',"random_name":"否","clear":"是","time_delay":"3","set_timeStart":"0","set_timeEnd":"0","startTime":"0","endTime":"8",
            "repo_material_cate_id":"255","add_count":"100"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
