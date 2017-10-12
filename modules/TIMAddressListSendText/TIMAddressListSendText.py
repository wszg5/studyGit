# coding:utf-8
import colorsys
import os
from PIL import Image
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice


class TIMAddressCheckDeposit:
    def __init__(self):
        self.repo = Repo( )
        self.xuma = None

    def GetUnique(self):
        nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" );  # 生成当前时间
        randomNum = random.randint( 0, 1000 );  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str( 00 ) + str( randomNum );
        uniqueNum = str( nowTime ) + str( randomNum );
        return uniqueNum


    def Bind(self, d, z):
        circle = 0
        self.scode = smsCode( d.server.adb.device_serial( ) )
        newStart = 1
        while newStart == 1:
            GetBindNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )
            print( GetBindNumber )
            z.sleep( 2 )
            z.heartbeat()
            obj = d( className="android.view.View", description="删除 按钮" )
            if obj.exists:
                z.heartbeat( )
                z.sleep( 1 )
                obj.click( )
            z.sleep(2)
            d( resourceId='com.tencent.tim:id/name', className='android.widget.EditText' ).set_text(GetBindNumber )  # GetBindNumber
            z.heartbeat( )
            z.sleep( 1 )
            d( text='下一步' ).click( )
            z.sleep( 3 )
            if d( text='下一步' ).exists:  # 操作过于频繁的情况
                return 'false'
            if d( text='确定' ).exists:  # 提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d( text='确定', ).click( )
            z.heartbeat( )
            code = self.scode.GetVertifyCode( GetBindNumber, self.scode.QQ_CONTACT_BIND, '4' )
            d( resourceId='com.tencent.tim:id/name', className='android.widget.EditText' ).set_text( code )
            print( code )
            newStart = 0
            if d( text='请输入短信验证码' ).exists:
                if circle < 4:
                    z.toast( '没有接收到验证码' )
                    d( textContains='返回' ).click( )
                    if d( text='确定' ).exists:
                        d( text='返回' ).click( )
                        z.sleep( 1 )
                    d( description='删除 按钮' ).click( )
                    circle = circle + 1
                    newStart = 1
                    continue
                else:
                    z.toast( '程序结束' )
                    print( circle )
                    return 'false'
            z.heartbeat( )
            d( text='完成', resourceId='com.tencent.tim:id/name' ).click( )
            z.sleep( 10 )
            if d( textContains='没有可匹配的' ).exists:
                return 'false'
        return 'true'

    def bindPhoneNumber(self, z, d):
        z.toast( "点击开始绑定" )
        self.scode = smsCode( d.server.adb.device_serial( ) )
        d( text='马上绑定' ).click( )
        while d( text='验证手机号码' ).exists:
            PhoneNumber = None
            j = 0
            while PhoneNumber is None:
                j += 1
                PhoneNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )  # 获取接码平台手机号码
                z.heartbeat( )
                if j > 20:
                    z.toast( '取不到手机号码' )
                    return "nothing"
            if not d( textContains='+86' ).exists:
                d( description='点击选择国家和地区' ).click( )
                if d( text='中国' ).exists:
                    d( text='中国' ).click( )
                else:
                    str = d.info  # 获取屏幕大小等信息
                    height = str["displayHeight"]
                    width = str["displayWidth"]
                    d.click( width * 5 / 12, height * 5 / 32 )
                    z.sleep( 1.5 )
                    z.input( '中国' )
                    z.sleep( 2 )
                    d( text='+86' ).click( )
            z.heartbeat( )
            obj = d( className="android.view.View", description="删除 按钮" )
            if obj.exists:
                z.heartbeat( )
                z.sleep( 1 )
                obj.click( )
            z.sleep( 2 )
            z.input( PhoneNumber )
            z.sleep( 1.5 )
            if d( text='下一步' ).exists:
                d( text='下一步' ).click( )
                z.sleep( 3 )
            if d( text='确定' ).exists:
                d( text='确定' ).click( )
                z.sleep( 2 )
            code = self.scode.GetVertifyCode( PhoneNumber, self.scode.QQ_CONTACT_BIND, '4' )  # 获取接码验证码
            self.scode.defriendPhoneNumber( PhoneNumber, self.scode.QQ_CONTACT_BIND )
            if code == '':
                z.toast( PhoneNumber + '手机号,获取不到验证码' )
                if d( text='返回' ).exists:
                    d( text='返回' ).click( )
                if not d( textContains='中国' ).exists:
                    if d( text='返回' ).exists:
                        d( text='返回' ).click( )
                if d( className='android.view.View', descriptionContains='删除' ).exists:
                    d( className='android.view.View', descriptionContains='删除' ).click( )
                continue
            z.heartbeat( )
            z.input( code )
            if d( text='完成' ).exists:
                d( text='完成' ).click( )
            z.sleep( 5 )
            break
        z.sleep( 1 )

    def action(self, d, z, args):
        z.toast( "准备执行TIM通讯录群发消息" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM通讯录群发消息" )
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
        d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        z.heartbeat( )
        if d( text="消息", resourceId="com.tencent.tim:id/ivTitleName" ).exists:
            z.toast( "登录状态正常，继续执行" )
        else:
            if d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).exists:
                d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).click( )
                z.sleep( 1 )
            elif d( text="消息", className="android.widget.TextView" ).exists and d( text="马上绑定",
                                                                                  className="android.widget.Button" ).exists:
                d( text="消息", className="android.widget.TextView" ).click( )
                z.sleep( 1 )
            elif d( text="返回" ).exists:
                d( text="返回" ).click( )
                z.sleep( 1 )

            else:
                z.toast( "登录状态异常，跳过此模块" )
                return
        repo_meg_id = args["repo_meg_id"]
        # Material = self.repo.GetMaterial( repo_meg_id, 0, 1 )
        # if len( Material ) == 0:
        #     d.server.adb.cmd( "shell",
        #                       "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % repo_meg_id ).communicate( )
        #     z.sleep( 10 )
        #     return
        # message = Material[0]['content']
        if d( text='马上绑定' ).exists:
            result = self.bindPhoneNumber( z, d )
            if result == "nothing":
                return
        if d( text='通讯录' ).exists:
            d( text='关闭' ).click( )
        d( description='快捷入口' ).click( )
        d( textContains='加好友' ).click( )
        d( text='添加手机联系人' ).click( )
        z.heartbeat( )
        if d(text="匹配手机通讯录").exists:
            d( text="匹配手机通讯录" ).click()
            z.sleep(1)
            z.heartbeat()
        while d( text='验证手机号码' ).exists:
            PhoneNumber = None
            j = 0
            while PhoneNumber is None:
                j += 1
                PhoneNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )  # 获取接码平台手机号码
                z.heartbeat( )
                if j > 2:
                    z.toast( '取不到手机号码' )
                    if (args["time_delay"]):
                        z.sleep( int( args["time_delay"] ) )
                    return
            z.heartbeat( )
            obj = d( className="android.view.View", description="删除 按钮" )
            if obj.exists:
                z.heartbeat( )
                z.sleep( 1 )
                obj.click( )
            z.sleep( 2 )
            z.input( PhoneNumber )
            z.sleep( 1.5 )
            if d( text='下一步' ).exists:
                d( text='下一步' ).click( )
                z.sleep( 3 )
            if d( text='确定' ).exists:
                d( text='确定' ).click( )
                z.sleep( 2 )
            code = self.scode.GetVertifyCode( PhoneNumber, self.scode.QQ_CONTACT_BIND, '4' )  # 获取接码验证码
            self.scode.defriendPhoneNumber( PhoneNumber, self.scode.QQ_CONTACT_BIND )
            if code == '':
                z.toast( PhoneNumber + '手机号,获取不到验证码' )
                if d( text='返回' ).exists:
                    d( text='返回' ).click( )
                if not d( textContains='中国' ).exists:
                    if d( text='返回' ).exists:
                        d( text='返回' ).click( )
                if d( className='android.view.View', descriptionContains='删除' ).exists:
                    d( className='android.view.View', descriptionContains='删除' ).click( )
                continue
            z.heartbeat( )
            z.input( code )
            if d( text='完成' ).exists:
                d( text='完成' ).click( )
            z.sleep( 5 )
            break
        # if d( resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText',
        #       index=2 ).exists:  # 检查到尚未 启用通讯录
        if d(text="启用").exists:          # 检查到尚未 启用通讯录
            d(text="启用").click()
            if not d( textContains='+86' ).exists:
                d( description='点击选择国家和地区' ).click( )
                if d( text='中国' ).exists:
                    d( text='中国' ).click( )
                else:
                    str = d.info  # 获取屏幕大小等信息
                    height = str["displayHeight"]
                    width = str["displayWidth"]
                    d.click( width * 5 / 12, height * 5 / 32 )
                    z.sleep( 1.5 )
                    z.input( '中国' )
                    z.sleep( 2 )
                    d( text='+86' ).click( )
            z.heartbeat( )
            text = self.Bind( d, z )  # 未开启通讯录的，现绑定通讯录
            z.heartbeat( )
            if text == 'false':  # 操作过于频繁的情况
                if (args["time_delay"]):
                    z.sleep( int( args["time_delay"] ) )
                return
            z.sleep( 3 )
        if d( textContains='没有可匹配的' ).exists:
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        if d( text='匹配手机通讯录' ).exists:
            d( text='匹配手机通讯录' ).click( )
            z.heartbeat( )
            z.sleep( 2 )
        obj1 = d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                                                                  index=2 ) \
            .child( className='android.widget.ImageView', index=0 )  # 判断第一次进通讯录是否有人
        if not obj1.exists:
            d( text='添加' ).click( )
            z.sleep( 1.5 )
            d( text='添加手机联系人' ).click( )
            if not obj1.exists:
                z.toast( "该手机上没有联系人" )
                if (args["time_delay"]):
                    z.sleep( int( args["time_delay"] ) )
                return
        index=1
        listNum = []
        unclick1 = True
        unclick2 = True
        n = 1
        while True:
            x = 0
            Material = self.repo.GetMaterial( repo_meg_id, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % repo_meg_id ).communicate( )
                z.sleep( 10 )
                return
            message = Material[0]['content']
            if unclick1:
                index = 2
                unclick1 = False
            obj2 =  obj = d(index=0,resourceId='com.tencent.tim:id/name', className='android.widget.AbsListView').child(
        className="android.widget.LinearLayout", index=index).child(className="android.widget.TextView",index=1)  # 第i个内容存在并且是人的情况
            if obj2.exists:
                # getPhoneInfo = d( index=0, resourceId='com.tencent.tim:id/name', className='android.widget.AbsListView' ).child(
                #     className="android.widget.LinearLayout", index=index ).child( resourceId="com.tencent.tim:id/name",className="android.widget.TextView", index=1 )
                if obj2.exists:
                    phoneNum = obj2.info['text'].encode("utf-8")
                    if phoneNum not in listNum and phoneNum !="备份通讯录":
                        listNum.append( phoneNum )
                        obj2.click()
                        z.sleep(1)
                        z.heartbeat()
                        if d(text="发消息",className="android.widget.Button").exists:
                            d( text="发消息", className="android.widget.Button" ).click()
                            z.sleep(1)
                            z.heartbeat()
                            obj = d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).left( index=0,
                                                                                                resourceId="com.tencent.tim:id/input",
                                                                                                className="android.widget.EditText" )
                            if obj.exists:
                                obj.click( )
                                z.sleep( 1 )
                                z.input( message )
                                z.sleep( 1 )
                                z.heartbeat( )

                            if d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).exists:
                                d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).click( )
                                z.sleep( 2 )
                                z.heartbeat()
                                if d(textContains="消息",resourceId="com.tencent.tim:id/ivTitleBtnLeft").exists:
                                    d( textContains="消息", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click()
                                    z.sleep(1)
                                    z.heartbeat()
                                    d( description='快捷入口' ).click( )
                                    d( textContains='加好友' ).click( )
                                    d( text='添加手机联系人' ).click( )
                                    while x < n-1:
                                        d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                                        x = x + 1

                    index = index + 1
                    continue
            else:
                if unclick2:
                    index = index
                    unclick2 = False
                else:
                    index = index - 1
                    z.heartbeat()
                    z.sleep(1)
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                n = n + 1
                z.sleep(2)
                obj2 = obj = d( index=0, resourceId='com.tencent.tim:id/name',
                                className='android.widget.AbsListView' ).child(
                    className="android.widget.LinearLayout", index=index ).child( className="android.widget.TextView",
                                                                               index=1 )
                if obj2.exists:
                    phoneNum = obj2.info['text']
                    if phoneNum  in listNum:
                        z.toast( "通讯录好友都发过消息了，模块结束运行" )
                        return
                index=1
                z.sleep(1)
                continue
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )


def getPluginClass():
    return TIMAddressCheckDeposit


if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "HT54VSK01061" )
    z = ZDevice( "HT54VSK01061" )
    z.server.install( )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).communicate( )
    args = {"time_delay": "3","repo_meg_id":"40"};  # cate_id是仓库号，length是数量
    o.action( d, z, args )
