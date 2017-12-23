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


class MMCYixinChickMsgCountOld:
    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )

    def action(self, d, z,args):
        z.toast( "准备执行MMS版易信检查短信数量入库" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：易信检查短信数量入库" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        d.server.adb.cmd( "shell", "am force-stop im.yixin" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        z.heartbeat( )
        if d(textContains="停止运行").exists:
            if d(text="确定").exists:
                d( text="确定" ).click()
                d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
                z.sleep(5)
        if d( text="消息", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            z.toast( "登录状态正常" )
            # d( text="消息", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
        else:
            if d( text="立即更新", resourceId="im.yixin:id/easy_dialog_positive_btn" ).exists:
                d( text="下次再说", resourceId="im.yixin:id/easy_dialog_negative_btn" ).click( )
                z.toast( "登录状态正常" )
            else:
                z.toast( "登录状态异常" )
                return
        if d( text="立即更新", resourceId="im.yixin:id/easy_dialog_positive_btn" ).exists:
            d( text="下次再说", resourceId="im.yixin:id/easy_dialog_negative_btn" ).click( )

        if d( text="我", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            d( text="我", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
            z.sleep(2)
        if d(text="立即体验").exists:
            d( text="立即体验" ).click()
            z.sleep(1)

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        msg = d( resourceId="im.yixin:id/my_free_services_root", className="android.widget.LinearLayout" ).child(
            index=2, className="android.widget.LinearLayout" ).child(
            index=1, resourceId="im.yixin:id/free_service_item_free_message" ).child( index=0,
                                                                                      resourceId="im.yixin:id/root" ).child(
            index=0, resourceId="im.yixin:id/content_layout" ).child(
            index=1, resourceId="im.yixin:id/quotaTV" )

        msgNum = 0
        if msg.exists:
            try:
                msgNum = msg.info["text"].encode( "utf-8" )
                msgNum = int( msgNum )
                if msgNum == 0:
                    z.toast( "可能没有短信可发,没必要入库" )
                    return
            except:
                z.toast( "可能没有短信可发,没必要入库" )
                return

        z.toast( "有短信可发消息" )

        if d(text="设置",resourceId="im.yixin:id/title_label").exists:
            d( text="设置", resourceId="im.yixin:id/title_label" ).click()
            z.sleep(1)
        else:
            d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
            if d( text="设置", resourceId="im.yixin:id/title_label" ).exists:
                d( text="设置", resourceId="im.yixin:id/title_label" ).click( )
                z.sleep( 1 )
            else:
                z.toast("找不到设置")
                return
        if d(text="帐号设置",resourceId="im.yixin:id/title_label").exists:
            d( text="帐号设置", resourceId="im.yixin:id/title_label" ).click()

        obj = d(index=2,className="android.widget.RelativeLayout").child(resourceId="im.yixin:id/detail_label",className="android.widget.TextView")
        phone = ""
        if obj.exists:
            phone = obj.info["text"].encode("utf-8")
            z.sleep(1)
            z.toast("获取到的手机号码为"+phone)
        while not d( text="我", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            d.press.back()
            z.sleep(1)



        repo_info_id = args["repo_info_id"]
        para = {"phoneNumber": phone, 'x_01': "", 'x_02': "", 'x_03': msgNum, }
        Repo( ).PostInformation( repo_info_id, para )

        z.toast( "模块完成" )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return MMCYixinChickMsgCountOld

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("INNZL7YDLFPBNFN7")
    z = ZDevice("INNZL7YDLFPBNFN7")

    args = {"time_delay":"3","repo_info_id":"282"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
