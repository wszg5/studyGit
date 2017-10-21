# coding:utf-8
from __future__ import division
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class TIMCheckGroupGroupChat:
    def __init__(self):
        self.repo = Repo()

    def getTimeSecond(self, thisTime):
        thistimeD = int( thisTime[6:8] )
        thistimeH = int( thisTime[8:10] )
        thistimeM = int( thisTime[10:12] )
        thistimeS = int( thisTime[12:] )
        second = thistimeD * 24 * 60 * 60 + thistimeH * 60 * 60 + thistimeM * 60 + thistimeS
        return second

    def action(self, d,z, args):
        z.toast( "TIM检存群聊" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM检存群聊" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        z.heartbeat( )
        if d( text="消息", resourceId="com.tencent.tim:id/ivTitleName" ).exists:
            z.toast( "登录状态正常，继续执行" )
        else:
            if d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).exists:
                d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).click( )
                z.sleep( 1 )
            elif d( text="消息", className="android.widget.TextView" ).exists and d( text="马上绑定",className="android.widget.Button" ).exists:
                d( text="消息", className="android.widget.TextView" ).click( )
                z.sleep( 1 )
            elif d( text="返回" ).exists:
                d( text="返回" ).click( )
                z.sleep( 1 )

            else:
                z.toast( "登录状态异常，跳过此模块" )
                return
        while True:
            if d( index=1, className='android.widget.ImageView' ).exists:
                z.heartbeat( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,className="android.widget.RelativeLayout" ).click( )
                z.sleep(2)
            # # if d( text="加好友" ).exists:  # 由于网速慢或手机卡可能误点
            # #     d( text="加好友" ).click( )
            # #     z.heartbeat( )
            #     d( text="返回", className="android.widget.TextView" ).click( )
            #     d( index=2, className="android.widget.FrameLayout" ).child( index=0,
            #                                                                 className="android.widget.RelativeLayout" ).click( )
            # z.sleep( 3 )
            if d( text='邮件', resourceId='com.tencent.tim:id/name', className="android.widget.TextView" ).exists:
                z.heartbeat( )
                d( index=0, resourceId='com.tencent.tim:id/head', className="android.widget.ImageView" ).click( )
                break
        z.sleep(5)
        z.heartbeat()
        for num in range(0,6):
            obj = d(index=0,className="android.widget.LinearLayout").child(index=1,className="android.widget.LinearLayout").child(index=0,className="android.widget.TextView",resourceId="com.tencent.tim:id/info")
            if obj.exists:
                myAccount = obj.info["text"]      #获取自己的账号
                z.toast("获取自己的账号")
                z.sleep(2)
                z.heartbeat()
                while d( text="返回", className="android.widget.TextView" ).exists:
                    d( text="返回", className="android.widget.TextView" ).click( )
                break
            else:
                z.toast("获取不到自己的账号再试一次")
                z.sleep(2)
                d.dump( compressed=False )
                while d(text="返回",className="android.widget.TextView").exists:
                    d( text="返回", className="android.widget.TextView" ).click()
                if d( index=0, resourceId='com.tencent.tim:id/head', className="android.widget.ImageView" ).exists:
                    d( index=0, resourceId='com.tencent.tim:id/head', className="android.widget.ImageView" ).click( )

        else:
            z.toast("都尝试6次,真的获取获取不到自己的账号,停止模块")
            return
        #
        #
        self.getIntoGroup(d,z)
        Str = d.info  # 获取屏幕大小等信息
        height = Str["displayHeight"]
        width = Str["displayWidth"]
        repo_info_id = args["repo_info_id"]
        x = 0
        y = 0
        group_name = "aaa"
        addressList = []
        if not d(index = 0,resourceId="com.tencent.tim:id/lv_discussion").child(index=1,className="android.widget.RelativeLayout").child(index=1,className="android.widget.TextView").exists:
            z.toast("没有群聊,停止模块")
            return
        # else:
        #     obj = d(index = 0,resourceId="com.tencent.tim:id/lv_discussion").child(index=1,className="android.widget.RelativeLayout").info["bounds"]
        #     top = obj["top"]
        #     left = obj["left"]
        #     right = obj["right"]
        #     bottom = obj["bottom"]
            # x = (394 - 271) / 540
        while True:
            # if d(className="android.widget.RelativeLayout",description="搜索聊天或者联系人").exists:
            #     x = 1
            n = 0
            obj = d( index=0, resourceId="com.tencent.tim:id/lv_discussion" ).child( index=x,
                                                                                     className="android.widget.RelativeLayout" ).child(
                index=1, className="android.widget.TextView" )
            obj2 = d( index=0, resourceId="com.tencent.tim:id/lv_discussion" ).child( index=x,
                                                                                      className="android.widget.RelativeLayout" ).child(
                index=2, resourceId="com.tencent.tim:id/text2" )
            if obj.exists:
                objInfo = obj.info["text"].encode( 'utf-8' )
                if objInfo == "搜索":
                    x = x + 1
                    continue
                if obj2.exists:
                    peopleCount = obj2.info["text"].encode( 'utf-8' )
                    peopleCount = peopleCount[1:][:-1]
                obj.click( )
                z.sleep( 1 )
                z.heartbeat( )
                if d( textContains="点击链接加入多人聊天" ).exists:
                    obj = d( textContains="点击链接加入多人聊天" ).info["text"]
                    obj = obj.encode( 'utf-8' )
                    print(obj)
                    obj = obj.split( ":" )
                    text = ""
                    for i in range( 1, len( obj ) ):
                        text += obj[i]
                        text += ":"
                    text = text[1:][:-1]
                    print(text)
                else:
                    if d( resourceId="com.tencent.tim:id/ivTitleBtnRightImage", description="聊天设置" ).exists:
                        d( resourceId="com.tencent.tim:id/ivTitleBtnRightImage", description="聊天设置" ).click( )
                        z.sleep( 2 )
                        z.heartbeat( )
                        if d( text="分享多人聊天", className="android.widget.TextView" ).exists:
                            d( text="分享多人聊天", className="android.widget.TextView" ).click( )
                            z.sleep( 1 )
                            z.heartbeat( )
                        else:

                            while not d( text="分享多人聊天", className="android.widget.TextView" ).exists:
                                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                                z.sleep(1.5)
                                d.dump( compressed=False )
                            z.sleep( 2 )
                            if d( text="分享多人聊天", className="android.widget.TextView" ).exists:
                                d( text="分享多人聊天", className="android.widget.TextView" ).click( )
                                z.sleep( 1 )
                                z.heartbeat( )
                            else:
                                z.toast( "没有分享多人聊天" )
                                x = x + 1
                                continue

                        if d( text="复制链接", className="android.widget.TextView" ).exists:
                            d( text="复制链接", className="android.widget.TextView" ).click( )
                            z.sleep( 3 )
                            z.heartbeat( )

                        if d( text="返回", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).exists:
                            d( text="返回", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click( )
                            z.sleep( 1 )

                        obj = d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).left( index=0,
                                                                                            resourceId="com.tencent.tim:id/input",
                                                                                            className="android.widget.EditText" )
                        if obj.exists:
                            obj.click( )
                            z.sleep( 1 )
                            obj.long_click( )
                            z.sleep( 1 )
                            d.click( 66 / 720 * width, 1084 / 1280 * height )
                            d.dump( compressed=False )
                            obj2 = obj.info["text"].encode( 'utf-8' )
                            if obj2 == "":
                                z.sleep( 1 )
                                obj.long_click( )
                                z.sleep( 1 )
                                d.click( 79 / 540 * width, 695 / 888 * height )
                            z.sleep( 1 )
                            z.heartbeat( )
                        if d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).exists:
                            d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).click( )
                            z.sleep( 1 )
                        d.dump( compressed=False )
                        if d( textContains="点击链接加入多人聊天" ).exists:
                            obj = d( textContains="点击链接加入多人聊天" ).info["text"]
                            obj = obj.encode( 'utf-8' )
                            print(obj)
                            obj = obj.split( ":" )
                            text = ""
                            for i in range( 1, len( obj ) ):
                                text += obj[i]
                                text += ":"
                            text = text[1:][:-1]
                            print(text)
                if text not in addressList:
                    addressList.append( text )
                para = {"phoneNumber": text, 'x_01': myAccount, 'x_02': objInfo, 'x_03': "0", 'x_05': peopleCount,
                        'x_06': 'normal'}
                Repo( ).PostInformation( repo_info_id, para )
                z.toast( "已获得群聊地址" )
                x = x + 1
                while d( resourceId="com.tencent.tim:id/ivTitleBtnLeft", textContains="消息" ).exists:
                    d( resourceId="com.tencent.tim:id/ivTitleBtnLeft", textContains="消息" ).click( )
                    z.sleep( 1 )
                    z.heartbeat( )
                self.getIntoGroup( d, z )
                while n < y:
                    d.swipe( (right - left) / 2, (bottom - top) / 2 + top, (right - left) / 2,(bottom - top) / 2 + top - (bottom - top) * 8 )
                    z.sleep(1)
                    n = n + 1

            else:
                obj = d( index=0, resourceId="com.tencent.tim:id/lv_discussion" ).child( index=x - 2,
                                                                                         className="android.widget.RelativeLayout" ).child(
                    index=1, className="android.widget.TextView" )
                if obj.exists:
                    obj = d( index=0, resourceId="com.tencent.tim:id/lv_discussion" ).child( index=x - 2,
                                                                                             className="android.widget.RelativeLayout" ).info[
                        "bounds"]
                    top = obj["top"]
                    left = obj["left"]
                    right = obj["right"]
                    bottom = obj["bottom"]
                    d.swipe( (right - left) / 2, (bottom - top) / 2 + top, (right - left) / 2,
                             (bottom - top) / 2 + top - (bottom - top) * 8 )
                    z.sleep(1.5)
                    y = y + 1
                    # d.dump( compressed=False )
                    if d( index=0, resourceId="com.tencent.tim:id/lv_discussion" ).child( index=x - 1,
                                                                                          className="android.widget.RelativeLayout" ).child(
                        index=1, className="android.widget.TextView" ).exists:
                        d( index=0, resourceId="com.tencent.tim:id/lv_discussion" ).child( index=x - 1,
                                                                                           className="android.widget.RelativeLayout" ).child(
                            index=1, className="android.widget.TextView" ).click( )
                        z.sleep( 1 )
                        z.heartbeat( )
                        if d( textContains="点击链接加入多人聊天" ).exists:
                            obj = d( textContains="点击链接加入多人聊天" ).info["text"]
                            obj = obj.encode( 'utf-8' )
                            print(obj)
                            obj = obj.split( ":" )
                            text = ""
                            for i in range( 1, len( obj ) ):
                                text += obj[i]
                                text += ":"
                            text = text[1:][:-1]
                            print(text)
                            if text in addressList:
                                z.toast("检存完毕")
                                break
                    else:
                        if d( index=0, resourceId="com.tencent.tim:id/lv_discussion" ).child( index=x - 2,
                                                                                              className="android.widget.RelativeLayout" ).child(
                            index=1, className="android.widget.TextView" ).exists:
                            d( index=0, resourceId="com.tencent.tim:id/lv_discussion" ).child( index=x - 2,
                                                                                               className="android.widget.RelativeLayout" ).child(
                                index=1, className="android.widget.TextView" ).click( )
                        z.sleep( 1 )
                        z.heartbeat( )
                        if d( textContains="点击链接加入多人聊天" ).exists:
                            obj = d( textContains="点击链接加入多人聊天" ).info["text"]
                            obj = obj.encode( 'utf-8' )
                            print(obj)
                            obj = obj.split( ":" )
                            text = ""
                            for i in range( 1, len( obj ) ):
                                text += obj[i]
                                text += ":"
                            text = text[1:][:-1]
                            print(text)
                            if text in addressList:
                                z.toast( "检存完毕" )
                                break
                    x = 1
                    while d( resourceId="com.tencent.tim:id/ivTitleBtnLeft", textContains="消息" ).exists:
                        d( resourceId="com.tencent.tim:id/ivTitleBtnLeft", textContains="消息" ).click( )
                        z.sleep( 1 )
                        z.heartbeat( )
                    self.getIntoGroup( d, z )
                    while n < y:
                        d.swipe( (right - left) / 2, (bottom - top) / 2 + top, (right - left) / 2,
                                 (bottom - top) / 2 + top - (bottom - top) * 8 )
                        z.sleep(1)
                        n = n + 1
                z.sleep( 1 )
        z.toast( "模块完成" )

    def getIntoGroup(self,d,z):
        while True:
            if d( index=1, className='android.widget.ImageView' ).exists:
                z.heartbeat( )
                d( index=1, className="android.widget.FrameLayout" ).child( index=0,
                                                                            className="android.widget.RelativeLayout" ).click( )
            if d( text="加好友" ).exists:  # 由于网速慢或手机卡可能误点
                d( text="加好友" ).click( )
                z.heartbeat( )
                d( text="返回", className="android.widget.TextView" ).click( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,
                                                                            className="android.widget.RelativeLayout" ).click( )
            z.sleep( 3 )
            if d(index=1, description='群和多人聊天 按钮', resourceId='com.tencent.tim:id/name', className="android.widget.RelativeLayout" ).exists:
                z.heartbeat( )
                d( index=1, description='群和多人聊天 按钮', resourceId='com.tencent.tim:id/name',
                   className="android.widget.RelativeLayout" ).click( )
                z.sleep(2)
                z.heartbeat()
                break

        if d(text="多人聊天",className="android.widget.TextView").exists:
            d( text="多人聊天", className="android.widget.TextView" ).click()
            z.sleep(1)
            z.heartbeat()

