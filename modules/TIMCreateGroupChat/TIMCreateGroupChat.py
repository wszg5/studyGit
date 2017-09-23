# coding:utf-8
from __future__ import division
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class TIMCreateGroupChat:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.toast( "TIM创建群聊" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM创建群聊" )
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
        d.server.adb.cmd( "shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        z.heartbeat( )
        if d( text="消息" ).exists:
            z.toast( "登录状态正常，继续执行" )
        else:
            z.toast( "登录状态异常，跳过此模块" )
            return
        z.heartbeat( )
        str1 = d.info  # 获取屏幕大小等信息
        height = str1["displayHeight"]
        width = str1["displayWidth"]
        totalNumber = int( args['totalNumber'] )  # 要给多少人发消息
        repo_address_id = args["repo_address_id"]
        while True:
            if d( index=1, className='android.widget.ImageView' ).exists:
                z.heartbeat( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,
                                                                            className="android.widget.RelativeLayout" ).click( )
            if d( text="加好友" ).exists:  # 由于网速慢或手机卡可能误点
                d( text="加好友" ).click( )
                z.heartbeat( )
                d( text="返回", className="android.widget.TextView" ).click( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,
                                                                            className="android.widget.RelativeLayout" ).click( )
            z.sleep( 3 )
            if d( text='邮件', resourceId='com.tencent.tim:id/name', className="android.widget.TextView" ).exists:
                z.heartbeat( )
                d( index=0, resourceId='com.tencent.tim:id/head', className="android.widget.ImageView" ).click( )
                break
        z.sleep( 5 )
        z.heartbeat( )
        obj = d(index=0,className="android.widget.LinearLayout").child(index=1,className="android.widget.LinearLayout").child(index=0,className="android.widget.TextView",resourceId="com.tencent.tim:id/info")
        if obj.exists:
            myAccount = obj.info["text"]      #获取自己的账号
            z.toast("获取自己的账号")
            z.sleep(2)
            z.heartbeat()
        else:
            z.toast("获取不到自己的账号")
            return
        while d(text="返回",resourceId="com.tencent.tim:id/ivTitleBtnLeft").exists:
            d( text="返回", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click()
            z.sleep(1)
            z.heartbeat()

        self.getIntoGroup(d,z)
        num = 0
        nameGender = args["name"]
        if nameGender=="男":
            nameGender = "M"
        elif nameGender=="女":
            nameGender = "W"
        else:
            nameGender = "B"
        n = 0
        repo_qq_id = args["repo_qq_id"]
        while n < totalNumber:
            if d( index=0, resourceId="com.tencent.tim:id/ivTitleBtnRightImage",
                  className="android.widget.ImageView" ).exists:
                z.sleep( 1 )
                z.heartbeat( )
                d( index=0, resourceId="com.tencent.tim:id/ivTitleBtnRightImage",
                   className="android.widget.ImageView" ).click( )
            if d( text="发起多人聊天" ).exists:
                d( text="发起多人聊天" ).click( )
                z.sleep( 1 )
                z.heartbeat( )
            while num<2:
                QQnumber = self.getFriends(z,repo_qq_id,myAccount)
                if not QQnumber:
                    return
                if d(text="搜索",className="android.widget.EditText").exists:
                    d( text="搜索", className="android.widget.EditText" ).click()
                    z.sleep(1)
                    z.input(QQnumber)
                    z.sleep(2)
                    if d( textContains="没有与", resourceId="com.tencent.tim:id/loading",
                          className="android.widget.TextView" ).exists:
                        z.toast( "该QQ号可能不是你的好友" )
                        self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "N", myAccount )
                        # i = i + 1
                        objText = d( index=0, className="android.widget.RelativeLayout" ).child(
                            className="android.widget.EditText" )
                        if objText.exists:
                            objText = objText.info["text"]
                            lenth = len( objText )
                            m = 0
                            while m < lenth:
                                d.press.delete( )
                                m = m + 1
                            continue
                    if d(text="已选择",className="android.widget.TextView").exists:
                        z.toast("已选择")
                        self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "Y", myAccount )
                        objText = d( index=0, className="android.widget.RelativeLayout" ).child(
                            className="android.widget.EditText" )
                        if objText.exists:
                            objText = objText.info["text"]
                            lenth = len( objText )
                            m = 0
                            while m < lenth:
                                d.press.delete( )
                                m = m + 1
                            continue

                    # obj = d( index=0, className="android.widget.AbsListView" ).child( index=1,className="android.widget.RelativeLayout",resourceId="com.tencent.tim:id/group_item_layout" )
                    obj = d(text="面对面发起多人聊天",className="android.widget.Button")
                    if obj.exists:
                        obj.click( )
                        z.sleep( 2 )
                        # if obj.exists:
                        #     obj.click( )
                        z.heartbeat( )
                        self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "Y", myAccount )
                        num = num + 1

            if d(textContains="发起",resourceId="com.tencent.tim:id/ivTitleBtnRightText").exists:
                z.heartbeat()
                d( textContains="发起",resourceId="com.tencent.tim:id/ivTitleBtnRightText").click()
                z.sleep(3)
                z.heartbeat()
                if d( textContains="发起" ).exists:
                    z.toast("创建不了群聊了,停止模块")
                    return
                n = n + 1
                num = 0
            if d(resourceId="com.tencent.tim:id/ivTitleBtnRightImage",description="聊天设置").exists:
                d( resourceId="com.tencent.tim:id/ivTitleBtnRightImage", description="聊天设置" ).click()
                z.sleep(2)
                z.heartbeat()
            if d(text="多人聊天名称",className="android.widget.TextView").exists:
                d( text="多人聊天名称", className="android.widget.TextView" ).click()
                z.sleep(1)
            name = nameGender + str( n )
            z.input( name )
            z.sleep( 1 )
            if d(text="完成").exists:
                d( text="完成" ).click()
                z.sleep(3)
                z.heartbeat()
                if d( text="完成" ).exists:
                    z.toast("操作频繁")
                    return
            if d(text="分享多人聊天",className="android.widget.TextView").exists:
                d( text="分享多人聊天", className="android.widget.TextView" ).click()
                z.sleep(1)
                z.heartbeat()
            else:
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                z.sleep(2)
                if d( text="分享多人聊天", className="android.widget.TextView" ).exists:
                    d( text="分享多人聊天", className="android.widget.TextView" ).click( )
                    z.sleep( 1 )
                    z.heartbeat( )
                else:
                    z.toast("没有分享多人聊天")

            if d(text="复制链接",className="android.widget.TextView").exists:
                d( text="复制链接", className="android.widget.TextView" ).click()
                z.sleep(1)
                z.heartbeat()

            if d(text="返回",resourceId="com.tencent.tim:id/ivTitleBtnLeft").exists:
                d( text="返回", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click()
                z.sleep(1)

            obj = d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).left( index=0,resourceId="com.tencent.tim:id/input",className="android.widget.EditText" )
            if obj.exists:
                obj.click( )
                z.sleep( 1 )
                obj.long_click( )
                z.sleep( 1 )
                d.click( 79/540 * width, 695/888 * height)
                z.sleep(1)
                z.heartbeat()
            if d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).exists:
                d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).click()
                z.sleep(1)
            d.dump( compressed=False )
            obj = d( index=2, className="android.widget.RelativeLayout" ).child( index=1,className="android.widget.TextView",resourceId="com.tencent.tim:id/chat_item_content_layout" )
            if obj.exists:
                obj = obj.info["text"]
                obj = obj.encode( 'utf-8' )
                print( obj )
                obj = obj.split( ":" )
                text = ""
                for i in range( 1, len( obj ) ):
                    text += obj[i]
                    text +=":"
                text = text[:-1]
                print( text )
                z.sleep( 1 )
                nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" )
                para = {"phoneNumber": text, 'x_01': name, 'x_02': myAccount,
                        'x_03': "0",'x_04': "", 'x_05': '3', 'x_06': ''}
                self.repo.PostInformation( repo_address_id, para )
                z.sleep( 1 )
            if n > totalNumber:
                break
            while d( resourceId="com.tencent.tim:id/ivTitleBtnLeft", textContains="消息" ).exists:
                d( resourceId="com.tencent.tim:id/ivTitleBtnLeft", textContains="消息" ).click( )
                z.sleep( 1 )
                z.heartbeat( )
            self.getIntoGroup(d,z)
        z.toast("模块完成")
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

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


    def getFriends(self,z,repo_qq_id,myAccount):
        qq = self.repo.GetNumber( repo_qq_id, 60, 1, "normal", "NO", None,
                                  myAccount.encode( 'utf-8' ) )  # 取出t1条两小时内没有用过的号码
        if len( qq ) == 0:
            # d.server.adb.cmd( "shell","am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库为空，等待中\"" % repo_qq_id ).communicate( )
            z.toast("仓库中本账号取不出数据了")
            return False
        # list = numbers  # 将取出的号码保存到一个新的集合
        # print( list )
        # z.sleep(15)
        z.sleep(1)
        z.heartbeat( )
        QQnumber = qq[0]['number']
        print( QQnumber )
        return QQnumber



def getPluginClass():
    return TIMCreateGroupChat

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT524SK00685")
    z = ZDevice("HT524SK00685")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_qq_id":"246","totalNumber":"3","time_delay":"3","name":"男","repo_address_id":"253"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)
    # z.cmd( "shell",'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"' % "http://url.cn/58E2Yuz#flyticket" )
    # Repo().uploadPhoneNumber( "448856030", 188 )
    # d.server.adb.cmd( "shell",
    #                   'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=wpa\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"' % "QQ" )
    # d.server.adb.cmd( "shell",'am start -a android.intent.action.VIEW -d "http://url.cn/58E2Yuz#flyticket"')
    # z.sleep(1)