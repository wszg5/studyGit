# coding:utf-8
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
from PIL import Image
import colorsys
# from RClient import *


class QlAddFriendsByAddressList:
    def __init__(self):

        self.repo = Repo()


    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def Bind(self, d, z):
        circle = 0
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        self.scode = smsCode( d.server.adb.device_serial( ) )
        newStart = 1
        while newStart == 1:
            GetBindNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )
            print( GetBindNumber )
            z.sleep( 2 )
            if d(text="请输入你的手机号码",className="android.widget.EditText").exists:
                d(text="请输入你的手机号码",className="android.widget.EditText").set_text(GetBindNumber)
            else:
                x1 = 502 / 540
                y1 = 279 / 888
                z.sleep(1)
                z.heartbeat()
                d.click(x1*width,y1*height)
                z.sleep(1)
                z.heartbeat()
                d( text="请输入你的手机号码", className="android.widget.EditText" ).set_text( GetBindNumber )
            z.heartbeat( )
            z.sleep( 1 )
            d( text='下一步' ).click( )
            z.sleep( 3 )
            if d( text='下一步' ).exists:  # 操作过于频繁的情况
                return 'false'
            if d( text='确定' ).exists:  # 提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d( text='确定', ).click( )
            z.heartbeat( )
            try:
                code = self.scode.GetVertifyCode( GetBindNumber, self.scode.QQ_CONTACT_BIND, '4' )
                z.input(code)
                print( code )
            except :
                z.toast("取不到验证码")
            # d( resourceId='com.tencent.tim:id/name', className='android.widget.EditText' ).set_text( code )
            # d(text="请输入短信验证码").set_text(code)
            newStart = 0
            if d( text='请输入短信验证码' ).exists:
                if circle < 4:
                    z.toast( '没有接收到验证码' )
                    # d( textContains='返回' ).click( )
                    if d( text='下一步' ).exists:
                        d( text='验证手机号码' ).click( )
                        if d(text="验证手机号").exists:
                            d(text="验证手机号").click()
                        z.sleep( 1 )

                    # d( description='删除 按钮' ).click( )
                    objtext = d(index=2,resourceId="com.tencent.qqlite:id/0",className="android.widget.EditText").info["text"]
                    lenth = len( objtext )
                    t = 0
                    while t < lenth:
                        d.press.delete( )
                        t = t + 1
                    time.sleep( 2 )
                    circle = circle + 1
                    newStart = 1
                    continue
                else:
                    z.toast( '程序结束' )
                    print( circle )
                    return 'false'
            z.heartbeat( )
            d( text='下一步' ).click( )
            if d(text="“QQ”想访问你的通讯录").exists:
                while d(text="好",className="android.widget.TextView").exists:
                    d( text="好", className="android.widget.TextView" ).click()
            z.sleep( 2 )
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
            if d( text='下一步' ).exists:
                d( text='下一步' ).click( )
            z.sleep( 5 )
            if d(text="“QQ”想访问你的通讯录").exists:
                while d(text="好",className="android.widget.TextView").exists:
                    d( text="好", className="android.widget.TextView" ).click()
            break
        z.sleep( 1 )

    def action(self, d, z, args):
        z.toast("准备执行轻聊版通讯录加好友")
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：轻聊版通讯录加好友" )
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
        d.server.adb.cmd( "shell", "am force-stop com.tencent.qqlite" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        z.heartbeat( )
        cate_id1 = args["repo_material_id"]
        Material = self.repo.GetMaterial( cate_id1, 0, 1 )
        message = Material[0]['content']  # 取出验证消息的内容
        if d( text="消息" ).exists:
            z.toast( "卡槽状态正常，继续执行" )
        else:
            z.toast( "卡槽状态异常，跳过此模块" )
            return
        if d( text='马上绑定' ).exists:
            result = self.bindPhoneNumber( z, d )
            if result == "nothing":
                return
        if d( text='通讯录' ).exists:
            d( text='关闭' ).click( )
        z.sleep(1)
        z.heartbeat()
        d(text="联系人").click()
        z.heartbeat()
        d( text='通讯录' ).click()
        z.heartbeat( )
        while d( text='验证手机号码' ).exists:
            text = self.Bind( d, z )  # 未开启通讯录的，现绑定通讯录
            z.heartbeat( )
            if text == 'false':  # 操作过于频繁的情况
                if (args["time_delay"]):
                    z.sleep( int( args["time_delay"] ) )
                print("操作频繁1")
                return
            z.sleep( 3 )

        #     PhoneNumber = None
        #     j = 0
        #     while PhoneNumber is None:
        #         j += 1
        #         PhoneNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )  # 获取接码平台手机号码
        #         z.heartbeat( )
        #         if j > 2:
        #             z.toast( '取不到手机号码' )
        #             if (args["time_delay"]):
        #                 z.sleep( int( args["time_delay"] ) )
        #             return
        #     z.input( PhoneNumber )
        #     z.sleep( 1.5 )
        #     if d( text='下一步' ).exists:
        #         d( text='下一步' ).click( )
        #         z.sleep( 3 )
        #     if d( text='确定' ).exists:
        #         d( text='确定' ).click( )
        #         z.sleep( 2 )
        #     code = self.scode.GetVertifyCode( PhoneNumber, self.scode.QQ_CONTACT_BIND, '4' )  # 获取接码验证码
        #     self.scode.defriendPhoneNumber( PhoneNumber, self.scode.QQ_CONTACT_BIND )
        #     if code == '':
        #         z.toast( PhoneNumber + '手机号,获取不到验证码' )
        #         if d( text='返回' ).exists:
        #             d( text='返回' ).click( )
        #         if not d( textContains='中国' ).exists:
        #             if d( text='返回' ).exists:
        #                 d( text='返回' ).click( )
        #         if d( className='android.view.View', descriptionContains='删除' ).exists:
        #             d( className='android.view.View', descriptionContains='删除' ).click( )
        #         continue
        #     z.heartbeat( )
        #     z.input( code )
        #     if d( text='完成' ).exists:
        #         d( text='完成' ).click( )
        #     z.sleep( 5 )
        #     break
        if d( text="“QQ”想访问你的通讯录" ).exists:
            while d( text="好", className="android.widget.TextView" ).exists:
                d( text="好", className="android.widget.TextView" ).click( )
        # if d( resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText',
        #       index=2 ).exists:  # 检查到尚未 启用通讯录
        if d( text="启用" ).exists:  # 检查到尚未 启用通讯录
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
                z.toast("操作频繁，稍后再试")
                print( "操作频繁2" )
                return
            z.sleep( 3 )
        if d( textContains='没有可匹配的' ).exists:
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            print( "没有可匹配的" )
            return
        if d( text='匹配通讯录' ).exists:
            d( text='匹配通讯录' ).click( )
        z.heartbeat( )
        z.sleep( 5 )
        obj1 = d(index=0, resourceId='com.tencent.qqlite:id/0' ).child( className='android.widget.RelativeLayout',index=0 ) # 判断第一次进通讯录是否有人
        if not obj1.exists:
            d( text='通讯录' ).click( )
            z.sleep( 1.5 )
            z.toast( "该手机上没有联系人" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            print( "该手机无联系人" )
            return
        count = 0
        index = 2
        EndIndex = int(args['EndIndex'])
        # while index < EndIndex + 1:
        # for index in range(2,EndIndex+3):
        #     cate_id = args["repo_material_id"]
        #     time.sleep(2)
        num = 0
        index = 0
        listNum = []
        unclick1 = True
        unclick2 = True
        while True:
            # for k in range( 1, 15 ):
            obj2 = d(index=0, resourceId='com.tencent.qqlite:id/0' ).child( className='android.widget.RelativeLayout',index=index ).child(
                index=0,className="android.widget.LinearLayout").child(index=2,className="android.widget.Button",resourceId="com.tencent.qqlite:id/0")  # 第i个内容存在并且是人的情况
            if obj2.exists:
                obj2 = d(index=0, resourceId='com.tencent.qqlite:id/0' ).child( className='android.widget.RelativeLayout',index=index ).child(
                index=0,className="android.widget.LinearLayout").child(index=1,className="android.widget.TextView",resourceId="com.tencent.qqlite:id/0")
                z.heartbeat()
                while d(text="通讯录").exists:
                    obj2.click( )
                z.sleep( 1 )
                obj3= d(index=1,resourceId="com.tencent.qqlite:id/info",className="android.widget.TextView")
                if obj3.exists:
                    obj3 = obj3.info["text"]
                    if obj3 not in listNum:
                        listNum.append(obj3)
                    else:
                        index = index +1
                        d( text="个人资料" ).click( )
                        continue
                if d( text="加好友").exists:
                    d( text="加好友").click( )

                z.sleep( 1 )
                z.heartbeat( )
                if d( text="加好友" ).exists:  # 拒绝被添加的轻况或请求失败
                    num = num + 1
                    index = index + 1
                    if num > 3:
                        z.toast( "请求失败，无法添加，退出模块" )
                        print( "请求失败" )
                        return
                    while d(text="个人资料").exists:
                        d(text="个人资料").click()
                    continue
                if d( text='必填' ).exists:  # 要回答问题的情况
                    z.heartbeat( )
                    d( text="身份验证" ).click( )
                    while d(text="个人资料").exists:
                        d(text="个人资料").click()
                    index = index + 1
                    num = 0
                    continue
                d.dump( compressed=False )
                if d( text="风险提示" ).exists:  # 风险提示
                    d( text="取消" ).click( )
                    z.sleep( 1 )
                    d( text="个人资料").click( )
                    index = index + 1
                    z.heartbeat( )
                    num = 0
                    continue
                obj = d( text='发送' )  # 不需要验证可直接添加为好友的情况
                if obj.exists:
                    z.sleep( 2 )
                    while d( text='发送' ).exists :
                        d( text='发送' ).click( )
                    if d( text='添加失败，请勿频繁操作' ).exists:
                        z.heartbeat( )
                        z.toast( "频繁操作,跳出模块" )
                        print( "操作频繁3" )
                        return
                    else:
                        count = count + 1
                        print( "请求发送成功" )
                        index = index +1
                    num = 0
                    continue
                d.dump( compressed=False )
                obj = d( index=3, className="android.widget.EditText", resourceId="com.tencent.qqlite:id/0" ).info  # 将之前消息框的内容删除        需要发送验证信息
                obj = obj['text']
                lenth = len( obj )
                t = 0
                while t < lenth:
                    d.press.delete( )
                    t = t + 1
                time.sleep( 2 )
                z.input( message )
                z.sleep( 1 )
                # d(index=2,className="android.widget.CompoundButton",resourceId="com.tencent.qqlite:id/name").click()
                z.heartbeat( )
                d( text='下一步', resourceId='com.tencent.qqlite:id/ivTitleBtnRightText' ).click( )
                z.sleep( 1 )
                if d( text='发送' ).exists:
                    d( text='发送' ).click( )
                if d( text='添加失败，请勿频繁操作' ).exists:  # 操作过于频繁的情况
                    z.toast( "频繁操作,跳出模块" )
                    print( "操作频繁4" )
                    return
                while d(text="发送").exists:
                    for i in range(0,2):
                        if d(text="发送").exists:
                            d(text="发送").click()
                    if d(text="发送").exists:
                        z.toast("请求失败,停止模块")
                        return
                # print( QQnumber + "请求发送成功" )
                index = index +1
                num = 0
                z.heartbeat( )
                count = count + 1
                if count == EndIndex:
                    z.toast( "添加数量好友达到需求数量,停止模块" )
                    print( "添加数量达标" )
                    return
            else:
                obj2 = d( index=0, resourceId='com.tencent.qqlite:id/0' ).child(index=index,text="未启用通讯录的联系人" )
                if obj2.exists:
                    z.toast("模块完成")
                    print( "模块完成" )
                    return
                if unclick2:
                    index = index
                    unclick2 = False
                else:
                    index = index - 1
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                z.sleep( 2 )
                obj2  = d(index=0, resourceId='com.tencent.qqlite:id/0' ).child( className='android.widget.RelativeLayout',index=index ).child(index=0,className="android.widget.LinearLayout")
                if obj2.exists:
                    obj2.click( )
                    obj3 = d( index=1, resourceId="com.tencent.qqlite:id/info", className="android.widget.TextView" )
                    if obj3.exists:
                        obj3 = obj3.info["text"]
                        if obj3 not in listNum:
                            listNum.append( obj3 )
                        else:
                            z.toast( "已无好友可加,停止模块！" )
                            print( "无好友可加" )
                            return
                    index = 1
                    z.sleep( 1 )
                    d( text="个人资料" ).click( )
                continue

def getPluginClass():
    return QlAddFriendsByAddressList


if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id": "39", "time_delay": "3", "EndIndex": "8"}  # cate_id是仓库号，length是数量
    o.action(d, z, args)