def getPluginClass():
    return TIMCheckGroupGroupChat

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("cda0ae8d")
    z = ZDevice("cda0ae8d")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_info_id":"260","time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)
    # if len( totalList ) == 0:
    #     z.toast( "%s仓库%s账号可数据为空" % (repo_group_id, myAccount) )
    # address = totalList[0]["x02"][1:]
    # address = address.encode( 'utf-8' )
    # print( address )
    # # d.server.adb.cmd( "shell", "am start -a android.intent.action.VIEW -d 'http://url.cn/58E2Yuz#flyticket'" )
    # z.sleep(1)
    # print("am start -a android.intent.action.VIEW -d '%s'" %address)
    # d.server.adb.cmd( "shell", "am start -a android.intent.action.VIEW -d 'http://url.cn/5Br4GP2#flyticket'" )
    # z.sleep( 1 )
    # para = {"phoneNumber": "www.baidu.com", 'x_01': "444455552", 'x_02': "MX", 'x_03': "0",
    #         'x_06': 'normal', 'x_20': "4455886644"}
    # Repo().PostInformation( "256", para )
    # z.sleep(1)
    # Str = d.info  # 获取屏幕大小等信息
    # height = Str["displayHeight"]
    # width = Str["displayWidth"]
    # repo_info_id = args["repo_info_id"]
    # x = 10
    # y = 0
    # myAccount = "448856030"
    # group_name = "aaa"
    # addressList = []



