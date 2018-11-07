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


class MMCQQCardParise2:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum


    def action(self, d, z,args):
        z.toast( "准备执行QQ名片名片点赞模块" )
        z.sleep( 1 )
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
            return
        count = int( args['count'] )  # 要添加多少人
        i = 0
        switch = args["switch"]
        # time_limit1 = int( args["time_limit1"] )
        repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
        click_count = int( args["click_count"] )
        flag = True
        while i < count :  # 总人数
            numbers = self.repo.GetNumber( repo_number_cate_id, 0, 1 )

            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % repo_number_cate_id ).communicate( )
                z.sleep( 5 )
                return
            z.heartbeat( )
            QQnumber = numbers[0]['number']  # 即将点赞的QQ号
            print(QQnumber)
            z.sleep( 1 )

            z.cmd( "shell",
                   'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"' % QQnumber )  # qq名片页面
            z.sleep( 2 )
            if d( text='QQ', resourceId="android:id/text1" ).exists:
                z.heartbeat( )
                d( text='QQ', resourceId="android:id/text1" ).click( )
                z.sleep( 2 )
                z.heartbeat( )
                while d( text='仅此一次' ).exists:
                    z.heartbeat( )
                    d( text='仅此一次' ).click( )

            z.sleep( random.randint( 6, 8 ) )
            objtext = ''
            objtext1 = ""
            obj = d( descriptionContains="当前有" ).child( index=0,
                                                        className='android.widget.LinearLayout' ).child(
                index=1, className="android.widget.TextView" )
            if obj.exists:
                objtext1 = obj.info["text"].encode( "utf-8" )
                objtext = objtext1
            else:
                if switch =="跳过":
                    z.toast("这个获取不到点赞数,跳过")
                    continue
                obj = d( descriptionContains="当前有" )
                flag = False
            if click_count>=10:
                click_count = 10
            if obj.exists:
                # objtext = obj.info["text"].encode("utf-8")
                for j in range( 0, random.randint(1,5) ):
                    if d( descriptionContains="当前有" ).exists:
                        d( descriptionContains="当前有" ).click( )
                        z.sleep( 1 )
                        # d.dump( compressed=False )
                        if objtext != "":
                            objtext2 = d( descriptionContains="当前有" ).child( index=0,
                                                                             className='android.widget.LinearLayout' ).child(
                                index=1, className="android.widget.TextView" ).info["text"].encode( "utf-8" )
                            if objtext == objtext2:
                                z.toast( "今天无法继续赞了，停止模块" )
                                return
                            objtext = objtext2
                        else:
                            z.toast( "这个获取不到点赞数,跳过" )
                            continue
            else:
                z.toast( "对方拒绝赞" )
                continue

            if flag:
                z.cmd( "shell",'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"' % QQnumber )  # qq名片页面
                z.sleep( 3 )
                if d( text='QQ', resourceId="android:id/text1" ).exists:
                    z.heartbeat( )
                    d( text='QQ', resourceId="android:id/text1" ).click( )
                    z.sleep( 2 )
                    z.heartbeat( )
                    while d( text='仅此一次' ).exists:
                        z.heartbeat( )
                        d( text='仅此一次' ).click( )
                z.sleep( random.randint( 5, 7 ) )
                if objtext1 == "":
                    z.toast( "这个获取不到点赞数,跳过" )
                    continue
                obj = d( descriptionContains="当前有" ).child( index=0,className='android.widget.LinearLayout' ).child(
                    index=1, className="android.widget.TextView" )
                if obj.exists:
                    objtext3 = obj.info["text"].encode( "utf-8" )
                    if int(objtext3)>int(objtext1):
                        z.toast("可以点赞")
                        i = i + 1
                    else:
                        z.toast("点赞无用")
                        break
                else:
                    z.toast( "这个获取不到点赞数,跳过" )
                    continue

        return



def getPluginClass():
    return MMCQQCardParise2

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("cc0e9474")
    z = ZDevice("cc0e9474")

    args = {"time_delay":"3","repo_number_cate_id":"244","count":"5","click_count":"2","switch":"跳过"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
