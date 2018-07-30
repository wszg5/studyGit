# coding:utf-8
from __future__ import division
from smsCode import smsCode
import string
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice


class QQEmailHandleSpam:
    def __init__(self):

        self.repo = Repo()

    def input(self,z,height,text):
        if height>888:
            z.input(text)
        else:
            z.cmd( "shell", "am broadcast -a ZY_INPUT_TEXT --es text \\\"%s\\\"" % text )

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

    def action(self, d, z, args):
        import sys
        reload( sys )
        sys.setdefaultencoding( 'utf8' )
        z.toast( "QQ邮箱标记非垃圾邮件" )
        z.heartbeat( )
        # str = d.info  # 获取屏幕大小等信息
        # height = str["displayHeight"]
        # width = str["displayWidth"]
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
            if d( text="收件箱​",className="android.widget.TextView" ).exists:
                if d(textContains="密码错误，请重新输入").exists:
                    z.toast("密码错误，请重新输入")
                    return
                else:
                    # z.toast( "状态正常，继续执行" )
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
        if d( text="收件箱​", className="android.widget.TextView" ).exists:
            if d( textContains="密码错误，请重新输入" ).exists:
                z.toast( "密码错误，请重新输入" )
                return
            else:
                z.toast( "状态正常，继续执行" )
        else:
            z.toast("状态不正常")
            return
        while True:
            d.swipe( width / 2, height * 4 / 5, width / 2, height / 5 )
            time.sleep( 2 )
            if d( textContains="垃圾箱", className="android.widget.TextView" ).exists:
                d( textContains="垃圾箱", className="android.widget.TextView" ).click()
                time.sleep(3)
                obj = d( index=5, className="android.widget.RelativeLayout" ).child( index=0, className="android.widget.FrameLayout" )
                if obj.exists:
                    obj.click()
                    time.sleep(3)
                    for x in range(5):
                        if d(resourceId="com.tencent.androidqqmail:id/f",description="更多操作").exists:
                            d( resourceId="com.tencent.androidqqmail:id/f", description="更多操作" ).click()
                            time.sleep(2)
                            d(text="这不是垃圾邮件",resourceId="com.tencent.androidqqmail:id/lf").click()
                            time.sleep(2)
                            if d(text="我知道了",className="android.widget.Button").exists:
                                d( text="我知道了", className="android.widget.Button" ).click()
                                time.sleep(2)
                        else:
                            break
                    else:
                        d.server.adb.cmd( "shell",
                                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                        time.sleep( 2 )
                else:
                    break

        z.toast("模块完成")
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return QQEmailHandleSpam

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("9cae944e")
    z = ZDevice("9cae944e")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"mailType": "只删收件箱","time_delay": "3",}
    # Str = d.info  # 获取屏幕大小等信息
    # height = int( Str["displayHeight"] )
    # width = int( Str["displayWidth"] )
    # o.input(z,height,"扎广泛的烦恼")
    o.action(d, z, args)
    # d(index=5,className="android.widget.RelativeLayout").child(index=0,className="android.widget.FrameLayout").long_click()
    # d(className="android.widget.Button",textContains="全选").click()
    # d(textContains="删除",className="android.widget.Button").click()
    # print "ds"

