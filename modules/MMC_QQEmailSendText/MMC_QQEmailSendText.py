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


class MMC_QQEmailSendText:
    def __init__(self):

        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )

    def action(self, d, z, args):
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
        z.toast( "准备执行MMC版QQ邮箱发消息" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：MMC版QQ邮箱发消息" )
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
        repo_mail_cateId = int(args['repo_mail_cateId'])
        repo_material_cateId= args["repo_material_cateId"]
        repo_material_cateId2 = args["repo_material_cateId2"]
        picture = args["picture"]
        size = args["size"]
        d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell","am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起来
        z.sleep( int( args["time_delay"] ) )
        z.heartbeat()
        Str = d.info  # 获取屏幕大小等信息
        height = Str["displayHeight"]
        width = Str["displayWidth"]
        z.heartbeat( )
        flag1 = False
        flag2 = False
        d.dump( compressed=False )
        if d( textContains="收件箱​",resourceId="com.tencent.androidqqmail:id/t0" ).exists:
            z.toast( "状态正常，继续执行" )
        else:
            if d( text="温馨提示​", className="android.widget.TextView" ).exists:
                d( text="确定", className="android.widget.Button" ).click( )
                z.sleep( 1 )
            elif d( text='密码错误，请重新输入' ).exists:
                z.toast("密码错误，状态不正常")
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            elif d(text="收件人：",resourceId="com.tencent.androidqqmail:id/nd").exists and d(text="写邮件",resourceId="com.tencent.androidqqmail:id/ac").exists:
                flag1 = True
            elif d(index=1,text="写邮件​",resourceId="com.tencent.androidqqmail:id/ac",className="android.widget.TextView").exists:
                while not d( text="离开", className="android.widget.Button" ).exists:
                    d.press.back( )
                    z.sleep( 1 )
                if d( text="离开", className="android.widget.Button" ).exists:
                    d( text="离开", className="android.widget.Button" ).click( )
                flag1 = True
            else:
                z.toast( "状态异常，跳过此模块" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
        selectContent = args["selectContent"]
        count = int( args["count"] )
        emailType = args["emailType"]
        numbers = self.repo.GetNumber( repo_mail_cateId, 120, count )
        if len( numbers ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_mail_cateId ).communicate( )
            z.sleep( 10 )
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
        if len( Material ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_material_cateId ).communicate( )
            z.sleep( 10 )
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        message = Material[0]['content']

        Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
        if len( Material2 ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_material_cateId2 ).communicate( )
            z.sleep( 10 )
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        message2 = Material2[0]['content']
        # if d(text="温馨提示​",className="android.widget.TextView").exists:
        #     d(text="确定",className="android.widget.Button").click()
        #     z.sleep(1)
        if d( description="写邮件和设置等功能" ).exists:
            d( description="写邮件和设置等功能" ).click( )
            z.sleep( 0.5 )
            if d( text="写邮件", resourceId="com.tencent.androidqqmail:id/w1" ).exists:
                d( text="写邮件", resourceId="com.tencent.androidqqmail:id/w1" ).click( )
                z.sleep( 0.5 )
                # d.click( 60 / 720 * width, 198 / 1280 * height )
                # z.sleep(0.5)
                flag2 = True

        if selectContent == "只发主题" or selectContent == "主题内容都发":
            d.click( 166 / 720 * width, 377 / 1280 * height )
            z.input( message2.encode( "utf-8" ) )
            z.sleep( 2 )
            z.heartbeat( )

        z.sleep( 1 )
        d.dump( compressed=False )
        if selectContent == "只发内容" or selectContent == "主题内容都发":
            if d(index=1,resourceId="com.tencent.androidqqmail:id/pq",className="android.widget.LinearLayout").child(
                    index=0,resourceId="com.tencent.androidqqmail:id/pr",className="android.widget.EditText").exists:
                d( index=1, resourceId="com.tencent.androidqqmail:id/pq",className="android.widget.LinearLayout" ).child(
                    index=0,resourceId="com.tencent.androidqqmail:id/pr",className="android.widget.EditText" ).click()
                z.input( message.encode( "utf-8" ) )
            # if not d( textContains="抄送/密送，发件人" ).exists:
            #     obj = d( index=0, className="android.webkit.WebView" ).child( index=0,
            #                                                                   className="android.view.View" ).child(
            #         index=0, className="android.view.View" )
            #     while not obj.exists:
            #         d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
            #         d.dump( compressed=False )
            #     obj.click( )
            #     z.input( message.encode( "utf-8" ) )
            # else:
            #     while not d( index=0, resourceId="com.tencent.androidqqmail:id/mp",
            #                  className="android.widget.EditText" ).exists:
            #         d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
            #         d.dump( compressed=False )
            #     if d( index=0, resourceId="com.tencent.androidqqmail:id/mp",
            #           className="android.widget.EditText" ).exists:
            #         text = d( index=0, resourceId="com.tencent.androidqqmail:id/mp",
            #                   className="android.widget.EditText" ).info["text"].encode( "utf-8" )
            #         z.sleep( 0.5 )
            #         if text == "" or text == None:
            #             d( index=0, resourceId="com.tencent.androidqqmail:id/mp",
            #                className="android.widget.EditText" ).click( )
            #             z.input( message.encode( "utf-8" ) )
            #             z.sleep( 0.5 )

        if flag2 or flag1:
            d.click( 81 / 720 * width, 189 / 1280 * height )
            for i in range( 0, count ):
                QQEmail = numbers[i]['number'].encode( "utf-8" )
                if emailType=="QQ邮箱":
                    z.input( QQEmail + "@qq.com " )
                elif emailType=="189邮箱":
                    z.input( QQEmail + "@189.cn " )
                else:
                    z.input( QQEmail + "@qq.com " )
                # if "@qq.com" not in QQEmail:
                #     z.input( QQEmail + "@qq.com " )
                # else:
                #     z.input( QQEmail + " " )
                print(QQEmail)

        if picture == "是":
            if d(index=0, resourceId="com.tencent.androidqqmail:id/p1", className="android.widget.RelativeLayout" ).child(index=0,resourceId="com.tencent.androidqqmail:id/p3",className="android.widget.Button").exists:
                d( index=0, resourceId="com.tencent.androidqqmail:id/p1",
                   className="android.widget.RelativeLayout" ).child( index=0,
                                                                      resourceId="com.tencent.androidqqmail:id/p3",
                                                                      className="android.widget.Button" ).click( )
                z.sleep( 0.5 )
                if d( resourceId="com.tencent.androidqqmail:id/gg", description="从相册选择文件" ).exists:
                    d( resourceId="com.tencent.androidqqmail:id/gg", description="从相册选择文件" ).click( )
                    z.sleep( 5 )
                    obj = d( index=2, resourceId="com.tencent.androidqqmail:id/h5",
                             className="android.widget.GridView" ).child(
                        index=1, className="android.widget.RelativeLayout" ).child(
                        index=0, resourceId="com.tencent.androidqqmail:id/v7", className="android.widget.CheckBox" )
                    if obj.exists:
                        obj.click( )
                        z.sleep( 0.5 )
                        if d( textContains="添加到邮件", resourceId="com.tencent.androidqqmail:id/hd" ).exists:
                            d( textContains="添加到邮件", resourceId="com.tencent.androidqqmail:id/hd" ).click( )
                            z.sleep( 2 )
                            if d( index=1, resourceId="com.tencent.androidqqmail:id/gk",
                                  className="android.widget.HorizontalScrollView" ).child( index=0,
                                                                                           resourceId="com.tencent.androidqqmail:id/gl",
                                                                                           className="android.widget.LinearLayout" ).exists:
                                d( index=1, resourceId="com.tencent.androidqqmail:id/gk",
                                   className="android.widget.HorizontalScrollView" ).child( index=0,
                                                                                            resourceId="com.tencent.androidqqmail:id/gl",
                                                                                            className="android.widget.LinearLayout" ).click( )
                                z.sleep( 0.5 )
                                z.heartbeat( )
                                if d( text="添加到正文", resourceId="com.tencent.androidqqmail:id/lj" ).exists:
                                    d( text="添加到正文", resourceId="com.tencent.androidqqmail:id/lj" ).click( )
                                    z.sleep( 0.5 )

                    else:
                        z.toast( "没有图片,停止模块" )
                        now = datetime.datetime.now( )
                        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                        z.setModuleLastRun( self.mid )
                        z.toast( '模块结束，保存的时间是%s' % nowtime )
                        return
        d.dump( compressed=False )
        if d( index=3, text="发送​", resourceId="com.tencent.androidqqmail:id/a_",className="android.widget.Button" ).exists:
            d( index=3, text="发送​", resourceId="com.tencent.androidqqmail:id/a_",className="android.widget.Button" ).click( )
            z.sleep(2)
            if d(textContains=size,resourceId="com.tencent.androidqqmail:id/lj",className="android.widget.TextView").exists:
                d( textContains=size, resourceId="com.tencent.androidqqmail:id/lj", className="android.widget.TextView" ).click()
        else:
            pass
        if d( index=3, text="发送​", resourceId="com.tencent.androidqqmail:id/a_",className="android.widget.Button" ).exists:
            z.toast("发送不了")

            while not d( text="离开",className="android.widget.Button" ).exists:
                d.press.back( )
                z.sleep(1)
            if d( text="离开", className="android.widget.Button" ).exists:
                d( text="离开", className="android.widget.Button" ).click()
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        if d(index=2,className="android.widget.Button").exists:
            d( index=2, className="android.widget.Button" ).click()
        if d(text="取消",className="android.widget.Button").exists or d(text="取消",className="android.widget.Button").exists:
            d( text="取消", className="android.widget.Button" ).click()


        z.toast("模块完成")
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束,保存的时间是%s' % nowtime )
        return


def getPluginClass():
    return MMC_QQEmailSendText

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("cda0ae8d")
    z = ZDevice("cda0ae8d")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"set_timeStart":"0","set_timeEnd":"0","startTime":"0","endTime":"8","repo_mail_cateId": "119", "repo_material_cateId": "39",
            "time_delay": "5","count":"3","picture":"是","size":"小","repo_material_cateId2":"255","selectContent":"主题内容都发","emailType":"189邮箱"};

    o.action(d, z, args)
