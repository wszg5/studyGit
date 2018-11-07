# coding:utf-8
from __future__ import division
from smsCode import smsCode
import string
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice


class QQEmailReply:
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
        z.toast( "QQ邮箱收件箱回复" )
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
        #     z.sleep( 2 )
        # if i > 200:
        #     z.toast( "网络不通，请检查网络状态" )
        #     if (args["time_delay"]):
        #         z.sleep( int( args["time_delay"] ) )
        #     return
        z.heartbeat( )
        # str = d.info  # 获取屏幕大小等信息
        # height = str["displayHeight"]
        # width = str["displayWidth"]
        repo_material_cateId= args["repo_material_cateId"]
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
        z.heartbeat( )
        # accountObj = d( resourceId="com.tencent.androidqqmail:id/ac", textContains="@",
        #                 className="android.widget.TextView" )
        # account = accountObj.info["text"]
        # account = accountArr[0]
        if d( textContains="收件箱", className="android.widget.TextView" ).exists:
            d( textContains="收件箱", className="android.widget.TextView" ).click( )
            time.sleep( 3 )
        while True:
            z.heartbeat( )
            obj = d( index=5, className="android.widget.RelativeLayout" ).child( index=0,className="android.widget.FrameLayout" )
            if obj.exists:
                if obj.child( descriptionContains="来自qq.com的退信" ).exists or obj.child(descriptionContains='主题是：Re').exists \
                        or obj.child(descriptionContains='主题是：re').exists or obj.child(descriptionContains='主题是：RE').exists \
                        or obj.child( descriptionContains='主题是：回复' ).exists or obj.child(descriptionContains='主题是：自动回复').exists:
                    z.toast( "这是退信或带有回复的信" )
                    obj.long_click( )
                    time.sleep( 2 )
                    if d( textContains="删除", className="android.widget.Button" ).exists:
                        d( textContains="删除", className="android.widget.Button" ).click( )
                        time.sleep( 3 )
                        continue
                        # obj = d( index=5, className="android.widget.RelativeLayout" ).child( index=0,
                        #                                                                      className="android.widget.FrameLayout" )
                        # if obj.exists:
                        #     obj.click( )
                        #     time.sleep( 3 )
                        # else:
                        #     z.toast( "没有邮件" )
                        #     return False
                else:
                    obj.click( )
                    time.sleep( 4 )
                    z.heartbeat( )
                    if d( description="回复和转发", resourceId="com.tencent.androidqqmail:id/g" ).exists:
                        d( description="回复和转发", resourceId="com.tencent.androidqqmail:id/g" ).click( )
                        time.sleep( 1 )
                        if d( resourceId="com.tencent.androidqqmail:id/lj", text="回复" ).exists:
                            d( resourceId="com.tencent.androidqqmail:id/lj", text="回复" ).click( )
                            time.sleep( 4 )
                            Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                            if len( Material ) == 0:
                                d.server.adb.cmd( "shell",
                                                  "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_material_cateId ).communicate( )
                                z.sleep( 10 )
                                return
                            message = Material[0]['content']
                            self.input( z, height, message )
                            z.heartbeat( )
                            if d( text="发送​", resourceId="com.tencent.androidqqmail:id/a_" ).exists:
                                d( text="发送​", resourceId="com.tencent.androidqqmail:id/a_" ).click( )
                                time.sleep( 3 )
                            if d( description="删除邮件", resourceId="com.tencent.androidqqmail:id/c" ).exists:
                                d( description="删除邮件", resourceId="com.tencent.androidqqmail:id/c" ).click( )
                                time.sleep( 4 )
                                d.press.back()
                                time.sleep(1)
                            else:
                                result = self.deleteMail( d )
                                if result:
                                    continue
                                else:
                                    break
                        else:
                            if d( description="删除邮件", resourceId="com.tencent.androidqqmail:id/c" ).exists:
                                d( description="删除邮件", resourceId="com.tencent.androidqqmail:id/c" ).click( )
                                time.sleep( 1 )
                                d.press.back( )
                                time.sleep( 1 )
                            else:
                                result = self.deleteMail( d )
                                if result:
                                    continue
                                else:
                                    break

                    else:
                        if d( description="删除邮件", resourceId="com.tencent.androidqqmail:id/c" ).exists:
                            d( description="删除邮件", resourceId="com.tencent.androidqqmail:id/c" ).click( )
                            time.sleep( 1 )
                        else:
                            result = self.deleteMail( d )
                            if result:
                                continue
                            else:
                                break
            else:
                z.toast("没有邮件了")
                return
        while True:
            if d(description="回复和转发",resourceId="com.tencent.androidqqmail:id/g").exists:
                d( description="回复和转发", resourceId="com.tencent.androidqqmail:id/g" ).click()
                time.sleep(1)
                if d(resourceId="com.tencent.androidqqmail:id/lj",text="回复").exists:
                    d( resourceId="com.tencent.androidqqmail:id/lj", text="回复" ).click()
                    time.sleep(4)
                    Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                    if len( Material ) == 0:
                        d.server.adb.cmd( "shell",
                                          "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_material_cateId ).communicate( )
                        z.sleep( 10 )
                        return
                    message = Material[0]['content']
                    self.input(z,height,message)
                    z.heartbeat( )
                    if d(text="发送​",resourceId="com.tencent.androidqqmail:id/a_").exists:
                        d( text="发送​", resourceId="com.tencent.androidqqmail:id/a_" ).click()
                        time.sleep(3)
                    if d(description="删除邮件",resourceId="com.tencent.androidqqmail:id/c").exists:
                        d( description="删除邮件", resourceId="com.tencent.androidqqmail:id/c" ).click()
                        time.sleep(4)
                    else:
                        result = self.deleteMail(d)
                        if result:
                            continue
                        else:
                            break
                else:
                    if d(description="删除邮件",resourceId="com.tencent.androidqqmail:id/c").exists:
                        d( description="删除邮件", resourceId="com.tencent.androidqqmail:id/c" ).click()
                        time.sleep(1)
                    else:
                        result = self.deleteMail(d)
                        if result:
                            continue
                        else:
                            break

            else:
                if d( description="删除邮件", resourceId="com.tencent.androidqqmail:id/c" ).exists:
                    d( description="删除邮件", resourceId="com.tencent.androidqqmail:id/c" ).click( )
                    time.sleep( 1 )
                else:
                    result = self.deleteMail( d )
                    if result:
                        continue
                    else:
                        break

        z.toast("模块完成")
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

    def deleteMail(self, d):
        d.server.adb.cmd( "shell","am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
        time.sleep( 2 )
        if d( text="取消​", resourceId='com.tencent.androidqqmail:id/a5', index=0 ).exists:
            d( text="取消​", resourceId='com.tencent.androidqqmail:id/a5', index=0 ).click( )
            time.sleep( 1 )
            if d( text="离开", className="android.widget.Button" ).exists:
                d( text="离开", className="android.widget.Button" ).click( )
                time.sleep( 1 )
            if d( text="收件箱​", className="android.widget.TextView" ).exists:
                if d( textContains="密码错误，请重新输入" ).exists:
                    z.toast( "密码错误，请重新输入" )
                    return False
                else:
                    z.toast( "状态正常，继续执行" )
        z.heartbeat( )
        if d( textContains="收件箱", className="android.widget.TextView" ).exists:
            d( textContains="收件箱", className="android.widget.TextView" ).click( )
            time.sleep( 3 )
            obj = d( index=5, className="android.widget.RelativeLayout" ).child( index=0,
                                                                                 className="android.widget.FrameLayout" )
            if obj.exists:
                obj.long_click( )
                time.sleep(2)
                z.heartbeat( )
                if d( textContains="删除", className="android.widget.Button" ).exists:
                    d( textContains="删除", className="android.widget.Button" ).click( )
                    time.sleep( 3 )
                    return True

            else:
                return False
        else:
            return False

def getPluginClass():
    return QQEmailReply

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("37f7b82f")
    z = ZDevice("37f7b82f")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_cateId": "383", "time_delay": "3"}
    # Str = d.info  # 获取屏幕大小等信息
    # height = int( Str["displayHeight"] )
    # width = int( Str["displayWidth"] )
    # o.input(z,height,"扎广泛的烦恼")
    o.action(d, z, args)

