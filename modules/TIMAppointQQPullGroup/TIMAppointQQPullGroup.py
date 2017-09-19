# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class TIMAppointQQPullGroup:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.toast( "TIM指定QQ拉群" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM指定QQ拉群" )
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
        if d( text="消息" ).exists:
            z.toast( "登录状态正常，继续执行" )
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
        obj = d(index=0,className="android.widget.LinearLayout").child(index=1,className="android.widget.LinearLayout").child(index=0,className="android.widget.TextView",resourceId="com.tencent.tim:id/info")
        if obj.exists:
            myAccount = obj.info["text"]      #获取自己的账号
            z.toast("获取自己的账号")
            z.sleep(2)
            z.heartbeat()
        else:
            z.toast("获取不到自己的账号")
            return
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        totalNumber = int(args['totalNumber'])  # 要给多少人发消息
        repo_qq_id = int( args["repo_qq_id"] )  # 得到取号码的仓库号
        qq = self.repo.GetNumber( repo_qq_id, 0, 1000, "normal", "NO" )  # 取出t1条两小时内没有用过的号码
        if len( qq ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库为空，等待中\"" % repo_qq_id ).communicate( )

            z.sleep( 10 )
            return
        # list = numbers  # 将取出的号码保存到一个新的集合
        # print( list )
        # z.sleep(15)
        num = random.randint( 0, len( qq ) - 1 )
        z.sleep( 1 )
        z.heartbeat( )
        if qq[num]['name']==None:
            count = 0
        else:
            count = int(qq[num]['name'])
        QQnumber = qq[num]['number']
        if  count>=totalNumber:
            self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "N", count )
            z.toast("该qq号已被拉群%s次"%count)
            return
        print(QQnumber)
        z.sleep(3)
        z.heartbeat()

        #先写死，到时候再改
        z.cmd( "shell",
               'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"' % QQnumber )  # qq名片页面

        if d(text='TIM').exists:
            z.heartbeat( )
            d(text='TIM').click()
            z.sleep(2)
            z.heartbeat()
            while d(text='仅此一次').exists:
                z.heartbeat( )
                d(text='仅此一次').click()
        z.sleep(1)
        if d(text="申请加群").exists:
            return
        z.sleep(1)
        d.dump( compressed=False )
        if d(text='加好友',className="android.widget.Button").exists:
            d(text='加好友',className="android.widget.Button").click()
            z.sleep(5)
            z.heartbeat()
            if d(text='加好友',className="android.widget.Button").exists:    #拒绝被添加的轻况
                return
            if d(text='必填',resourceId='com.tencent.tim:id/name').exists:                     #要回答问题的情况
                z.heartbeat( )
                return
            d.dump( compressed=False )
            if d(text="风险提示").exists:   #风险提示
                z.heartbeat()
                return
            obj = d( text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText' )  # 不需要验证可直接添加为好友的情况
            if obj.exists:
                z.sleep( 2 )
                obj.click( )
                if d( text='添加失败，请勿频繁操作', resourceId='com.tencent.tim:id/name' ).exists:
                    z.heartbeat( )
                    z.toast( "频繁操作,跳出模块" )
                    return
                else:
                    print( QQnumber + "请求发送成功" )

            z.sleep( 2 )
            z.heartbeat( )
            d.dump( compressed=False )
            if d(text='下一步',resourceId='com.tencent.tim:id/ivTitleBtnRightText').exists:
                z.heartbeat()
                d(text='下一步',resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
            z.sleep( 2 )
            if d(text='发送').exists:
                d(text='发送').click()
                z.sleep(3)
            if d( resourceId='com.tencent.tim:id/name', text='添加失败，请勿频繁操作' ).exists:  # 操作过于频繁的情况
                z.toast("频繁操作,跳出模块")
                return
            print(QQnumber+"请求发送成功")
            z.heartbeat()
        while True:
            z.sleep(3)
            z.heartbeat()
            repo_group_id = int( args["repo_group_id"] )  # 得到取号码的仓库号
            numbers = self.repo.GetNumber( repo_group_id, 60, 1, "normal", "NO", myAccount.encode('utf-8') )  # 取出t1条两小时内没有用过的号码
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库中该账号对应的数据取完，等待中\"" % repo_group_id ).communicate( )
                z.sleep( 10 )
                return
            list = numbers  # 将取出的号码保存到一个新的集合
            # print( list )
            # z.sleep(15)
            group = list[0]['number']
            z.sleep( 1 )
            z.heartbeat( )
            z.toast( "准备唤醒的群号为" + group )
            d.server.adb.cmd("shell", 'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=group&source=qrcode"'%group )  # 群页面
            z.heartbeat()
            z.sleep(2)
            z.heartbeat( )
            if d( text='TIM' ).exists:
                d( text='TIM' ).click( )
                time.sleep( 0.5 )
                while d( text='仅此一次' ).exists:
                    d( text='仅此一次' ).click( )
            n = 0
            flag = False
            while (not d(text="发消息",className="android.widget.Button").exists and not d(text='申请加群').exists) or \
                    ( d(text="发消息",className="android.widget.Button").exists and  d(text="QQ电话",className="android.widget.Button").exists):
                z.toast( "准备唤醒的群号为" + group )
                d.server.adb.cmd( "shell",
                                  'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=group&source=qrcode"' % group )  # 群页面
                z.heartbeat()
                z.sleep(2)
                if (not d(text="发消息",className="android.widget.Button").exists and not d(text='申请加群').exists) or \
                    ( d(text="发消息",className="android.widget.Button").exists and  d(text="QQ电话",className="android.widget.Button").exists):
                    if n==4:
                        z.toast("唤醒不出来")
                        flag=True
                        break
                    else:
                        n = n + 1
                else:
                    if d( text='TIM' ).exists:
                        d( text='TIM' ).click( )
                        time.sleep( 0.5 )
                        while d( text='仅此一次' ).exists:
                            d( text='仅此一次' ).click( )
                    break
            if flag:
                z.sleep(1)
                continue
            if d(text='申请加群').exists:
                z.toast("不是该群成员了，无法拉群")
                self.repo.savePhonenumberXM( group, repo_group_id, "N", myAccount )
                z.sleep(2)
                continue
            # z.sleep(1)
            # z.heartbeat()
            obj = d(index=3,className="android.widget.LinearLayout").child(description='邀请新成员',className="android.widget.ImageView")  #点不到这个，莫名其妙
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
                    continue
            if d( index=0, resourceId="com.tencent.tim:id/ivTitleBtnRightImage", description="更多" ).exists:
                d( index=0, resourceId="com.tencent.tim:id/ivTitleBtnRightImage", description="更多" ).click( )
                z.sleep(2)
                z.heartbeat()
            if d(text="邀请新成员",resourceId="com.tencent.tim:id/action_sheet_button").exists:
                z.sleep(1)
                z.heartbeat()
                d( text="邀请新成员", resourceId="com.tencent.tim:id/action_sheet_button" ).click()
            z.sleep(2)
            z.heartbeat()
            if d(text="搜索",className="android.widget.EditText").exists:
                d( text="搜索", className="android.widget.EditText" ).click()
                z.sleep(2)
                z.heartbeat()
                z.input(QQnumber)
                z.sleep(1)
            if d(text="已加入",className="android.widget.TextView").exists:
                z.toast("该好友已加入该群")
                continue
            d.dump( compressed=False )
            if d(textContains="没有与",resourceId="com.tencent.tim:id/loading",className="android.widget.TextView").exists:
                z.toast( "该QQ号可能不是你的好友，请重新添加或等待对方同意,停止模块" )
                return
            obj = d(index=0,className="android.widget.AbsListView").child(index=1,className="android.widget.RelativeLayout",resourceId="com.tencent.tim:id/group_item_layout")
            if obj.exists:
                obj.click()
                z.sleep(2)
                z.heartbeat()
                if d(text="完成",resourceId="com.tencent.tim:id/ivTitleBtnRightText").exists:
                    d( text="完成", resourceId="com.tencent.tim:id/ivTitleBtnRightText" ).click()
                    z.sleep(3)
                    z.heartbeat()
                    if d(text="完成",resourceId="com.tencent.tim:id/ivTitleBtnRightText").exists:
                        z.toast("无法拉好友入群")
                        self.repo.savePhonenumberXM( group, repo_group_id, "N", myAccount )
                        continue
                    count = count + 1
                    self.repo.savePhonenumberXM( group, repo_group_id, "Y", myAccount )
                    z.sleep(1)
                    z.heartbeat()
                    self.repo.savePhonenumberXM(QQnumber , repo_qq_id, "normal",count)
                    if count>=totalNumber:
                        break
            else:
                z.toast("该QQ号可能不是你的好友，请重新添加")
                return
        z.toast("模块完成")
        print("模块完成")
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return TIMAppointQQPullGroup

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT524SK00685")
    z = ZDevice("HT524SK00685")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_group_id":"233","repo_qq_id":"236","totalNumber":"12","time_delay":"3"}    #cate_id是仓库号，length是数量
    # o.action(d, z,args)
    qq = Repo().GetNumber( "233", 1, 1,"normal","NO",None,"226378573")  # 取出t1条两小时内没有用过的号码
    if len( qq ) == 0:
        d.server.adb.cmd( "shell",
                          "am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库为空，等待中\"" % "236" ).communicate( )
        z.sleep( 10 )
    # list = numbers  # 将取出的号码保存到一个新的集合
    # print( list )
    # z.sleep(15)
    z.sleep( 1 )
    z.heartbeat( )
    if qq[0]['name'] == None:
        count = 0
    else:
        count = int( qq[0]['name'] )
    QQnumber = qq[0]['number']
    if count >= 100:
        z.toast( "该qq号已被拉群%s次" % count )
    print( QQnumber )
    count = count + 1
    Repo().savePhonenumberXM(QQnumber,"236","Y",count)
    z.sleep(1)
