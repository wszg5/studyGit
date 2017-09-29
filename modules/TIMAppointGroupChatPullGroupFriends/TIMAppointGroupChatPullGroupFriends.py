# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class TIMAppointGroupChatPullGroupFriends:
    def __init__(self):
        self.repo = Repo()

    def getTimeSecond(self,thisTime):
        thistimeD = int(thisTime[6:8])
        thistimeH = int(thisTime[8:10])
        thistimeM = int(thisTime[10:12])
        thistimeS = int(thisTime[12:])
        second = thistimeD * 24*60*60 + thistimeH * 60*60 + thistimeM * 60 + thistimeS
        return second

    def action(self, d,z, args):
        z.toast( "TIM指定群聊拉群成员" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM指定群聊拉群成员" )
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
        z.heartbeat( )
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        totalNumber = int( args['totalNumber'] )  # 要给多少人发消息
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
        # while d(text="返回",resourceId="com.tencent.tim:id/ivTitleBtnLeft").exists:
        #     d( text="返回", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click()
        #     z.sleep(1)
        #     z.heartbeat()

        j = 1
        text = 0
        listText = []
        x = 0
        groupNumber = args["groupNumber"]
        repo_information_id = args["repo_information_id"]
        while x < groupNumber:
            nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" )  # 当前时间

            para = {"x_key": "", "x_value": ""}
            totalList = Repo( ).GetTIMInfomation( repo_information_id, para )

            if len( totalList ) == 0:
                z.toast( "%s仓库%s账号可用数据为空" % (repo_information_id, myAccount) )
                return
            num = random.randint( 0, len( totalList ) - 1 )
            address = totalList[num]["phonenumber"]
            address = address.encode( 'utf-8' )
            if totalList[num]["x03"]==None:
                useCount = 0
            else:
                useCount = int( totalList[num]["x03"] )
            if totalList[num]["x05"]==None:
                peopleCount = 3
            peopleCount = int( totalList[num]["x05"] )
            thisTime = totalList[num]["x04"]  # 仓库中数据：时间
            if useCount >= 5:
                if thisTime == None:
                    para = {"phoneNumber": address, 'x_01': myAccount,
                            'x_03': useCount, 'x_04': nowTime}
                    z.toast( "该地址已被超过五人使用,3小时候后才可被使用" )
                    self.repo.PostInformation( repo_information_id, para )
                    continue
                thisTime = self.getTimeSecond( thisTime )
                nowTime = self.getTimeSecond( nowTime )
                if nowTime - thisTime >= 3 * 60 * 60:
                    para = {"phoneNumber": address, 'x_01': myAccount,
                            'x_03': "0"}
                    self.repo.PostInformation( repo_information_id, para )
                else:
                    continue
            print(address)
            d.server.adb.cmd( "shell", 'am start -a android.intent.action.VIEW -d "%s"' % address )
            z.sleep( 2 )
            a = 0
            while not d( text="加入多人聊天", className="android.widget.Button" ).exists:
                if d(text="UC浏览器",className="android.widget.TextView").exists:
                    d( text="UC浏览器", className="android.widget.TextView" ).click()
                    z.sleep(5)
                if d( text="仅此一次" ).exists and (not d( text="TIM" ).exists):
                    d( text="仅此一次" ).click( )
                    z.sleep( 2 )
                    z.heartbeat( )
                if d( text="打开", className="android.widget.TextView" ).exists:
                    d( text="打开", className="android.widget.TextView" ).click( )
                    z.sleep( 3 )
                    z.heartbeat( )
                if d(text="始终允许",className="android.widget.TextView").exists:
                    d( text="始终允许", className="android.widget.TextView" ).click()
                    z.sleep(2)
                    z.heartbeat()
                if d( text="TIM" ).exists:
                    d( text="TIM" ).click( )
                    z.sleep( 2 )
                    z.heartbeat( )
                    if d( text="仅此一次" ).exists:
                        d( text="仅此一次" ).click( )
                        z.sleep( 2 )
                        z.heartbeat( )
                a = a + 1
                if a==4:
                    z.toast("浏览器加载不出来")
                    return

            if d( text="加入多人聊天", className="android.widget.Button" ).exists:
                d( text="加入多人聊天", className="android.widget.Button" ).click( )
                z.sleep( 2 )
                z.heartbeat( )

            if d( resourceId="com.tencent.tim:id/ivTitleBtnRightImage", description="聊天设置" ).exists:
                d( resourceId="com.tencent.tim:id/ivTitleBtnRightImage", description="聊天设置" ).click( )
                z.sleep( 1 )
                z.heartbeat( )
            peopleNumber = 0
            if d( textContains="多人聊天成员", className="android.widget.TextView" ).exists:
                peopleNumber = d( textContains="多人聊天成员", className="android.widget.TextView" ).info["text"]
                peopleNumber =int( peopleNumber[7:][:-2])
                if peopleNumber>=80:
                    z.toast("该群聊已经有80人以上")
                    continue
            else:
                z.toast( "浏览器加载不出来" )
                return

            obj = d( index=1, className="android.widget.GridView" ).child( index=peopleNumber,
                                                                           className="android.widget.RelativeLayout" ).child(
                index=0, className="android.widget.ImageView" )
            flag = False
            while not obj.exists:
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                d.dump( compressed=False )
                if (not obj.exists) and d(text="退出多人聊天",className="android.widget.Button").exists:
                    z.toast("到底了,无法邀请,无法邀请")
                    flag=True
                    break
            if flag:
                continue
            z.sleep( 1 )
            if obj.exists:
                obj.click()
                z.sleep( 1 )
                z.heartbeat( )
            peopleNumber = int( peopleNumber )
            if 80 - peopleNumber <= totalNumber:
                totalNumber = 80 - peopleNumber
            count = self.pullFriends( d, z, args, myAccount, totalNumber )
            if count==None:
                count = 0
                para = {"phoneNumber": address, 'x_01': myAccount,
                        'x_03': useCount + 1, "x_05": count + peopleNumber}
                self.repo.PostInformation( repo_information_id, para )
                return
            x = x + 1
            z.sleep( 1 )
            z.heartbeat( )
            if useCount + 1>=5:
                para = {"phoneNumber": address, 'x_01': myAccount,
                        'x_03': useCount + 1,"x_04":nowTime,"x_05": count + peopleNumber}
            else:
                para = {"phoneNumber": address, 'x_01': myAccount,
                        'x_03': useCount + 1, "x_05": count + peopleNumber}
            self.repo.PostInformation( repo_information_id, para )
        # self.getIntoGroup(d,z)
        #
        # if d(text="多人聊天",className="android.widget.TextView").exists:
        #     d( text="多人聊天", className="android.widget.TextView" ).click()
        #     z.sleep(1)
        #     z.heartbeat()
        # if not d(index=0,resourceId="com.tencent.tim:id/lv_discussion",className="android.widget.AbsListView").child(index=1,className="android.widget.RelativeLayout").exists:
        #     if totalNumber % 90 ==0:
        #         i = totalNumber/90
        #     else:
        #         i = totalNumber / 90 + 1
        #     for n in range(0,i):
        #         if d(index=0,resourceId="com.tencent.tim:id/ivTitleBtnRightImage",className="android.widget.ImageView").exists:
        #             z.sleep(1)
        #             z.heartbeat()
        #             d( index=0, resourceId="com.tencent.tim:id/ivTitleBtnRightImage", className="android.widget.ImageView" ).click()
        #         if d(text="发起多人聊天").exists:
        #             d( text="发起多人聊天" ).click()
        #             z.sleep(1)
        #             z.heartbeat()
        #         if totalNumber > 90:
        #             self.pullFriends( d, z, args, myAccount, 90 )
        #         else:
        #             self.pullFriends( d, z, args, myAccount, totalNumber-90 )
        #         totalNumber = totalNumber - 90
        # else:
        #     j = 1
        #     text = 0
        #     listText=[]
        #     while True:
        #         objNum = d( index=0, resourceId="com.tencent.tim:id/lv_discussion",
        #                     className="android.widget.AbsListView" ).child(
        #             index=j, className="android.widget.RelativeLayout" ).child(
        #             index=2, resourceId="com.tencent.tim:id/text2", className="android.widget.TextView"
        #         )
        #         objT = d( index=0, resourceId="com.tencent.tim:id/lv_discussion",
        #                     className="android.widget.AbsListView" ).child(
        #             index=j, className="android.widget.RelativeLayout" ).child(
        #             index=1, resourceId="com.tencent.tim:id/text1", className="android.widget.TextView"
        #         )
        #
        #         if objNum.exists:
        #             text = objNum.info["text"]
        #             text = int( text[1:][:-1] )
        #             z.sleep( 1 )
        #             text = 90 - text
        #             if text > totalNumber:
        #                 text = totalNumber
        #             obj = objT.info["text"]
        #             if objT not in listText:
        #                 listText.append(objT)
        #                 objNum.click()
        #                 z.sleep(2)
        #                 z.heartbeat()
        #             else:
        #                 j = j + 1
        #                 continue
        #             if d(index=0,resourceId="com.tencent.tim:id/ivTitleBtnRightImage",description="聊天设置").exists:
        #                 d( index=0, resourceId="com.tencent.tim:id/ivTitleBtnRightImage", description="聊天设置" ).click()
        #             picnum = d( text="邀请" ).up( index=0, className="android.widget.ImageView",
        #                                         resourceId="com.tencent.tim:id/icon" )
        #             if picnum.exists:
        #                 while picnum.exists:
        #                     picnum.click( )
        #                 z.sleep( 1 )
        #                 z.heartbeat( )
        #             else:
        #                 d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
        #                 z.sleep( 2 )
        #                 if picnum.exists:
        #                     while picnum.exists:
        #                         picnum.click( )
        #                         z.sleep( 1 )
        #                         z.heartbeat( )
        #                 else:
        #                     z.toast( "该群聊无法邀请好友" )
        #                     # self.repo.savePhonenumberXM( group, repo_group_id, "N", myAccount )
        #             self.pullFriends(d,z, args,myAccount,text)
        #             totalNumber = totalNumber - text
        #             j = j + 1
        #         else:
        #             if j>=9:
        #                 d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
        #                 if d( index=0, resourceId="com.tencent.tim:id/lv_discussion",className="android.widget.AbsListView" ).child( index=j-1, className="android.widget.RelativeLayout" ).child(
        #             index=1, resourceId="com.tencent.tim:id/text1", className="android.widget.TextView").exists:
        #                     obj = objT.info["text"]
        #                     if objT not in listText:
        #                         listText.append( objT )
        #                         # objNum.click( )
        #                         j =  1
        #                         z.sleep( 2 )
        #                         z.heartbeat( )
        #                         continue
        #             if totalNumber % 90 == 0:
        #                 i = totalNumber / 90
        #             else:
        #                 i = totalNumber / 90 + 1
        #             for n in range( 0, i ):
        #                 if d( index=0, resourceId="com.tencent.tim:id/ivTitleBtnRightImage",
        #                       className="android.widget.ImageView" ).exists:
        #                     z.sleep( 1 )
        #                     z.heartbeat( )
        #                     d( index=0, resourceId="com.tencent.tim:id/ivTitleBtnRightImage",
        #                        className="android.widget.ImageView" ).click( )
        #                 if d( text="发起多人聊天" ).exists:
        #                     d( text="发起多人聊天" ).click( )
        #                     z.sleep( 1 )
        #                     z.heartbeat( )
        #                 self.pullFriends( d, z, args, myAccount, 90 )
        #                 totalNumber = totalNumber - 90
        #                 j = j + 1
        #                 if d(textContains="消息",resourceId="com.tencent.tim:id/ivTitleBtnLeft").exists:
        #                     d( textContains="消息", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click()
        #                 self.getIntoGroup(d,z)
                # self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "Y", myAccount )
        z.toast("模块完成")
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

    def pullFriends(self, d,z, args,myAccount,totalNumber):
        count = 0
        x = 0
        i = 0
        qqList = []
        flag = True
        # flag2 = False
        repo_group_id = int( args["repo_group_id"] )
        groupNumber = self.getGroupNumber( d,z,args, myAccount )
        if groupNumber==None:
            return
        while True:
            # obj = d(index=3,className="android.widget.LinearLayout").child(description='邀请新成员',className="android.widget.ImageView")

            repo_qq_id = int( args["repo_qq_id"] )  # 得到取号码的仓库号
            qq = self.repo.GetNumber( repo_qq_id, 60, 2000, "normal", "NO",None, groupNumber )  # 取出t1条两小时内没有用过的号码
            if len( qq ) == 0:
                self.repo.savePhonenumberXM( myAccount, repo_qq_id, "N", groupNumber )
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库账号为%s没有数据可以再取出来，等待中\"" % (repo_qq_id,myAccount.encode( 'utf-8' )) ).communicate( )
                if x == 0:
                    z.sleep( 5 )
                    return
                else:
                    z.toast("仓库中该账户已经没有未被拉过的的好友")
                    break
            # list = numbers  # 将取出的号码保存到一个新的集合
            # print( list )
            # z.sleep(15)
            # if len(qq) == 1:
            #     flag2 = True
            if i >len(qq)-1:
                break
            z.sleep( 1 )
            z.heartbeat( )
            QQnumber = qq[i]['number'].encode( 'utf-8' )
            print( QQnumber )

            if d(text="从群聊中选择",className="android.widget.Button").exists:
                d( text="从群聊中选择", className="android.widget.Button" ).click()
                z.sleep(2)
                z.heartbeat()
            if d( text="搜索", className="android.widget.EditText" ).exists and d(text="返回",resourceId="com.tencent.tim:id/ivTitleBtnLeft").exists:
                d( text="搜索", className="android.widget.EditText" ).click( )
                z.sleep( 0.5 )
                z.heartbeat( )
                z.input( groupNumber )
                z.sleep( 0.5 )
                if d( textContains="没有与", resourceId="com.tencent.tim:id/loading",
                      className="android.widget.TextView" ).exists:
                    z.toast( "该群号码可能不是你的群" )
                    self.repo.savePhonenumberXM( myAccount, repo_qq_id, "N", groupNumber )
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

            if d( text="搜索", className="android.widget.EditText" ).exists and d(text="群",resourceId="com.tencent.tim:id/ivTitleBtnLeft").exists:
                if flag:
                    d( text="搜索", className="android.widget.EditText" ).click( )
                    flag = False
                    z.sleep( 0.5 )
                    z.heartbeat( )
                z.input( QQnumber )
                z.sleep( 0.5 )

                breakA = False
                while d( text="已加入", className="android.widget.TextView" ).exists or d(text="已选择",className="android.widget.TextView").exists:
                    z.toast( "该好友已加入该群或已选择" )
                    # self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "Y", groupNumber )
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
                    i = i + 1
                    # self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "Y", groupNumber )
                    continue
            # d.dump( compressed=False )
            if d( textContains="没有与", resourceId="com.tencent.tim:id/loading",
                  className="android.widget.TextView" ).exists:
                z.toast( "该群号可能不是你的群" )
                self.repo.savePhonenumberXM( myAccount, repo_qq_id, "N", groupNumber )
                i = i + 1
                groupNumber = self.getGroupNumber(d,z,args,myAccount)
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
                i = i + 1
                if QQnumber not in qqList:
                    qqList.append( QQnumber )
                # self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "Y", groupNumber )
                count = count + 1
                if count >= totalNumber:
                    break
            else:
                z.toast( "该QQ号可能不是你的群中的群成员了" )
                self.repo.savePhonenumberXM( QQnumber, repo_qq_id, "N", groupNumber )
                # i = i + 1
                continue
        if d( textContains="完成", resourceId="com.tencent.tim:id/ivTitleBtnRightText" ).exists:
            d( textContains="完成", resourceId="com.tencent.tim:id/ivTitleBtnRightText" ).click( )
            z.sleep( 3 )
            z.heartbeat( )
            if d( textContains="完成", resourceId="com.tencent.tim:id/ivTitleBtnRightText" ).exists:
                z.toast( "无法拉好友入群聊,停止模块" )
                self.repo.savePhonenumberXM( myAccount, repo_group_id, "N", groupNumber )
                return
            for i in range( len( qqList ) ):
                self.repo.savePhonenumberXM( qqList[i], repo_qq_id, "Y", myAccount )
            self.repo.savePhonenumberXM( myAccount, repo_qq_id, "Y", groupNumber )
            z.sleep( 1 )
            z.heartbeat( )
            return count

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

    def getGroupNumber(self,d,z,args,myAccount):
        repo_group_id = int( args["repo_group_id"] )  # 得到取号码的仓库号
        group = self.repo.GetNumber( repo_group_id, 60, 1, "normal", "NO",
                                     myAccount.encode( 'utf-8' ) )  # 取出t1条两小时内没有用过的号码
        if len( group ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库账号为%s没有数据可以再取出来，等待中\"" % (repo_group_id,
                              myAccount.encode( 'utf-8' )) ).communicate( )
            return
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
        groupNumber = group[0]['name']
        print( groupNumber )
        return groupNumber
def getPluginClass():
    return TIMAppointGroupChatPullGroupFriends

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("cda0ae8d")
    z = ZDevice("cda0ae8d")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_qq_id":"259","repo_group_id":"249","totalNumber":"25","time_delay":"3","repo_information_id":"253","groupNumber":"5"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)
    # obj = d( index=1, className="android.widget.GridView" ).child( index=57,
    #                                                                className="android.widget.RelativeLayout" ).child(index=0,className="android.widget.ImageView")