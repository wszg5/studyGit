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


class MMCYixinAutoReplyOld:
    def __init__(self):
        self.repo = Repo()

    def action(self, d, z,args):
        sendTime = args["sendTime"]
        sendTime = sendTime.split( "-" )
        try:
            sendTimeStart = int( sendTime[0] )
            sendTimeEnd = int( sendTime[1] )
        except:
            z.toast( "发送时间间隔的参数格式有误" )
            return
        z.toast( "准备执行易信监控回复旧版本" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：易信监控回复(旧)" )
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
        d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        if d(textContains="停止运行").exists:
            if d(text="确定").exists:
                d( text="确定" ).click()
                d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
                z.sleep(5)
        z.heartbeat( )
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
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        add_count = int(args["add_count"])
        msgcount = int(args["msgcount"])
        repo_material_cate_id = args["repo_material_cate_id"]
        i = 0
        num = 0
        index = 0
        while i <add_count:
            obj = d(index=index,className="android.widget.LinearLayout").child(index=0,className="android.widget.RelativeLayout")
            if not obj.exists:
                z.heartbeat()
                if d( index=index, className="android.widget.LinearLayout" ).child( index=1,
                                                                                    className="android.widget.RelativeLayout" ).exists:
                    obj = d(index=index,className="android.widget.LinearLayout").child(index=1,className="android.widget.RelativeLayout")
                else:
                    index = index + 1

                    if d( index=index, className="android.widget.LinearLayout" ).child( index=0,
                                                                                        className="android.widget.RelativeLayout" ).exists:
                        continue
                    else:
                        if not d( index=index, className="android.widget.LinearLayout" ).child( index=1,className="android.widget.RelativeLayout" ).exists:

                            index = 0
                            i = i + 1
                            if i>=add_count:
                                z.toast( "这一页到底了,监控的轮数到设定的值了" )
                                break
                            z.toast( "这一页到底了,进行下一轮重新监控" )
                        continue
            z.heartbeat()
            objText = obj.child(index=0,resourceId="im.yixin:id/portrait_panel").child(
                index=1,className="android.widget.TextView",resourceId="im.yixin:id/unread_number_tip")
            objClick = obj.child(index=0,resourceId="im.yixin:id/portrait_panel").child( index=0,
                                                                       resourceId="im.yixin:id/imgHead" )
            # objYixn = obj.child(index=1,text="易信团队",resourceId="im.yixin:id/lblNickname",className="android.widget.TextView")
            # objWY = obj.child( index=1, text="网易新闻", resourceId="im.yixin:id/lblNickname",
            #                      className="android.widget.TextView" )
            objname = obj.child( index=1, resourceId="im.yixin:id/lblNickname",
                                 className="android.widget.TextView" )
            if objname.exists:
                name = objname.info["text"].encode("utf-8")
                if objText.exists and name!="易信团队" and name!="易信资讯" and name!="网易新闻" and name!="公众号":
                    z.toast( "监控对象为" + name + ",对方发来了消息")
                else:
                    z.toast("监控对象为"+name)
            z.heartbeat()
            if num ==10:
                z.toast( "连续等待了100秒,还没消息,跳出模块" )
                return
            if d( textContains="找朋友聊聊吧", resourceId="im.yixin:id/message_list_empty_hint").exists:
                z.toast( "没有消息,等待10秒" )
                z.sleep(10)
                num = num + 1
                continue
            num = 0
            z.heartbeat()
            if objText.exists and name != "易信团队" and name != "易信资讯" and name != "网易新闻" and name != "公众号":
                if objClick.exists :
                    objClick.click()
                    z.sleep(3)
                    if not d(text="群空间",resourceId="im.yixin:id/teamsns_entry").exists:
                        if d(index=1,resourceId="im.yixin:id/editTextMessage",className="android.widget.EditText").exists:
                            d( index=1, resourceId="im.yixin:id/editTextMessage", className="android.widget.EditText" ).click()
                            for j in range( 0, random.randint( 1, msgcount ) ):
                                Material = self.repo.GetMaterial( repo_material_cate_id, 0, 1 )
                                if len( Material ) == 0:
                                    d.server.adb.cmd( "shell",
                                                      "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % repo_material_cate_id ).communicate( )
                                    z.sleep( 10 )
                                    return
                                message = Material[0]['content']  # 取出发送消息的内容
                                z.input( message )
                                z.sleep( 1 )
                                if d(text="发送",resourceId="im.yixin:id/buttonSendMessage").exists:
                                    d( text="发送", resourceId="im.yixin:id/buttonSendMessage" ).click()
                                    z.sleep( random.randint( sendTimeStart, sendTimeEnd ) )
                    while not d( text="消息", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
                        d.press.back()
                        z.sleep(2)
            index = index + 1
            # z.heartbeat()
            # if objClick.exists:
            #     objClick.long_click()
            #     z.sleep(0.5)
            #     if d(text="删除该聊天",resourceId="im.yixin:id/custom_dialog_text_view").exists:
            #         d( text="删除该聊天", resourceId="im.yixin:id/custom_dialog_text_view" ).click()

        z.toast( "模块完成" )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCYixinAutoReplyOld

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("INNZL7YDLFPBNFN7")
    z = ZDevice("INNZL7YDLFPBNFN7")

    args = {"time_delay":"3",
            "repo_material_cate_id":"255","add_count":"3","msgcount":"3","sendTime":"2-4"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
