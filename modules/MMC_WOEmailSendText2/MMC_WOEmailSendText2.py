# coding:utf-8
from __future__ import division

import os
import random

from smsCode import smsCode
import string
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice


class MMC_WOEmailSendText2:
    def __init__(self):
        self.repo = Repo()

    def action(self, d, z, args):
        startTime = args["startTime"]
        endTime = args["endTime"]
        try:
            if not self.repo.timeCompare( startTime, endTime ):
                z.toast( "该时间不在允许运行时间范围内" )
                return
            else:
                z.toast( "该时间允许运行" )
        except:
            z.toast( "输入的时间格式错误,请检查后再试" )
            return

        z.toast( "准备执行wo邮箱发消息" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：WO邮箱发消息" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        repo_mail_cateId = int( args['repo_mail_cateId'] )
        repo_material_cateId = args["repo_material_cateId"]
        repo_material_cateId2 = args["repo_material_cateId2"]
        picture = args["picture"]
        count = int( args["count"] )
        flag = True
        d.server.adb.cmd( "shell", "am force-stop com.asiainfo.android" ).communicate( )  # 强制停止
        for i in range( 0, count ):
            d.server.adb.cmd( "shell",
                              "am start -n com.asiainfo.android/com.asiainfo.mail.ui.sendmail.SendMailActivity" ).communicate( )  # 拉起来
            if flag:
                z.sleep( int( args["time_delay"] ) )
                flag = False
            else:
                z.sleep( 2 )
            z.heartbeat( )

            if d( textContains="写邮件", resourceId="com.asiainfo.android:id/tv_title" ).exists and d( text="收件人：",
                                                                                                    className="android.widget.TextView" ):
                z.toast( "状态正常，继续执行" )
            else:
                z.toast( "状态异常，跳过此模块" )
                return
            selectContent = args["selectContent"]
            emailType = args["emailType"]
            numbers = self.repo.GetNumber( repo_mail_cateId, 60, 1 )
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_mail_cateId ).communicate( )
                z.sleep( 10 )
                return
            Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_material_cateId ).communicate( )
                z.sleep( 10 )
                return
            message = Material[0]['content']

            Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
            if len( Material2 ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_material_cateId2 ).communicate( )
                z.sleep( 10 )
                return
            message2 = Material2[0]['content']

            if d( index=1, className="android.widget.EditText" ).exists:
                d( index=1, className="android.widget.EditText" ).click( )
                number = numbers[0]['number']
                if "@" not in number:
                    z.toast( "%s仓库里的号码没有邮件类型,使用默认类型" % repo_mail_cateId )
                    if emailType == "QQ邮箱":
                        z.input( number + "@qq.com " )
                    elif emailType == "189邮箱":
                        z.input( number + "@189.cn " )
                    elif emailType == "139邮箱":
                        z.input( number + "@139.com " )
                    elif emailType == "163邮箱":
                        z.input( number + "@163.com " )
                    elif emailType == "wo邮箱":
                        z.input( number + "@wo.cn " )
                    else:
                        z.input( number + "@wo.cn " )

            if selectContent == "只发主题" or selectContent == "主题内容都发":
                if d( index=1, resourceId="com.asiainfo.android:id/subject" ).exists:
                    d( index=1, resourceId="com.asiainfo.android:id/subject" ).click( )
                z.input( message2.encode( "utf-8" ) )
                z.sleep( 0.5 )
                z.heartbeat( )

            z.sleep( 1 )
            d.dump( compressed=False )
            if selectContent == "只发内容" or selectContent == "主题内容都发":
                if d( index=1, resourceId="com.asiainfo.android:id/message_content", text="请输入正文" ).exists:
                    d( index=1, resourceId="com.asiainfo.android:id/message_content", text="请输入正文" ).click( )
                    z.input( message.encode( "utf-8" ) )

            if picture == "是":
                if d( index=0, resourceId="com.asiainfo.android:id/send_mail_attachment",
                      className="android.widget.ImageView" ).exists:
                    d( index=0, resourceId="com.asiainfo.android:id/send_mail_attachment",
                       className="android.widget.ImageView" ).click( )
                    z.sleep( 0.5 )
                    d.click( 356 / 720 * width, 931 / 1280 * height )
                    z.sleep( 5 )
                    obj = d( index=1, resourceId="com.asiainfo.android:id/gridview",
                             className="android.widget.GridView" ).child(
                        index=0, resourceId="com.asiainfo.android:id/framelyt" ).child(
                        index=0, resourceId="com.asiainfo.android:id/image", className="android.widget.ImageView" )
                    if obj.exists:
                        obj.click( )
                        z.sleep( 0.5 )
                        if d( textContains="确定", resourceId="com.asiainfo.android:id/preview_text" ).exists:
                            d( textContains="确定", resourceId="com.asiainfo.android:id/preview_text" ).click( )
                            z.sleep( 2 )
                        d.press.back( )
                    else:
                        z.toast( "没有图片,停止模块" )
                        return
            if d( index=2, resourceId="com.asiainfo.android:id/iv_right_button",
                  className="android.widget.ImageView" ).exists:
                d( index=2, resourceId="com.asiainfo.android:id/iv_right_button",
                   className="android.widget.ImageView" ).click( )
                z.sleep( 1 )

            if d(text="继续发送",resourceId="android:id/button1",className="android.widget.Button").exists:
                d( text="继续发送", resourceId="android:id/button1", className="android.widget.Button" ).click()
                z.sleep(1)

            if d( index=2, resourceId="com.asiainfo.android:id/iv_right_button",
                  className="android.widget.ImageView" ).exists:
                z.toast( "发送不了" )
        z.toast( "模块完成" )
        return


def getPluginClass():
    return MMC_WOEmailSendText2

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_mail_cateId": "119", "repo_material_cateId": "39",
            "time_delay": "5","count":"3","picture":"是","repo_material_cateId2":"255","selectContent":"只发内容","emailType":"QQ邮箱","startTime":"23","endTime":"15"}

    o.action(d, z, args)
