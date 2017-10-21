# coding:utf-8
from __future__ import division
from smsCode import smsCode
import string
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice


class QQEmailSendText:
    def __init__(self):

        self.repo = Repo()


    def action(self, d, z, args):
        z.toast( "QQ邮箱发消息" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ邮箱发消息" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        repo_mail_cateId = int(args['repo_mail_cateId'])
        repo_material_cateId= args["repo_material_cateId"]
        d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell","am start -n com.tencent.androidqqmail/com.tencent.qqmail.launcher.desktop.LauncherActivity" ).communicate( )  # 拉起来
        z.sleep( 7 )
        Str = d.info  # 获取屏幕大小等信息
        height = Str["displayHeight"]
        width = Str["displayWidth"]
        z.heartbeat( )
        flag1 = False
        flag2 = False
        d.dump( compressed=False )
        if d( text="收件箱​",resourceId="com.tencent.androidqqmail:id/q3" ).exists:
            z.toast( "状态正常，继续执行" )
        else:
            if d( text="温馨提示​", className="android.widget.TextView" ).exists:
                d( text="确定", className="android.widget.Button" ).click( )
                z.sleep( 1 )
            elif d(text="收件人：",resourceId="com.tencent.androidqqmail:id/jw").exists and d(text="写邮件",resourceId="com.tencent.androidqqmail:id/k").exists:
                flag1 = True
            elif d(index=1,text="写邮件​",resourceId="com.tencent.androidqqmail:id/k",className="android.widget.TextView").exists:
                d.click(60/720 * width,198/1280 * height)
                flag1 = True
            else:
                z.toast( "状态异常，跳过此模块" )
                return
        count = int(args["count"])
        numbers = self.repo.GetNumber( repo_mail_cateId, 120, count )
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
        # if d(text="温馨提示​",className="android.widget.TextView").exists:
        #     d(text="确定",className="android.widget.Button").click()
        #     z.sleep(1)
        if d(description="写邮件和设置等功能").exists:
            d( description="写邮件和设置等功能" ).click()
            z.sleep(0.5)
            if d(text="写邮件",resourceId="com.tencent.androidqqmail:id/u3").exists:
                d( text="写邮件", resourceId="com.tencent.androidqqmail:id/u3" ).click()
                z.sleep(0.5)
                d.click( 60 / 720 * width, 198 / 1280 * height )
                z.sleep(0.5)
                flag2 = True
        if flag2 or flag1:
            for i in range(0,count):
                QQEmail = numbers[i]['number'].encode("utf-8")
                if "@qq.com" not in QQEmail:
                    z.input( QQEmail + "@qq.com " )
                else:
                    z.input( QQEmail + " " )
                print(QQEmail + "@qq.com")
        z.sleep(1)
        d.dump( compressed=False )
        if not d(textContains="抄送/密送，发件人").exists:
            obj = d(index=0,className="android.webkit.WebView").child(index=0,className="android.view.View").child(index=0,className="android.view.View")
            while not obj.exists:
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                d.dump( compressed=False )
            obj.click()
            z.input( message.encode( "utf-8" ) )
        else:
            while not d(index=0,resourceId="com.tencent.androidqqmail:id/mp",className="android.widget.EditText").exists:
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                d.dump( compressed=False )
            if d(index=0,resourceId="com.tencent.androidqqmail:id/mp",className="android.widget.EditText").exists:
                text = d( index=0, resourceId="com.tencent.androidqqmail:id/mp", className="android.widget.EditText" ).info["text"].encode("utf-8")
                z.sleep(0.5)
                if text=="" or text==None:
                    d( index=0, resourceId="com.tencent.androidqqmail:id/mp", className="android.widget.EditText" ).click()
                    z.input(message.encode("utf-8"))
                    z.sleep(0.5)
        if d(resourceId="com.tencent.androidqqmail:id/m1",description="附件操作").exists:
            d( resourceId="com.tencent.androidqqmail:id/m1", description="附件操作" ).click()
            z.sleep(0.5)
            if d(resourceId="com.tencent.androidqqmail:id/cu",description="从相册选择文件").exists:
                d( resourceId="com.tencent.androidqqmail:id/cu", description="从相册选择文件" ).click()
                z.sleep(5)
                obj = d( index=2, resourceId="com.tencent.androidqqmail:id/de",className="android.widget.GridView" ).child(
                    index=1, className="android.widget.RelativeLayout" ).child(
                    index=2, resourceId="com.tencent.androidqqmail:id/t8",className="android.widget.CheckBox" )
                if obj.exists:
                    obj.click( )
                    z.sleep( 0.5 )
                    if d( textContains="添加到邮件", resourceId="com.tencent.androidqqmail:id/do" ).exists:
                        d( textContains="添加到邮件", resourceId="com.tencent.androidqqmail:id/do" ).click( )
                        z.sleep( 2 )
                        if d( index=1, resourceId="com.tencent.androidqqmail:id/cz",
                              className="android.widget.HorizontalScrollView" ).child( index=0,
                                                                                       resourceId="com.tencent.androidqqmail:id/d0",
                                                                                       className="android.widget.LinearLayout" ).exists:
                            d( index=1, resourceId="com.tencent.androidqqmail:id/cz",
                               className="android.widget.HorizontalScrollView" ).child( index=0,
                                                                                        resourceId="com.tencent.androidqqmail:id/d0",
                                                                                        className="android.widget.LinearLayout" ).click( )
                            z.sleep( 0.5 )
                            z.heartbeat( )
                            if d( text="添加到正文", resourceId="com.tencent.androidqqmail:id/hy" ).exists:
                                d( text="添加到正文", resourceId="com.tencent.androidqqmail:id/hy" ).click( )
                                z.sleep( 0.5 )

                else:
                    z.toast( "没有图片,停止模块" )
                    return
        d.dump( compressed=False )
        if d( index=3, text="发送​", resourceId="com.tencent.androidqqmail:id/d",className="android.widget.Button" ).exists:
            d( index=3, text="发送​", resourceId="com.tencent.androidqqmail:id/d",className="android.widget.Button" ).click( )
            z.sleep(2)
            if d(textContains="小",resourceId="com.tencent.androidqqmail:id/hy",className="android.widget.TextView").exists:
                d( textContains="小", resourceId="com.tencent.androidqqmail:id/hy", className="android.widget.TextView" ).click()
        else:
            pass
        if d( index=3, text="发送​", resourceId="com.tencent.androidqqmail:id/d",className="android.widget.Button" ).exists:
            z.toast("发送不了")
            return
        if d(index=2,className="android.widget.Button").exists:
            d( index=2, className="android.widget.Button" ).click()
        z.toast("模块完成")
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return QQEmailSendText

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("cda0ae8d")
    z = ZDevice("cda0ae8d")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_mail_cateId": "119", "repo_material_cateId": "39", "time_delay": "3","count":"3"};

    o.action(d, z, args)

