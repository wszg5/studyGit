# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class TIMAppointGroupPullFriends:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.toast( "TIM指定群拉好友" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM指定群拉好友" )
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
        z.sleep(5)
        z.heartbeat()
        for num in range(0,6):
            obj = d(index=0,className="android.widget.LinearLayout").child(index=1,className="android.widget.LinearLayout").child(index=0,className="android.widget.TextView",resourceId="com.tencent.tim:id/info")
            if obj.exists:
                myAccount = obj.info["text"]      #获取自己的账号
                z.toast("获取自己的账号")
                z.sleep(2)
                z.heartbeat()
                break
            else:
                z.toast("获取不到自己的账号再试一次")
                z.sleep(2)
                d.dump( compressed=False )
                while d( text="返回", className="android.widget.TextView" ).exists:
                    d( text="返回", className="android.widget.TextView" ).click( )
                if d( index=0, resourceId='com.tencent.tim:id/head', className="android.widget.ImageView" ).exists:
                    d( index=0, resourceId='com.tencent.tim:id/head', className="android.widget.ImageView" ).click( )

        else:
            z.toast("都尝试6次,真的获取获取不到自己的账号,停止模块")
            return
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        totalNumber = int(args['totalNumber'])  # 要给多少人发消息

        repo_group_id = int( args["repo_group_id"] )  # 得到取号码的仓库号
        numbers = self.repo.GetNumber( repo_group_id, 0, 100, "normal", "NO" )  # 取出t1条两小时内没有用过的号码
        if len( numbers ) == 0:
            d.server.adb.cmd( "shell","am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库中该账号对应的数据取完，等待中\"" % repo_group_id ).communicate( )
            z.sleep( 10 )
            return
        list = numbers  # 将取出的号码保存到一个新的集合
        # print( list )
        # z.sleep(15)
        num = random.randint(0,len(list)-1)
        group = list[num]['number']
        print(group)
        z.sleep(3)
        z.heartbeat()

        while d(text="返回",resourceId="com.tencent.tim:id/ivTitleBtnLeft").exists:
            d( text="返回", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click()
            z.sleep(1)
            z.heartbeat()
        flag2 = False
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
                d( text="添加",className="com.tencent.tim:id/ivTitleBtnRightText" ).click( )
                z.sleep(2)
                z.heartbeat()
                break
        if d(text="我的群",className="android.widget.TextView").exists:
            d( text="多人聊天", className="android.widget.TextView" ).click()
            z.sleep(1)
            z.heartbeat()
        if d(text="QQ号/手机号/群").exists:
            d( text="QQ号/手机号/群" ).click()
            z.sleep(1)
            z.heartbeat()
            z.input(group)
            z.sleep(1)
            z.heartbeat()
        if d(text="找群:",className="android.widget.TextView").exists:
            d( text="找群:", className="android.widget.TextView" ).click()
            z.sleep(2)
            z.heartbeat()

        if d( text='申请加群' ).exists:
            d( text='申请加群' ).click( )
            z.sleep( 2 )
            flag2 = True
            if d( text='申请加群' ).exists:
                # i = i +1
                z.toast( "无法加群" )
                # self.repo.savePhonenumberXM( group, repo_group_id, "N" )
                return
            z.sleep( 2 )
            if d( text='发送',className="android.widget.TextView").exists:
                d( text='发送',className="android.widget.TextView").click( )
                z.sleep( 3 )
                if d( text='发送',className="android.widget.TextView").exists:
                    z.toast("添加失败")
                    z.heartbeat( )
                    # self.repo.savePhonenumberXM( group, repo_group_id, "N" )
                    return
            print( group + "发送成功" )
        elif d(text="发消息").exists:
            # i = i +1
           pass
        else:
            z.toast("停止模块")
            return
        z.sleep( 1 )

        if flag2 :
            if d(resourceId="com.tencent.tim:id/ivTitleBtnLeft",description="返回按钮").exists:
                d( resourceId="com.tencent.tim:id/ivTitleBtnLeft", description="返回按钮" ).click()
                z.sleep(2)
                z.heartbeat()

            if d(text="取消",resourceId="com.tencent.tim:id/btn_cancel_search").exists:
                d( text="取消", resourceId="com.tencent.tim:id/btn_cancel_search" ).click()
                z.sleep(1)
                z.heartbeat()
            if d(text="联系人",resourceId="com.tencent.tim:id/ivTitleBtnLeft").exists:
                d( text="联系人", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click()
                z.sleep(1)
                z.heartbeat()
            if d( index=1, description='群和多人聊天 按钮', resourceId='com.tencent.tim:id/name',
                  className="android.widget.RelativeLayout" ).exists:
                z.heartbeat( )
                d( index=1, description='群和多人聊天 按钮', resourceId='com.tencent.tim:id/name',
                   className="android.widget.RelativeLayout" ).click( )
                z.sleep( 2 )
                z.heartbeat( )
            if d( text="我的群", className="android.widget.TextView" ).exists:
                d( text="多人聊天", className="android.widget.TextView" ).click( )
                z.sleep( 1 )
                z.heartbeat( )

            if d(text="搜索",className="android.widget.TextView").exists:
                d( text="搜索", className="android.widget.TextView" ).click()
                z.sleep(1)
                z.heartbeat()
                z.input(group)
                if d( textContains="没有与", resourceId="com.tencent.mobileqq:id/loading",
                      className="android.widget.TextView" ).exists:
                    z.toast( "该群号可能不是你的群,结束运行" )
                    self.repo.savePhonenumberXM( myAccount, repo_group_id, "N", group )
                    return

                ob =  d(index=0,className="android.widget.RelativeLayout").child(index=0,resourceId="com.tencent.tim:id/image",className="android.widget.ImageView")
                if ob.exists:
                    ob.click()
                    z.sleep(1)
                    z.heartbeat()
                else:
                    z.toast("该QQ群不是你加入的的群了,停止运行")
                    self.repo.savePhonenumberXM( myAccount, repo_group_id, "N", group )
                    return

                if d(resourceId="com.tencent.tim:id/ivTitleBtnRightImage",description="群资料卡").exists:
                    d( resourceId="com.tencent.tim:id/ivTitleBtnRightImage", description="群资料卡" ).click()
                    z.sleep(3)
                    z.heartbeat()

        obj = d( index=3, className="android.widget.LinearLayout" ).child( description='邀请新成员',
                                                                           className="android.widget.ImageView" )  # 点不到这个，莫名其妙
        # obj = d( text="群成员", className="android.widget.TextView" )
        if obj.exists:
            d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
            # d( index=3, className="android.widget.LinearLayout" ).child( description='邀请新成员',
            #                                                              className="android.widget.ImageView" ).click()
            d.dump( compressed=False )
            # obj.click( )
            obj.click( )
            z.sleep( 5 )
            z.heartbeat( )
        else:
            d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
            z.sleep( 2 )
            if obj.exists:
                obj = obj.click( )
                z.sleep( 5 )
            else:
                z.toast( "该群无法邀请好友" )
                self.repo.savePhonenumberXM( group, repo_group_id, "N", myAccount )
                return
        if d( index=0, resourceId="com.tencent.tim:id/ivTitleBtnRightImage", description="更多" ).exists:
            d( index=0, resourceId="com.tencent.tim:id/ivTitleBtnRightImage", description="更多" ).click( )
            z.sleep( 2 )
            z.heartbeat( )
        if d( text="邀请新成员", resourceId="com.tencent.tim:id/action_sheet_button" ).exists:
            z.sleep( 1 )
            z.heartbeat( )
            d( text="邀请新成员", resourceId="com.tencent.tim:id/action_sheet_button" ).click( )
        z.sleep( 2 )
        z.heartbeat( )
        count = 0
        i = 0
        qqList = []
        repo_qq_id = int( args["repo_qq_id"] )  # 得到取号码的仓库号
        qq = self.repo.GetNumber( repo_qq_id, 0, 100, "normal", "NO", None,
                                  myAccount.encode( 'utf-8' ) )  # 取出t1条两小时内没有用过的号码
        if len( qq ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库为空，等待中\"" % repo_qq_id ).communicate( )
            return
        while True:
            # obj = d(index=3,className="android.widget.LinearLayout").child(description='邀请新成员',className="android.widget.ImageView")

            # list = numbers  # 将取出的号码保存到一个新的集合
            # print( list )
            # z.sleep(15)
            if i >len(qq)-1:
                break
            # z.sleep( 1 )
            z.heartbeat( )
            QQnumber = qq[i]['number'].encode('utf-8')
            print(QQnumber)

            if d(text="搜索",className="android.widget.EditText").exists:
                d( text="搜索", className="android.widget.EditText" ).click()
                z.sleep(2)
                z.heartbeat()
                z.input(QQnumber)
                z.sleep(2)
            breakA = False
            while d(text="已加入",className="android.widget.TextView").exists:
                z.toast("该好友已加入该群")
                objText = d(index=0,className="android.widget.RelativeLayout").child(index=1,className="android.widget.EditText")
                if objText.exists:
                    objText = objText.info["text"]
                    lenth = len( objText )
                    m = 0
                    while m < lenth:
                        d.press.delete( )
                        m = m + 1
                breakA = True
                z.sleep(1)
                break
            if breakA:
                i = i + 1
                self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "Y", myAccount )
                continue
            d.dump( compressed=False )
            if d( textContains="没有与", resourceId="com.tencent.tim:id/loading",
                  className="android.widget.TextView" ).exists:
                z.toast( "该QQ号可能不是你的好友" )
                self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "N", myAccount )
                i = i + 1
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
            obj = d( index=0, className="android.widget.AbsListView" ).child( index=1,
                                                                              className="android.widget.RelativeLayout",
                                                                              resourceId="com.tencent.tim:id/group_item_layout" )
            if obj.exists:
                obj.click( )
                z.sleep( 2 )
                z.heartbeat( )
                self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "Y", myAccount )
                i = i + 1
                if QQnumber not in qqList:
                    qqList.append( QQnumber )
                count = count + 1
                if count >= totalNumber:
                    break
            else:
                z.toast( "该QQ号可能不是你的好友" )
                self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "N", myAccount )
                i = i + 1
                continue
        if d( textContains="完成", resourceId="com.tencent.tim:id/ivTitleBtnRightText" ).exists:
            d( textContains="完成", resourceId="com.tencent.tim:id/ivTitleBtnRightText" ).click( )
            z.sleep( 3 )
            z.heartbeat( )
            if d( textContains="完成", resourceId="com.tencent.tim:id/ivTitleBtnRightText" ).exists:
                z.toast( "无法拉好友入群" )
                # self.repo.savePhonenumberXM( myAccount, repo_group_id, "N", group )
                return
            for i in range( len( qqList ) ):
                self.repo.savePhonenumberXM( qqList[i], repo_qq_id, "Y", myAccount )
            z.sleep( 1 )
            z.sleep( 1 )
            z.heartbeat( )
            # self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "Y", myAccount )
        z.toast("模块完成")
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return TIMAppointGroupPullFriends

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT524SK00685")
    z = ZDevice("HT524SK00685")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_qq_id":"246","repo_group_id":"239","totalNumber":"5","time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)
    # numbers = Repo().GetNumber( "239", 60, 1000, "normal", "NO" )
    # if len( numbers ) == 0:
    #     d.server.adb.cmd( "shell",
    #                       "am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库中该账号对应的数据取完，等待中\"" % "239" ).communicate( )
    #     z.sleep( 10 )
    # list = numbers  # 将取出的号码保存到一个新的集合
    # # print( list )
    # # z.sleep(15)
    # num = random.randint( 0, len( list ) - 1 )
    # group = list[num]['number']
    # print( group )
    # z.sleep( 3 )