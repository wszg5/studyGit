# coding:utf-8
from __future__ import division

import random
import re

from smsCode import smsCode
import string
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice


class QQEmailSendTextAll2:
    def __init__(self):

        self.repo = Repo()

    def input(self,random_code,z,text):
        if random_code=="乱码":
            z.cmd( "shell", "am broadcast -a ZY_INPUT_TEXT --es text \\\"%s\\\"" % text )
        else:
            z.input(text)

    def getTime(self, timeType):
        path = "/cgi-bin/cgi_svrtime"
        conn = httplib.HTTPConnection( "cgi.im.qq.com", None, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        data = response.read( ).replace( "\n", "" )
        # if response.status == 200:
        #   data = response.read()
        # else:
        #   print u"http://cgi.im.qq.com/cgi-bin/cgi_svrtime 失效了"
        #  return ""
        timea = datetime.datetime.strptime( data, '%Y-%m-%d %H:%M:%S' )
        if timeType == "EnTime":
            return timea.strftime( "%a, %b %d,  %Y %I:%M %p" )
        elif timeType == "CnTime":
            nt = timea
            w = ""
            weekday = nt.weekday( )
            if weekday == 0:
                w = "星期一"
            elif weekday == 1:
                w = "星期二"
            elif weekday == 2:
                w = "星期三"
            elif weekday == 3:
                w = "星期四"
            elif weekday == 4:
                w = "星期五"
            elif weekday == 5:
                w = "星期六"
            elif weekday == 6:
                w = "星期日"
            p = nt.strftime( "%p" )
            if p == "PM" or p == "pm":
                p = "下午"
            else:
                p = "上午"

            nowtime = nt.strftime( '%Y年%m月%d日%I:%M' )
            nowtime = nowtime.replace( "日", "日 (%s) %s" % (w, p) )
            return nowtime
        else:
            return timea.strftime( "%a, %b %d,  %Y %I:%M %p" )

    def send_mail(self, d, z, args, fj, repo_mail_cateId, repo_mail_cateId2, account, check, account_num):
        # repo_mail_cateId = args['repo_mail_cateId']
        repo_material_cateId = args['repo_material_cateId']
        selectContent = args["selectContent"]
        repo_material_cateId2 = args['repo_material_cateId2']
        Str = d.info  # 获取屏幕大小等信息
        height = int( Str["displayHeight"] )
        width = int( Str["displayWidth"] )
        size = args['size']
        random_code = args['random_code']
        z.heartbeat( )
        numberArr = []
        if repo_mail_cateId:
            count = 1
        else:
            count = 0
        if repo_mail_cateId2:
            if "@" in repo_mail_cateId2:
                numberArr.append(repo_mail_cateId2)
                count2 = 0
            else:
                count2 = 1
        else:
            count2 = 0

        if count > 0:
            numbers = self.repo.GetNumber( repo_mail_cateId, 120, count )
            if len( numbers ) == 0:
                if args["nuberLoop"] == "循环":
                    self.repo.UpdateNumberStauts( "", repo_mail_cateId, "normal" )
                    numbers = self.repo.GetNumber( repo_mail_cateId, 120, count )
                    if len( numbers ) == 0:
                        z.toast( "%s号仓库没有号码" % repo_mail_cateId )
                        return
                else:
                    d.server.adb.cmd( "shell",
                                      "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_mail_cateId ).communicate( )
                    z.sleep( 10 )
                    return
            QQEmail = numbers[0]['number'].encode( "utf-8" )
            if "@" not in QQEmail:
                QQEmail += "@qq.com"
            numberArr.append(QQEmail)

        if count2 > 0:
            numbers = self.repo.GetNumber( repo_mail_cateId2, 120, count2 )
            if len( numbers ) == 0:
                if args["nuberLoop"] == "循环":
                    self.repo.UpdateNumberStauts( "", repo_mail_cateId2, "normal" )
                    numbers = self.repo.GetNumber( repo_mail_cateId2, 120, count2 )
                    if len( numbers ) == 0:
                        z.toast( "%s号仓库没有号码" % repo_mail_cateId2 )
                        return
                else:
                    d.server.adb.cmd( "shell",
                                      "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_mail_cateId2 ).communicate( )
                    z.sleep( 10 )
                    return
            QQEmail = numbers[0]['number'].encode( "utf-8" )
            if "@" not in QQEmail:
                QQEmail += "@qq.com"
            numberArr.append(QQEmail)

        Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
        if len( Material ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_material_cateId ).communicate( )
            z.sleep( 10 )
            return
        message = Material[0]['content']

        Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
        if len( Material ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_material_cateId ).communicate( )
            z.sleep( 10 )
            return
        message2 = Material2[0]['content']
        z.heartbeat( )
        # if d(text="温馨提示​",className="android.widget.TextView").exists:
        #     d(text="确定",className="android.widget.Button").click()
        #     z.sleep(1)
        if d( description="写邮件和设置等功能" ).exists:
            d( description="写邮件和设置等功能" ).click( )
            z.sleep( 0.5 )
            if d( text="写邮件" ).exists:
                d( text="写邮件" ).click( )
                z.sleep( 0.5 )
                # d.click( 60 / 720 * width, 198 / 1280 * height )
                # z.sleep(0.5)
                flag2 = True
        else:
            d.swipe( width / 2, height * 1 / 5, width / 2, height * 4 / 5 )
            time.sleep( 3 )
            if d( text="写邮件" ).exists:
                d( text="写邮件" ).click( )
                z.sleep( 0.5 )
                # d.click( 60 / 720 * width, 198 / 1280 * height )
                # z.sleep(0.5)
                flag2 = True
        z.heartbeat( )
        if selectContent == "只发主题" or selectContent == "主题内容都发":
            d.click( 166 / 720 * width, 377 / 1280 * height )
            self.input(random_code,z, message2.encode( "utf-8" ) )
            z.sleep( 2 )
            z.heartbeat( )

        z.sleep( 1 )
        d.dump( compressed=False )
        if selectContent == "只发内容" or selectContent == "主题内容都发":
            if "@" not in account:
                account2 = account + "@qq.com"
            else:
                account2 = account
            message = message.replace( "+FromMail+", account2.encode( "utf-8" ) )
            email = numberArr[0]
            message = message.replace( "+ToMail+", email.encode( "utf-8" ) )
            message = message.replace( "+Subject+", message2.encode( "utf-8" ) )
            while True:
                try:
                    x = self.getTime( "CnTime" )
                    x = unicode( x.decode( "utf-8" ) )
                    message = message.replace( u"+CnTime+", x )
                    break
                except:
                    pass
            while True:
                try:
                    x2 = self.getTime( "EnTime" ).encode( "utf-8" )
                    x2 = unicode( x2.decode( "utf-8" ) )
                    message = message.replace( "+EnTime+", x2 )
                    break
                except:
                    pass
            z.heartbeat( )
            if not d( textContains="抄送/密送，发件人" ).exists:
                obj = d( index=0, className="android.webkit.WebView" ).child( index=0,
                                                                              className="android.view.View" ).child(
                    index=0, className="android.view.View" )
                while not obj.exists:
                    d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                    d.dump( compressed=False )
                obj.click( )
                self.input(random_code,z, message.encode( "utf-8" ) )
            else:
                while not d( index=0, className="android.widget.EditText" ).exists:
                    d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                    d.dump( compressed=False )
                if d( index=0, className="android.widget.EditText" ).exists:
                    text = d( index=0, className="android.widget.EditText" ).info["text"].encode( "utf-8" )
                    z.sleep( 0.5 )
                    if text == "" or text == None:
                        d( index=0, className="android.widget.EditText" ).click( )
                        self.input(random_code,z, message.encode( "utf-8" ) )
                        z.sleep( 0.5 )

        d.click( 81 / 720 * width, 189 / 1280 * height )
        for numberMail in numberArr:
            # self.input(z,height,QQEmail+" ")
            self.input(random_code,z, numberMail+" " )

        if fj:
            if d( index=0, resourceId="com.tencent.androidqqmail:id/p3", className="android.widget.Button" ).exists:
                d( resourceId="com.tencent.androidqqmail:id/p3", className="android.widget.Button" ).click( )
                z.sleep( 0.5 )
                if d( description="从相册选择文件" ).exists:
                    d( description="从相册选择文件" ).click( )
                    z.sleep( 5 )
                    obj = d( index=2, className="android.widget.GridView" ).child(
                        index=1, className="android.widget.RelativeLayout" ).child(
                        index=0, className="android.widget.CheckBox" )
                    if obj.exists:
                        obj.click( )
                        z.sleep( 0.5 )
                        if d( textContains="添加到邮件" ).exists:
                            d( textContains="添加到邮件" ).click( )
                            z.sleep( 2 )
                            addToText = args['addToText']
                            if addToText == "添加":
                                if d( index=1,
                                      className="android.widget.HorizontalScrollView" ).child( index=0,

                                                                                               className="android.widget.LinearLayout" ).exists:
                                    d( index=1,
                                       className="android.widget.HorizontalScrollView" ).child( index=0,
                                                                                                className="android.widget.LinearLayout" ).click( )
                                    z.sleep( 0.5 )
                                    z.heartbeat( )
                                    if d( text="添加到正文" ).exists:
                                        d( text="添加到正文" ).click( )
                                        z.sleep( 0.5 )

                    else:
                        z.toast( "没有图片,停止模块" )
                        return
        z.heartbeat( )
        d.dump( compressed=False )
        if d( text="发送​", className="android.widget.Button", resourceId="com.tencent.androidqqmail:id/a_" ).exists:
            d( text="发送​", className="android.widget.Button", resourceId="com.tencent.androidqqmail:id/a_" ).click( )
            z.sleep( 2 )
            if d( textContains=size, className="android.widget.TextView",
                  resourceId="com.tencent.androidqqmail:id/lj" ).exists:
                d( textContains=size, className="android.widget.TextView",
                   resourceId="com.tencent.androidqqmail:id/lj" ).click( )
            if d( text="确定" ).exists:
                d( text="确定" ).click( )
        else:
            pass
        if d( text="发送​", className="android.widget.Button", resourceId="com.tencent.androidqqmail:id/a_" ).exists:
            z.toast( "发送不了" )
            return
        time.sleep( 2 )
        if d( index=2, className="android.widget.Button" ).exists:
            d( index=2, className="android.widget.Button" ).click( )
        if d( text="取消", className="android.widget.Button" ).exists or d( text="取消",
                                                                          className="android.widget.Button" ).exists:
            d( text="取消", className="android.widget.Button" ).click( )
        time.sleep( 3 )
        # if d( text="收件箱​", className="android.widget.TextView" ).exists:
        #     d.swipe( width / 2, height * 4 / 5, width / 2, height / 5 )
        #     time.sleep( 2 )
        # elif d( text="群邮件​", resourceId="com.tencent.androidqqmail:id/t0" ).exists:
        #     pass
        # else:
        #     return
        obj = d( description='待发送' ).child( resourceId="com.tencent.androidqqmail:id/t4" )
        if obj.exists:
            # z.toast( "发送失败" )
            # for it in numbers:
            #     it2 = it["number"]
            #     self.repo.UpdateNumberStauts(it2,repo_mail_cateId,"normal")
            # for bcc in bccNumbers:
            #     bcc2 = bcc["number"]
            #     self.repo.UpdateNumberStauts(bcc2,repo_mail_cateId,"normal")
            failCount = int( args["failCount"] )
            num = 0

            if obj.exists:
                num = obj.info['text']
                if int( num ) >= failCount:
                    z.toast( "共有%s个未发送,跳出模块" % num )
                    return 'over'
        z.heartbeat( )
        if check:
            if (args["time_delay"]):
                z.toast("等待%s秒后查看另一个帐号是否收到邮件"%int(args["time_delay"]))
                time.sleep(int(args["time_delay"]))

            accountObj2 = d( descriptionContains='%s的收件箱有' % repo_mail_cateId2.split( '@' )[0] )
            if not accountObj2.exists:
                account_num2 = 0
            else:
                account_num2 = accountObj2.info['contentDescription']
                account_num2 = int( re.findall( r'\d+', account_num2 )[1] )

            if account_num2 > account_num:
                z.toast( "收到邮件" )
                return 'success'
            else:
                z.toast( "没有收到邮件" )
                return 'fail'

    def action(self, d, z, args):
        import sys
        reload( sys )
        sys.setdefaultencoding( 'utf8' )
        z.toast( "QQ邮箱根据另一个帐号的收信情况发信" )
        random_code = args['random_code']
        # z.toast( "正在ping网络是否通畅" )
        # z.heartbeat( )
        # i = 0
        # while i < 200:
        #     i += 1
        #     ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
        #     print( ping )
        #     if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
        #         z.toast( "网络通畅。开始执行：QQ邮箱发消息" )
        #         break
        # if i > 200:
        #     z.toast( "网络不通，请检查网络状态" )
        #     if (args["time_delay"]):
        #         z.sleep( int( args["time_delay"] ) )
        #     return
        z.heartbeat( )
        # str = d.info  # 获取屏幕大小等信息
        # height = str["displayHeight"]
        # width = str["displayWidth"]
        repo_mail_cateId = int(args['repo_mail_cateId'])
        repo_material_cateId= args["repo_material_cateId"]
        repo_material_cateId2 = args["repo_material_cateId2"]
        size = args["size"]
        # d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
        # d.server.adb.cmd( "shell","am start -n com.tencent.androidqqmail/com.tencent.qqmail.launcher.desktop.LauncherActivity" ).communicate( )  # 拉起来
        d.server.adb.cmd( "shell","am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
        # z.sleep( 7 )
        Str = d.info  # 获取屏幕大小等信息
        height = int(Str["displayHeight"])
        width = int(Str["displayWidth"])
        z.heartbeat( )
        flag1 = False
        flag2 = False
        for t in range(2):
            d.dump( compressed=False )
            if d( text="所有收件箱​",className="android.widget.TextView" ).exists:
                if d(textContains="密码错误，请重新输入").exists:
                    z.toast("密码错误，请重新输入")
                    return
                else:
                    z.toast( "状态正常，继续执行" )
                    break
            else:
                if d( text="温馨提示​", className="android.widget.TextView" ).exists:
                    d( text="确定", className="android.widget.Button" ).click( )
                    z.sleep( 1 )
                    break
                elif d(text="收件人：").exists and d(text="写邮件").exists:
                    flag1 = True
                    break
                elif d(text="取消​",resourceId='com.tencent.androidqqmail:id/a5',index=0).exists:
                    d( text="取消​", resourceId='com.tencent.androidqqmail:id/a5',index=0 ).click()
                    time.sleep(1)
                    if d(text="离开",className="android.widget.Button").exists:
                        d( text="离开", className="android.widget.Button" ).click()
                        time.sleep(1)
                    if d( text="收件箱​", className="android.widget.TextView" ).exists:
                        d.press.back()
                        time.sleep(1)
                        if d( textContains="密码错误，请重新输入" ).exists:
                            z.toast( "密码错误，请重新输入" )
                            return
                        else:
                            z.toast( "状态正常，继续执行" )
                            break

                elif d(index=1,text="写邮件​",className="android.widget.TextView").exists:
                    d.click(60/720 * width,198/1280 * height)
                    flag1 = True
                    break
                else:
                    if t>=1:
                        z.toast( "状态异常，跳过此模块" )
                        return
                    else:
                        d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
                        d.server.adb.cmd( "shell",
                                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                        time.sleep( 5 )
        if d( text="所有收件箱​", className="android.widget.TextView" ).exists:
            if d( textContains="密码错误，请重新输入" ).exists:
                z.toast( "密码错误，请重新输入" )
                return
            # else:
            #     z.toast( "状态正常，继续执行" )
        else:
            z.toast("状态不正常")
            return
        z.heartbeat()
        accountObj = d( className="android.widget.RelativeLayout", index=4, descriptionContains='的收件箱' )
        if accountObj.exists:
            accountObj2 = d(className="android.widget.RelativeLayout", index=5, descriptionContains='的收件箱')
            if not accountObj2.exists:
                z.toast("只有一个帐号，跳出模块")
                return
        else:
            accountObj = d( className="android.widget.RelativeLayout", index=5, descriptionContains='的收件箱' )
            accountObj2 = d( className="android.widget.RelativeLayout", index=6, descriptionContains='的收件箱' )
            if not accountObj2.exists:
                # accountObj2 = d( className="android.widget.RelativeLayout", index=4, descriptionContains='的收件箱' )
                z.toast( "只有一个帐号，跳出模块" )
                return

        account2 = accountObj2.info['contentDescription']
        account2 = re.search(r'\d{5,11}', account2).group(0) + '@qq.com'

        account = accountObj.info['contentDescription']
        account = re.search( r'\d{5,11}', account ).group( 0 ) + '@qq.com'
        # account = accountArr[0]
        sendCount = int(args["sendCount"])
        train_cate_id = args['train_cate_id']
        auto_reply_cate_id = account2
        fj = False
        success1 = False
        success2 = False
        success3 = False
        success4 = False
        success5 = False
        account_num = 0
        accountObj2 = d( descriptionContains='%s的收件箱有' % account2.split( '@' )[0] )
        if not accountObj2.exists:
            account_num = 0
        else:
            account_num = accountObj2.info['contentDescription']
            account_num = int( re.findall( r'\d+', account_num )[1] )


        z.toast("给正常号码和 %s 『不带附件』发消息" %account2)
        for sc in range(4):
            z.heartbeat( )
            result = self.send_mail(d,z,args,fj,repo_mail_cateId,auto_reply_cate_id,account,True,account_num)
            if result=='over':
                return
            elif result=='success':
                # d.press.back( )
                # time.sleep( 1 )
                if sc==0:
                    success1 = True
                elif sc==1:
                    success2 = True
                elif sc==2:
                    success3 = True
                elif sc==3:
                    success5 = True
                break
            else:
                # d.press.back()
                # time.sleep(1)
                if sc==0:
                    fj = True
                    z.toast( "给正常号码和%s『带附件』发消息"% account2 )
                elif sc==1:
                    fj = False
                    repo_mail_cateId = ''
                    z.toast( "给%s发消息" % account2 )
                elif sc==2:
                    fj = True
                    z.toast( "给%s『带附件』发消息" % account2)
                else:
                    fj = True
                    success4 = True
                    z.toast( "给小号『带附件』发消息" )
                    break


        if success1:
            repo_mail_cateId = args['repo_mail_cateId']
            auto_reply_cate_id = repo_mail_cateId
        elif success2:
            # fj = True
            repo_mail_cateId = args['repo_mail_cateId']
            auto_reply_cate_id = repo_mail_cateId
        elif success3 or success5:
            repo_mail_cateId = ''
            auto_reply_cate_id = args['repo_mail_cateId']
        elif success4:
            repo_mail_cateId = ''
            auto_reply_cate_id = args['train_cate_id']
            sendCount = random.randint(3,6)

        for sc in range( sendCount ):
            z.heartbeat( )
            result = self.send_mail( d, z, args, fj, repo_mail_cateId, auto_reply_cate_id, account, False,account_num )
            if result=='over':
                return



        z.toast("模块完成")


def getPluginClass():
    return QQEmailSendTextAll2

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("37f7b82f")
    z = ZDevice("37f7b82f")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_mail_cateId": "399", "repo_material_cateId": "382", "time_delay": "5","sendCount":"6","size":"实际大小","repo_material_cateId2":"383","selectContent":"主题内容都发",
            "failCount":"7","nuberLoop":"循环","addToText":"添加",'train_cate_id':"411",'random_code':"不乱码"}
    # obj = d(description='待发送').child(resourceId="com.tencent.androidqqmail:id/t4")
    # if obj.exists:
    #     print obj.info['text']
    # if d( text='加载更多' ).exists:
    #     d( text='加载更多' ).click( )
    #     time.sleep( 3 )

    o.action(d, z, args)