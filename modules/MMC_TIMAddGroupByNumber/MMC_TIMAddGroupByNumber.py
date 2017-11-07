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


class MMCTIMAddAddressByNumber:
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

        add_count = int(args['add_count'])  # 要添加多少人
        repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号

        z.sleep(1)
        z.heartbeat( )
        d(resourceId='com.tencent.tim:id/name',description='快捷入口').click()
        z.heartbeat( )
        z.sleep( 1 )
        if d(text='加好友',resourceId='com.tencent.tim:id/name').exists:
            d(text='加好友',resourceId='com.tencent.tim:id/name').click()
            z.heartbeat( )
        else:
            z.heartbeat( )
            d(resourceId='com.tencent.tim:id/name', description='快捷入口').click()
            z.heartbeat( )
            d(text='加好友',resourceId='com.tencent.tim:id/name').click()
        z.sleep(1)
        z.heartbeat( )

        count = 0
        num = 0
        while count<add_count:
            numbers = self.repo.GetNumber( repo_number_cate_id, 120, add_count )  # 取出add_count条两小时内没有用过的号码
            if len( numbers ) == 0:  #
                d.server.adb.cmd( "shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到号码\"" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            list = numbers  # 将取出的号码保存到一个新的集合
            # num = list[0]['number']
            QQnumber = numbers[0]['number']
            if d( text='QQ号/手机号/群', resourceId='com.tencent.tim:id/name' ).exists:
                d( text='QQ号/手机号/群', resourceId='com.tencent.tim:id/name' ).click( )
                # d(text='QQ号/手机号/群', resourceId='com.tencent.tim:id/et_search_keyword').click()
            z.heartbeat( )
            # d(text='QQ号/手机号/群', resourceId='com.tencent.tim:id/et_search_keyword').set_text(QQnumber)  # 第一次添加的帐号 list[0]
            z.input( QQnumber )
            z.heartbeat( )
            # d( text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search' ).click( )
            if d( text="找群:", className="android.widget.TextView" ).exists:
                d( text="找群:", className="android.widget.TextView" ).click( )
                z.sleep( 8 )
            numbers = list[i]
            repo_material_cate_id = args["repo_material_cate_id"]  # 得到验证语的仓库号
            Material = self.repo.GetMaterial( repo_material_cate_id, 0, 1 )
            wait = 1  # 判断素材仓库里是否由素材
            material = ""
            while wait == 1:
                try:
                    material = Material[0]['content']  # 取出验证消息的内容
                    wait = 0
                except Exception:
                    d.server.adb.cmd( "shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到验证消息\"" )
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return                        # 得到验证语
            # numbers = self.repo.GetNumber( repo_number_cate_id, 120, add_count )    # 取出两小时内没有用过的号码
            # list = numbers
            # QQnumber = numbers[0]['number']
            z.heartbeat( )
            time.sleep(1)
            if d(text='没有找到相关结果',className='android.widget.TextView').exists:                            #没有这个人的情况
                z.heartbeat( )
                d(resourceId='com.tencent.tim:id/ib_clear_text',description='清空').click()
                continue
            time.sleep(2)

            if d(text='申请加群').exists:
                d( text='申请加群' ).click()
                z.sleep(8)
            else:
                if d(text="发消息",className="android.widget.Button").exists:
                    z.sleep(1)
                    d.press.back()
                    d( resourceId='com.tencent.tim:id/ib_clear_text', description='清空' ).click( )
                    continue
                else:
                    if d( index=0, resourceId='com.tencent.tim:id/name',
                          className="android.widget.TextView" ).exists:  # 在同一查条件有多个人
                        z.heartbeat( )
                        z.sleep( 2 )
                        d( index=0, resourceId='com.tencent.tim:id/name', className="android.widget.TextView" ).click()
                        z.sleep( 2 )
                        if d( text='申请加群' ).exists:
                            d( text='申请加群' ).click( )
                            z.sleep( 8 )
                    else:
                        if d(text="返回").exists:
                            d( text="返回" ).click()
                            if d(resourceId='com.tencent.tim:id/ib_clear_text',description='清空').exists:
                                d( resourceId='com.tencent.tim:id/ib_clear_text', description='清空' ).click( )
                                continue
                # i = i +1
                continue
            z.sleep(1)
            if d(text='申请加群').exists:
                # i = i +1
                continue
            # if d(text="输入答案",className="android.widget.EditText").exists:
            #     d( text="输入答案", className="android.widget.EditText" ).click()
            switch = args["switch"]
            if switch=="是":
                obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
                obj = obj['text']
                lenth = len(obj)
                m = 0
                while m < lenth:
                    d.press.delete()
                    m = m + 1
                z.input(material)
            z.sleep(2)
            if d(text='发送').exists:
                d(text='发送').click()
                z.sleep(6)
            if d(text='发送').exists:
                if d( text="输入答案", className="android.widget.EditText" ).exists:
                    d.press.back()
                    z.sleep(0.5)
                    d.press.back()
                    if d( resourceId='com.tencent.tim:id/ib_clear_text', description='清空' ).exists:
                        d( resourceId='com.tencent.tim:id/ib_clear_text', description='清空' ).click( )
                        z.sleep( 0.5 )
                    continue
                else:
                    z.toast("添加失败")
                    break
            if d(text="发送成功",className="com.tencent.tim:id/ivTitleName").exists:
                d.press.back()
                z.sleep(0.5)
                d( resourceId='com.tencent.tim:id/ib_clear_text', description='清空' ).click( )
            print(QQnumber+"发送成功")
            if num==add_count:
                z.toast("模块完成")
                return
            num = num +1
            # i = i +1
            z.sleep(2)
            z.heartbeat()
            if d( text='申请加群' ).exists:
                # i = i +1
                d.press.back()
                if d(resourceId='com.tencent.tim:id/ib_clear_text',description='清空').exists:
                    d( resourceId='com.tencent.tim:id/ib_clear_text', description='清空' ).click( )
                    z.sleep(0.5)

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCTIMAddAddressByNumber

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
            "repo_number_cate_id":"229","repo_material_cate_id":"255","add_count":"5","switch":"否"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
