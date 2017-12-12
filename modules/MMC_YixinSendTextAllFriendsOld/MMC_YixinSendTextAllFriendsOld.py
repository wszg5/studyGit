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


class MMCYixinSendTextAllFriendsOld:
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
        sendTime = args["sendTime"]
        sendTime = sendTime.split( "-" )
        try:
            sendTimeStart = int( sendTime[0] )
            sendTimeEnd = int( sendTime[1] )
        except:
            z.toast( "发送时间间隔的参数格式有误" )
            return
        z.toast( "准备执行MMS版易信加群发消息" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：易信群发消息" )
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

        if d( text="通讯录", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            d( text="通讯录", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
            if d( text="立即体验", resourceId="im.yixin:id/new_presented_resources_experience_btn" ).exists:
                d( text="立即体验", resourceId="im.yixin:id/new_presented_resources_experience_btn" ).click( )
                z.sleep( 1 )
            z.sleep(2)
            if not d( text="添加好友", resourceId="im.yixin:id/lblfuncname" ).exists:
                if d( text="通讯录", resourceId="im.yixin:id/tab_title_label",
                      className="android.widget.TextView" ).exists:
                    d( text="通讯录", resourceId="im.yixin:id/tab_title_label",
                       className="android.widget.TextView" ).click( )

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        add_count = int(args["add_count"])
        i = 4
        num = 0
        nameList = []
        # x = 0
        # y = 0
        while num < add_count:

            obj = d( index=0, resourceId="im.yixin:id/lvContacts", className="android.widget.ListView" ).child( index=i,
                                                                                                                className="android.widget.RelativeLayout" )


            objName = d(index=i,className="android.widget.RelativeLayout").child(index=1,className="android.widget.LinearLayout",resourceId="im.yixin:id/nameLayout").child(
                resourceId="im.yixin:id/lblNickname",className="android.widget.TextView")

            objOver =  obj.child(className="android.widget.TextView",resourceId="im.yixin:id/contactCountText",textContains="共有好友")
            z.heartbeat()
            # if x>2:
            #     if len(nameList)==0:
            #         z.toast("没有好友,停止模块")
            #         return
            # if y >2:
            #     if len(nameList)==0:
            #         z.toast("没有好友,停止模块")
            #         return
            #     else:
            #         z.toast("共有%d个好友"%(len(nameList)))
            #         break
            # x = x + 1
            if obj.exists:
                if objName.exists:
                    name = objName.info["text"].encode( "utf-8" )
                    if not name in nameList and name !="易信团队":
                        nameList.append(name)
                        num = num + 1
                    # elif not name in nameList and name =="易信团队":
                    #     # y = y + 1

                i = i + 1
                continue
            else:
                if d(className="android.widget.TextView",resourceId="im.yixin:id/contactCountText",textContains="共有好友").exists:
                    z.toast( "到底了" )
                    break
                if d(textContains="多些好友互动易信才会更好玩喔",resourceId="im.yixin:id/contactCountText",className="android.widget.TextView").exists:
                    z.toast( "到底了" )
                    break
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                i = 0
                continue
        # if d(className="android.widget.TextView",resourceId="im.yixin:id/action_search").exists:
        #     d( className="android.widget.TextView", resourceId="im.yixin:id/action_search" ).click()
        #     if d(description="搜索查询",resourceId="im.yixin:id/search_src_text").exists:
        #         d( description="搜索查询", resourceId="im.yixin:id/search_src_text" ).click()
        if len( nameList ) == 0:
            z.toast("没有好友,停止模块")
            return
        megcount = int(args["megcount"])
        repo_material_cate_id = args["repo_material_cate_id"]
        random.shuffle( nameList )
        for item in nameList:
            z.heartbeat()
            if d(description="清除查询",resourceId="im.yixin:id/search_close_btn").exists:
                d( description="清除查询", resourceId="im.yixin:id/search_close_btn" ).click()
                z.sleep(1)
            else:
                if d( className="android.widget.TextView", resourceId="im.yixin:id/action_search" ).exists:
                    d( className="android.widget.TextView", resourceId="im.yixin:id/action_search" ).click( )
                    if d( description="搜索查询", resourceId="im.yixin:id/search_src_text" ).exists:
                        d( description="搜索查询", resourceId="im.yixin:id/search_src_text" ).click( )
            z.input(item)
            z.sleep(1)
            if d(text=item,resourceId="im.yixin:id/lblNickname").exists:
                d( text=item, resourceId="im.yixin:id/lblNickname" ).click()
                z.sleep(4)
                z.heartbeat()
            else:
                z.toast("可能他不是你的好友了")
                continue
            z.heartbeat()
            if d( index=1, resourceId="im.yixin:id/editTextMessage", className="android.widget.EditText" ).exists:
                d( index=1, resourceId="im.yixin:id/editTextMessage", className="android.widget.EditText" ).click( )
                for j in range( 0, random.randint( 1, megcount ) ):
                    Material = self.repo.GetMaterial( repo_material_cate_id, 0, 1 )
                    if len( Material ) == 0:
                        d.server.adb.cmd( "shell",
                                          "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % repo_material_cate_id ).communicate( )
                        z.sleep( 10 )
                        return
                    message = Material[0]['content']  # 取出发送消息的内容
                    z.input( message )
                    z.sleep( 1 )
                    if d( text="发送", resourceId="im.yixin:id/buttonSendMessage" ).exists:
                        d( text="发送", resourceId="im.yixin:id/buttonSendMessage" ).click( )
                        z.sleep( random.randint( sendTimeStart, sendTimeEnd ) )
                a = 0
                z.heartbeat()
                while not d(description="清除查询",resourceId="im.yixin:id/search_close_btn").exists and not d(
                        text="消息", resourceId="im.yixin:id/tab_title_label",
                        className="android.widget.TextView" ).exists:
                    d.press.back( )
                    z.sleep( 2 )
                    if a == 4:
                        z.toast( "可能干猛了" )
                        break
                    else:
                        a = a + 1
        z.toast( "模块完成" )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCYixinSendTextAllFriendsOld

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
            "repo_material_cate_id":"255","add_count":"20","sendTime":"2-4","megcount":"5"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
