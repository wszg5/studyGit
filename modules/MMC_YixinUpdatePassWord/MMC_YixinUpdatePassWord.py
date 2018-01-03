# coding:utf-8
from __future__ import division
import base64
import logging
import re
import string

from uiautomator import Device
from Repo import *
import os, time, datetime, random
import json

from zcache import cache
from zservice import ZDevice


class MMCYixinUpdatePassWord:
    def __init__(self):
        self.repo = Repo()

    def GetPassword(self, numOfNum=4, numOfLetter=4):
        # 选中numOfNum个数字
        slcNum = [random.choice( string.digits ) for i in range( numOfNum )]
        # 选中numOfLetter个字母
        slcLetter = [random.choice( string.lowercase ) for i in range( numOfLetter )]
        slcChar = slcLetter + slcNum
        genPwd = ''.join( [i for i in slcChar] )
        return genPwd



    def action(self, d, z,args):
        z.toast( "准备执行MMS版易信修改密码" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：易信修改密码" )
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
        if d( text="我", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            z.toast( "登录状态正常" )
            d( text="我", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
        else:
            return
        if d(text="立即体验",resourceId="im.yixin:id/new_presented_resources_experience_btn").exists:
            d( text="立即体验", resourceId="im.yixin:id/new_presented_resources_experience_btn" ).click()
            z.sleep(1)

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        z.heartbeat()

        if d( text="设置").exists:
            d( text="设置").click( )
            z.sleep( 1 )
        else:
            d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
            if d( text="设置").exists:
                d( text="设置").click( )
                z.sleep( 1 )
            else:
                z.toast( "找不到设置" )
                return
        if d( text="帐号设置", resourceId="im.yixin:id/title_label" ).exists:
            d( text="帐号设置", resourceId="im.yixin:id/title_label" ).click( )

        obj = d( index=1, resourceId="im.yixin:id/align_right_layout" ).child( resourceId="im.yixin:id/detail_label",
                                                                               className="android.widget.TextView" )
        phone = ""
        if obj.exists:
            phone = obj.info["text"].encode( "utf-8" )
            z.sleep( 1 )
            z.toast( "获取到的手机号码为" + phone )

        account_card_id = args["account_card_id"]
        accounts = self.repo.GetDesignationAccount(phone,account_card_id)
        if len(accounts)==0:
            z.toast("帐号为%s不在仓库号为%s中,请重新选择帐号库"%(phone,account_card_id))
            return
        pw = accounts[0]["password"]
        newPassword = self.GetPassword()
        z.heartbeat()
        if d(text="修改密码",resourceId="im.yixin:id/title_label",className="android.widget.TextView").exists:
            d( text="修改密码", resourceId="im.yixin:id/title_label", className="android.widget.TextView" ).click()

            z.input(pw)
            if d(index=1,resourceId="im.yixin:id/new_password_edittext").exists:
                d( index=1, resourceId="im.yixin:id/new_password_edittext" ).click()
                z.input(newPassword)
            if d(text="确定",resourceId="im.yixin:id/action_bar_right_clickable_textview").exists:
                d( text="确定", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).click()

            self.repo.RegisterAccount(phone,newPassword,'',account_card_id,"normal")






        z.toast( "模块完成" )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCYixinUpdatePassWord

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"time_delay":"3",
            "repo_material_cate_id":"139","gender":"男","repo_material_cate_id2":"139","repo_material_cate_id3":"139","account_card_id":"281"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
