# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class MobilqqPullGroupFriends:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.toast( "QQ指定群拉群成员" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ指定群拉群成员" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.mobileqq" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        z.heartbeat( )
        if d( text="消息" ).exists:
            z.toast( "登录状态正常，继续执行" )
        else:
            z.toast( "登录状态异常，跳过此模块" )
            return
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
        if d(textContains='匹配').exists:
            d.press.back()
        z.heartbeat( )
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        totalNumber = int( args['totalNumber'] )  # 要给多少人发消息

        while True:                          #由于网速慢或手机卡可能误点
            z.heartbeat( )
            if d(index=1,className="android.widget.RelativeLayout").child( index=0, className='android.widget.Button',description="帐户及设置" ).exists:  # 点击ＱＱ头像.exists:
                z.sleep(1)
                z.heartbeat()
                d(index=1,className="android.widget.RelativeLayout").child( index=0, className='android.widget.Button',description="帐户及设置" ).click()
                z.heartbeat( )
                # d( resourceId="com.tencent.mobileqq:id/name", index=0,className='android.widget.RelativeLayout' ).child(
                #     index=0, className='android.widget.FrameLayout').child(resourceId="com.tencent.mobileqq:id/head", index=1,className='android.widget.ImageView').click( )  # 点击ＱＱ头像
                z.heartbeat( )
            if d( index=1, resourceId='com.tencent.mobileqq:id/head', className='android.widget.ImageView' ).exists:
                d( index=1, resourceId='com.tencent.mobileqq:id/head', className='android.widget.ImageView' ).click( )
                z.sleep(2)
                z.heartbeat()
                break
            if d(text="加好友").exists:    #由于网速慢或手机卡可能误点
                d(text="加好友").click()
                d(text="返回",className="android.widget.TextView").click()
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,className="android.widget.RelativeLayout" ).click( )
            z.sleep( 3 )

        objText =  d(index=0,className="android.widget.LinearLayout").child(index=0,className="android.widget.LinearLayout").child(index=1,className="android.widget.TextView",resourceId="com.tencent.mobileqq:id/info")
        if objText.exists:
            myAccount = objText.info["text"]
            z.toast( "获取自己的账号" )
            z.sleep( 2 )
            z.heartbeat( )
        else:
            z.toast( "获取不到自己的账号" )
            return

        repo_appoint_group_id = int( args["repo_appoint_group_id"] )  # 得到取号码的仓库号
        numbers = self.repo.GetNumber( repo_appoint_group_id, 60, 1000, "normal", "NO")  # 取出t1条两小时内没有用过的号码
        if len( numbers ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库中为空，等待中\"" % repo_appoint_group_id ).communicate( )
            z.sleep( 10 )
            return
        list = numbers  # 将取出的号码保存到一个新的集合
        # print( list )
        # z.sleep(15)
        num = random.randint( 0, len( list ) - 1 )
        group = list[num]['number']
        print( group )
        z.sleep( 2 )
        z.heartbeat( )
        z.toast( "准备唤醒的群号为" + group )
        d.server.adb.cmd( "shell",'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=group&source=qrcode"' % group )  # 群页面
        z.sleep( 2 )
        z.heartbeat( )
        if d( text='QQ' ).exists:
            d( text='QQ' ).click( )
            time.sleep( 0.5 )
            while d( text='仅此一次' ).exists:
                d( text='仅此一次' ).click( )
        n = 0
        flag = False
        while (not d( text="发消息", className="android.widget.Button" ).exists and not d( text='申请加群' ).exists) or d( text="编辑资料",className="android.widget.Button" ).exists:
            z.toast( "准备唤醒的群号为" + group )
            d.server.adb.cmd( "shell",'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=group&source=qrcode"' % group )  # 群页面
            z.heartbeat( )
            z.sleep( 2 )
            if d( text='QQ' ).exists:
                d( text='QQ' ).click( )
                time.sleep( 0.5 )
                while d( text='仅此一次' ).exists:
                    d( text='仅此一次' ).click( )
                break
            if (not d( text="发消息", className="android.widget.Button" ).exists and not d( text='申请加群' ).exists) or d( text="编辑资料",className="android.widget.Button" ).exists:
                if n == 4:
                    z.toast( "唤醒不出来" )
                    flag = True
                    break
                else:
                    n = n + 1
            else:
                if d( text='QQ' ).exists:
                    d( text='QQ' ).click( )
                    time.sleep( 0.5 )
                    while d( text='仅此一次' ).exists:
                        d( text='仅此一次' ).click( )
                break
        if flag:
            z.sleep( 1 )
            return

        flag2 = False
        if d(text="申请加群").exists:
            d(text="申请加群").click()
            z.sleep(3)
            z.heartbeat()
            if d(text="申请加群").exists:
                z.toast("该群无法加入,停止模块")
                self.repo.savePhonenumberXM( group, repo_appoint_group_id, "N" )
                return
            if d( text='发送' ,className="android.widget.TextView").exists:
                d( text='发送' ,className="android.widget.TextView").click( )
                z.sleep(4)
                if d( text='发送',className="android.widget.TextView" ).exists:
                    z.toast( "该群无法加入,停止模块" )
                    self.repo.savePhonenumberXM( group, repo_appoint_group_id, "N" )
            z.heartbeat( )

        if d(resourceId="com.tencent.mobileqq:id/ivTitleBtnRightImage",description="群资料卡").exists:
            d( resourceId="com.tencent.mobileqq:id/ivTitleBtnRightImage", description="群资料卡" ).click()
            z.sleep(2)
            z.heartbeat()
        elif d( text="发消息", className="android.widget.Button" ).exists:
            pass
        else:
            z.toast( "准备唤醒的群号为" + group )
            d.server.adb.cmd( "shell",
                              'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=group&source=qrcode"' % group )  # 群页面
            z.sleep( 2 )
            z.heartbeat( )
            if d( text='QQ' ).exists:
                d( text='QQ' ).click( )
                time.sleep( 0.5 )
                while d( text='仅此一次' ).exists:
                    d( text='仅此一次' ).click( )
            n = 0
            flag = False
            while (not d( text="发消息", className="android.widget.Button" ).exists and not d( text='申请加群' ).exists) :
                z.toast( "准备唤醒的群号为" + group )
                d.server.adb.cmd( "shell",
                                  'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=group&source=qrcode"' % group )  # 群页面
                z.heartbeat( )
                z.sleep( 2 )
                if d( text='QQ' ).exists:
                    d( text='QQ' ).click( )
                    time.sleep( 0.5 )
                    while d( text='仅此一次' ).exists:
                        d( text='仅此一次' ).click( )
                    break
                if (not d( text="发消息", className="android.widget.Button" ).exists and not d( text='申请加群' ).exists):
                    if n == 4:
                        z.toast( "唤醒不出来" )
                        flag = True
                        break
                    else:
                        n = n + 1
                else:
                    if d( text='QQ' ).exists:
                        d( text='QQ' ).click( )
                        time.sleep( 0.5 )
                        while d( text='仅此一次' ).exists:
                            d( text='仅此一次' ).click( )
                    break
            if flag:
                z.sleep( 1 )
                return
        if d(text="申请加群").exists:
            z.toast("还没有加入该群,请等待")
            return

        obj = d(description="邀请新成员",className="android.widget.ImageView")
        if obj.exists:
            # d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
            # z.sleep(1)
            obj.click( )
            z.sleep( 2 )
            z.heartbeat( )
        else:
            d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
            z.sleep( 2 )
            if obj.exists:
                obj = obj.click( )
                z.sleep( 2 )
            else:
                z.toast( "该群无法邀请好友" )
                self.repo.savePhonenumberXM( group, repo_appoint_group_id, "N" )

        count = int(self.pullFriends(d,z,args,myAccount,totalNumber))
        if count>=totalNumber:
            z.toast("模块完成")
            return
        totalNumber = totalNumber - count
        count = 0
        while count<totalNumber:
            count = self.pullFriends( d, z, args, myAccount, totalNumber )
            totalNumber = totalNumber - count
            count = 0
        z.sleep(1)

        z.toast("模块完成")
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

    def pullFriends(self, d,z, args,myAccount,totalNumber):
        count = 0
        repo_group_id = int( args["repo_group_id"] )
        groupNumber = self.getGroupNumber( args, myAccount )
        while count<10:
            # obj = d(index=3,className="android.widget.LinearLayout").child(description='邀请新成员',className="android.widget.ImageView")

            repo_qq_id = int( args["repo_qq_id"] )  # 得到取号码的仓库号
            qq = self.repo.GetNumber( repo_qq_id, 60, 1, "normal", "NO", groupNumber )  # 取出t1条两小时内没有用过的号码
            if len( qq ) == 0:
                # d.server.adb.cmd( "shell",
                #                   "am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库账号为%s没有数据可以再取出来，等待中\"" % repo_qq_id,myAccount.encode( 'utf-8' ) ).communicate( )
                z.toast("该群已经没有数据可取出来了")
                if count == 0:
                    # z.sleep( 10 )
                    self.repo.savePhonenumberXM( groupNumber, repo_qq_id, "N", myAccount )
                    z.sleep(1)
                    z.heartbeat()
                    groupNumber = self.getGroupNumber( args, myAccount )
                    qq = self.repo.GetNumber( repo_qq_id, 60, 1, "normal", "NO", groupNumber )  # 取出t1条两小时内没有用过的号码
                    if len( qq ) == 0:
                        z.toast( "该群已经没有数据可取出来了" )
                        return

                    return
                else:
                    # z.toast("仓库中该群已经没有未被拉过的的群成员")
                    break
            # list = numbers  # 将取出的号码保存到一个新的集合# print( list )
            # z.sleep(15)
            z.sleep( 1 )
            z.heartbeat( )
            QQnumber = qq[0]['number']
            print( QQnumber )

            if d(text="从群聊中选择",className="android.widget.Button").exists:
                d( text="从群聊中选择", className="android.widget.Button" ).click()
                z.sleep(2)
                z.heartbeat()
            if d( text="搜索", className="android.widget.EditText" ).exists and d(text="返回",resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").exists:
                d( text="搜索", className="android.widget.EditText" ).click( )
                z.sleep( 2 )
                z.heartbeat( )
                z.input( groupNumber )
                z.sleep( 2 )
                if d( textContains="没有与", resourceId="com.tencent.mobileqq:id/loading",
                      className="android.widget.TextView" ).exists:
                    z.toast( "该QQ号可能不是你的好友" )
                    self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "N", groupNumber )
                    objText = d( index=0, className="android.widget.RelativeLayout" ).child(
                        className="android.widget.EditText" )
                    if objText.exists:
                        objText = objText.info["text"]
                        lenth = len( objText )
                        m = 0
                        while m < lenth:
                            d.press.delete( )
                            m = m + 1
                    # i = i + 1
                    continue
                if d(text="我的群",className="android.widget.TextView").exists:
                    d( text="我的群", className="android.widget.TextView" ).click()
                    z.sleep(2)
                    z.heartbeat()

            if d( text="搜索", className="android.widget.EditText" ).exists and d(text="群",resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").exists:
                d( text="搜索", className="android.widget.EditText" ).click( )
                z.sleep( 2 )
                z.heartbeat( )
                z.input( QQnumber )
                z.sleep( 2 )

                breakA = False
                while d( text="已加入", className="android.widget.TextView" ).exists or d(text="已选择",className="android.widget.TextView").exists:
                    z.toast( "该好友已加入该群或已选择" )
                    self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "Y", groupNumber )
                    objText = d( index=0, className="android.widget.RelativeLayout" ).child(className="android.widget.EditText" )
                    if objText.exists:
                        objText = objText.info["text"]
                        lenth = len( objText )
                        m = 0
                        while m < lenth:
                            d.press.delete( )
                            m = m + 1
                    breakA = True
                    z.sleep( 1 )
                    break
                if breakA:
                    # i = i + 1
                    self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "Y", groupNumber )
                    continue
            # d.dump( compressed=False )
            if d( textContains="没有与", resourceId="com.tencent.mobileqq:id/loading",
                  className="android.widget.TextView" ).exists:
                z.toast( "该群号可能不是你的群" )
                self.repo.savePhonenumberXM( groupNumber, repo_qq_id, "N", myAccount )
                # i = i + 1
                groupNumber = self.getGroupNumber(args,myAccount)
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
            # obj = d( index=0, className="android.widget.AbsListView" ).child( index=1,
            #                                                                   className="android.widget.RelativeLayout",
            #                                                                   resourceId="com.tencent.tim:id/group_item_layout" )
            obj = d( text="群成员",className="android.widget.TextView" )
            if obj.exists:
                obj.click( )
                z.sleep( 2 )
                z.heartbeat( )
                # if obj.exists:
                #     z.toast("已达上线")
                #     z.sleep( 2 )
                #     z.heartbeat( )
                #     break
                self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "Y", groupNumber )
                count = count + 1
                if count >= totalNumber:
                    break
            else:
                z.toast( "该QQ号可能不是你的群中的群成员了" )
                self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "N", groupNumber )
                # i = i + 1
                continue
        if d( textContains="完成", resourceId="com.tencent.mobileqq:id/ivTitleBtnRightText" ).exists:
            d( textContains="完成", resourceId="com.tencent.mobileqq:id/ivTitleBtnRightText" ).click( )
            z.sleep( 3 )
            z.heartbeat( )
            if d( textContains="完成", resourceId="com.tencent.mobileqq:id/ivTitleBtnRightText" ).exists:
                z.toast( "无法拉好友入群聊,停止模块" )
                self.repo.savePhonenumberXM( groupNumber, repo_group_id, "N", myAccount )
                return
            self.repo.savePhonenumberXM( groupNumber, repo_group_id, "Y", myAccount )
            z.sleep( 1 )
            z.heartbeat( )
            return count

    def getGroupNumber(self,args,myAccount):
        repo_group_id = int( args["repo_group_id"] )  # 得到取号码的仓库号
        group = self.repo.GetNumber( repo_group_id, 60, 1, "normal", "NO",
                                     myAccount.encode( 'utf-8' ) )  # 取出t1条两小时内没有用过的号码
        if len( group ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库账号为%s没有数据可以再取出来，等待中\"" % repo_group_id,
                              myAccount.encode( 'utf-8' ) ).communicate( )
            # if x == 0:
            #     z.sleep( 10 )
            #     return
            # else:
            #     z.toast( "仓库中该账户已经没有未被拉过的的好友" )
        # list = numbers  # 将取出的号码保存到一个新的集合
        # print( list )
        # z.sleep(15)
        z.sleep( 1 )
        z.heartbeat( )
        groupNumber = group[0]['number']
        print( groupNumber )
        return groupNumber
def getPluginClass():
    return MobilqqPullGroupFriends

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_qq_id":"235","repo_group_id":"233","repo_appoint_group_id":"239","totalNumber":"25","time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)
