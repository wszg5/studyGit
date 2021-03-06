# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class TIMGroupChatSendTextForGroupFriends2:
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
        z.toast( "TIM群聊群成员发消息" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM群聊群成员发消息" )
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
        if d( text="消息", resourceId="com.tencent.tim:id/ivTitleName" ).exists and not d( text="马上绑定",className="android.widget.Button" ).exists:
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
        repo_meg_id = args["repo_meg_id"]
        repo_group_id = int( args["repo_group_id"] )  # 得到取号码的仓库号

        n = 0
        # group_number = int(args["group_number"])
        while n<totalNumber:
            nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" )  # 当前时间

            para = {"x_key": "", "x_value": ""}
            totalList = Repo( ).GetTIMInfomation( repo_group_id, para )

            if len( totalList ) == 0:
                z.toast( "%s仓库可用数据为空" % repo_group_id )
                return
            num = random.randint( 0, len( totalList ) - 1 )
            address = totalList[num]["phonenumber"]
            address = address.encode( 'utf-8' )
            name = totalList[num]["x02"]
            if totalList[num]["x03"] == None:
                useCount = 0
            else:
                useCount = int( totalList[num]["x03"] )
            if not totalList[num]["x04"] ==None :
                thisTime = totalList[num]["x04"].encode("utf-8")  # 仓库中数据：时间
            else:
                thisTime = None
            if useCount >= 5:
                if thisTime == None or thisTime == "None":
                    para = {"phoneNumber": address, 'x_01': myAccount,
                            'x_03': useCount, 'x_04': nowTime,'x_06':'N'}
                    # z.toast( "该地址已被超过五人使用,3小时候后才可被使用" )
                    self.repo.PostInformation( repo_group_id, para )
                    para2 = {"x_key": "x_06", "x_value": "normal"}
                    totalList = Repo( ).GetTIMInfomation( repo_group_id, para2 )

                    if len( totalList ) == 0:
                        z.toast( "%s仓库%s账号可用数据为空" % (repo_group_id, myAccount) )
                        return
                    num = random.randint( 0, len( totalList ) - 1 )
                    address = totalList[num]["phonenumber"]
                    address = address.encode( 'utf-8' )
                    useCount = int( totalList[num]["x03"] )
                    if totalList[num]["x05"] == None:
                        peopleCount = 0
                    else:
                        peopleCount = int( totalList[num]["x05"] )
                    if not totalList[num]["x04"] == None:
                        thisTime = totalList[num]["x04"].encode( "utf-8" )  # 仓库中数据：时间
                    else:
                        thisTime = None
                else:
                    thisTime = self.getTimeSecond( thisTime )
                    nowTime = self.getTimeSecond( nowTime )
                    if nowTime - thisTime >= 2 * 60 * 60:
                        para = {"phoneNumber": address, 'x_01': myAccount,
                                'x_03': "0",'x_04':None,'x_06':'normal'}
                        self.repo.PostInformation( repo_group_id, para )
                    else:
                        para2 = {"x_key": "x_06", "x_value": "normal"}
                        totalList = Repo( ).GetTIMInfomation( repo_group_id, para2 )

                        if len( totalList ) == 0:
                            z.toast( "%s仓库%s账号可用数据为空" % (repo_group_id, myAccount) )
                            return
                        num = random.randint( 0, len( totalList ) - 1 )
                        address = totalList[num]["phonenumber"]
                        address = address.encode( 'utf-8' )
                        if totalList[num]["x03"] == None:
                            useCount = 0
                        else:
                            useCount = int( totalList[num]["x03"] )
                        if totalList[num]["x05"] == None:
                            peopleCount = 0
                        else:
                            peopleCount = int( totalList[num]["x05"] )
                        if not totalList[num]["x04"] == None:
                            thisTime = totalList[num]["x04"].encode( "utf-8" )  # 仓库中数据：时间
                        else:
                            thisTime = None
            print(address)


            # while True:
            #     Material = self.repo.GetMaterial( repo_meg_id, 0, 1 )
            #     if len( Material ) == 0:
            #         d.server.adb.cmd( "shell",
            #                           "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % repo_group_id ).communicate( )
            #         z.sleep( 10 )
            #         return
            #     message = Material[0]['content']
            #     nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" )  # 当前时间
            #     # para = {"phoneNumber":address,"x_key": "x_02", "x_value": name}
            #     # totalList = Repo( ).GetTIMInfomation( repo_group_id, para )
            #     totalList = Repo( ).GetInformation( repo_group_id, address )
            #     if len( totalList ) == 0:
            #         z.toast( "%s仓库可用数据为空" % repo_group_id )
            #         break
            #     if y == len(totalList):
            #         para = {"phoneNumber": address, 'x_01': myAccount,"x_20":number,
            #                 'x_03': useCount + 1}
            #         self.repo.PostInformation( repo_group_id, para )
            #         break
            #     num = random.randint( 0, len( totalList ) - 1 )
            #     address = totalList[y]["phonenumber"]
            #     address = address.encode( 'utf-8' )
            #     if totalList[y]["x03"] == None:
            #         useCount = 0
            #     else:
            #         useCount = int( totalList[y]["x03"] )
            #     if not totalList[num]["x04"] == None:
            #         thisTime = totalList[num]["x04"].encode( "utf-8" )  # 仓库中数据：时间
            #     else:
            #         thisTime = None
            #     if useCount >= 5:
            #         if thisTime == None or thisTime == "None":
            #             para = {"phoneNumber": address, 'x_01': myAccount,
            #                     'x_03': useCount, 'x_04': nowTime}
            #             # z.toast( "该地址已被超过五人使用,3小时候后才可被使用" )
            #             self.repo.PostInformation( repo_group_id, para )
            #             y = y + 1
            #             continue
            #         else:
            #             thisTime = self.getTimeSecond( thisTime )
            #             nowTime = self.getTimeSecond( nowTime )
            #             if nowTime - thisTime >= 2 * 60 * 60:
            #                 para = {"phoneNumber": address, 'x_01': myAccount,
            #                         'x_03': "0"}
            #                 self.repo.PostInformation( repo_group_id, para )
            #             else:
            #                 y = y + 1
            #                 continue
            #     print(address)
            #     number = totalList[y]["x20"]
            #     if d(description="QQ电话",resourceId="com.tencent.tim:id/ivTitleBtnRightCall").exists:
            #         d( description="QQ电话", resourceId="com.tencent.tim:id/ivTitleBtnRightCall" ).click()
            #         z.sleep(1)
            #         z.heartbeat()
            #     if d(resourceId="com.tencent.tim:id/et_search_keyword",text="搜索").exists:
            #         d( resourceId="com.tencent.tim:id/et_search_keyword", text="搜索" ).click()
            #         z.sleep(1)
            #         z.heartbeat()
            #         z.input( number )
            #
            #     if d( textContains="没有与", resourceId="com.tencent.tim:id/loading",
            #           className="android.widget.TextView" ).exists:
            #         z.toast( "该账号不在群聊" )
            #         z.sleep(1)
            #         y = y + 1
            #         if d(resourceId="com.tencent.tim:id/ib_clear_text",description="清空").exists:
            #             d( resourceId="com.tencent.tim:id/ib_clear_text", description="清空" ).click()
            #             z.sleep(1)
            #             z.heartbeat()
            #         continue
            #
            #     if d(text="多人聊天成员",className="android.widget.TextView").exists:
            #         d( text="多人聊天成员", className="android.widget.TextView" ).click()
            #         z.sleep(1)
            #         z.heartbeat()
            #
            #     obj = d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).left( index=0,
            #                                                                         resourceId="com.tencent.tim:id/input",
            #                                                                         className="android.widget.EditText" )
            #     if obj.exists:
            #         obj.click( )
            #         z.sleep( 1 )
            #         z.input(message)
            #         z.sleep(1)
            #         z.heartbeat()
            #
            #     if d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).exists:
            #         d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).click( )
            #         z.sleep( 1 )
            #         y = y + 1
            #     if useCount + 1 >= 5:
            #         para = {"phoneNumber": address, 'x_01': myAccount,
            #                 'x_03': useCount + 1, "x_04": nowTime}
            #     else:
            #         para = {"phoneNumber": address, 'x_01': myAccount,
            #                 'x_03': useCount + 1}
            #     self.repo.PostInformation( repo_group_id, para )
            #     if d(resourceId="com.tencent.tim:id/ivTitleBtnLeft",text="返回").exists:
            #         d( resourceId="com.tencent.tim:id/ivTitleBtnLeft", text="返回" ).click()
            #         z.sleep(1)
            #     if d( resourceId="com.tencent.tim:id/ib_clear_text", description="清空" ).exists:
            #         d( resourceId="com.tencent.tim:id/ib_clear_text", description="清空" ).click( )
            #         z.sleep( 1 )
            #         z.heartbeat( )
            x = 0
            y = 0
            i = 0
            peopleNumber = 1
            while True:
                if i == peopleNumber:
                    if useCount + 1 >= 5:
                        para = {"phoneNumber": address, 'x_01': myAccount,
                                'x_03': useCount + 1, "x_04": nowTime}
                    else:
                        para = {"phoneNumber": address, 'x_01': myAccount,
                                'x_03': useCount + 1}
                    self.repo.PostInformation( repo_group_id, para )
                    break
                d.server.adb.cmd( "shell", 'am start -a android.intent.action.VIEW -d "%s"' % address )
                z.sleep( 2 )
                z.sleep( 10 )
                a = 0
                while not d( text="加入多人聊天", className="android.widget.Button" ).exists:
                    while d( text="UC浏览器", className="android.widget.TextView" ).exists:
                        d( text="UC浏览器", className="android.widget.TextView" ).click( )
                        if d( text="跳过", className="android.widget.TextView" ).exists:
                            d( text="跳过", className="android.widget.TextView" ).click( )
                        z.sleep( 5 )
                        z.heartbeat( )
                    while d( text="仅此一次" ).exists and (not d( text="TIM" ).exists):
                        d( text="仅此一次" ).click( )
                        z.sleep( 2 )
                    z.sleep( 1 )
                    z.heartbeat( )
                    while d( text="打开", className="android.widget.TextView" ).exists:
                        d( text="打开", className="android.widget.TextView" ).click( )
                        z.sleep( 3 )
                        z.heartbeat( )
                    z.sleep( 1 )
                    while d( text="始终允许", className="android.widget.TextView" ).exists:
                        d( text="始终允许", className="android.widget.TextView" ).click( )
                        z.sleep( 2 )
                        z.heartbeat( )
                    z.sleep( 1 )
                    while d( text="TIM" ).exists:
                        d( text="TIM" ).click( )
                        z.sleep( 2 )
                        z.heartbeat( )
                        if d( text="仅此一次" ).exists:
                            d( text="仅此一次" ).click( )
                            z.sleep( 2 )
                            z.heartbeat( )
                    a = a + 1
                    d.dump( compressed=False )
                    z.sleep( 2 )
                    if a == 4:
                        z.toast( "浏览器加载不出来" )
                        break

                if d( text="加入多人聊天", className="android.widget.Button" ).exists:
                    d( text="加入多人聊天", className="android.widget.Button" ).click( )
                    z.sleep( 2 )
                    z.heartbeat( )
                else:
                    z.toast( "浏览器加载不出来" )
                    return

                while d( resourceId="com.tencent.tim:id/ivTitleBtnRightImage", description="聊天设置" ).exists:
                    d( resourceId="com.tencent.tim:id/ivTitleBtnRightImage", description="聊天设置" ).click( )
                    z.sleep( 1 )
                    z.heartbeat( )
                peopleNumber = 0
                if d( textContains="多人聊天成员", className="android.widget.TextView" ).exists:
                    peopleNumber = d( textContains="多人聊天成员", className="android.widget.TextView" ).info["text"]
                    peopleNumber = int( peopleNumber[7:][:-2] )

                Material = self.repo.GetMaterial( repo_meg_id, 0, 1 )
                if len( Material ) == 0:
                    d.server.adb.cmd( "shell",
                                      "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % repo_group_id ).communicate( )
                    z.sleep( 10 )
                    return
                message = Material[0]['content']
                peopleList = []

                z.sleep( 0.5 )

                d.dump( compressed=False )
                obj = d( index=1, className="android.widget.GridView" ).child( index=i,
                                                                               className="android.widget.RelativeLayout" )
                if obj.exists:
                    obj.click( )
                    z.sleep( 3 )
                    z.heartbeat( )
                    if d(text="发消息",className="android.widget.Button").exists:
                        d( text="发消息", className="android.widget.Button" ).click()
                        z.sleep(2)
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
                        #     z.sleep( 1 )
                        # if d(textContains="消息",resourceId="com.tencent.tim:id/ivTitleBtnLeft").exists:
                        #     d( textContains="消息", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click()
                        #     z.sleep(2)
                            i = i + 1
                    else:
                        z.toast("无法发送消息给对方")
                        i = i + 1
                        continue
                    # obj = d( index=0, className="android.widget.LinearLayout" ).child( index=1,
                    #                                                                    className="android.widget.RelativeLayout" ).child(
                    #     index=1, className="android.widget.TextView" )
                    # d.dump( compressed=False )
                    # # obj = d( text="帐号", className="android.widget.TextView" ).down( index=1 )
                    # obj = d( index=0, className="android.widget.LinearLayout" ).child( index=1,
                    #                                                                    className="android.widget.LinearLayout" ).child(
                    #     index=0, className="android.widget.TextView", resourceId="com.tencent.tim:id/info" )
                    # if obj.exists:
                    #     thisAccount = obj.info["text"].encode( 'utf-8' )  # 获取的账号
                    #     try:
                    #         thisAccount = int( thisAccount )
                    #     except:
                    #         i = i + 1
                    #         if d( text="返回", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).exists:
                    #             d( text="返回", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click( )
                    #         continue
                    # else:
                    #     if d( text="帐号", className="android.widget.TextView" ).exists:
                    #         obj = d( text="帐号", className="android.widget.TextView" ).down( index=1 )
                    #         z.sleep( 0.5 )
                    #     else:
                    #         d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                    #         d.dump( compressed=False )
                    #         if d( text="帐号", className="android.widget.TextView" ).exists:
                    #             obj = d( text="帐号", className="android.widget.TextView" ).down( index=1 )
                    #             z.sleep( 0.5 )
                    #         else:
                    #             z.toast( "获取不到账号" )
                    #
                    # if obj.exists:
                    #     thisAccount = obj.info["text"].encode( 'utf-8' )  # 获取的账号
                    #     try:
                    #         thisAccount = int( thisAccount )
                    #     except:
                    #         d.dump( compressed=False )
                    #         obj = d( text="帐号", className="android.widget.TextView" ).down( index=1,
                    #                                                                         className="android.widget.TextView" )
                    #         if obj.exists:
                    #             thisAccount = obj.info["text"].encode( 'utf-8' )  # 获取的账号
                    #             try:
                    #                 thisAccount = int( thisAccount )
                    #             except:
                    #                 i = i + 1
                    #                 if d( text="返回", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).exists:
                    #                     d( text="返回", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click( )
                    #                 continue
                    #     z.sleep( 1 )
                    #     # thisAccount = str(thisAccount)
                    #     z.toast( "获得的帐号:%d" % thisAccount )
                    #     if thisAccount not in peopleList:
                    #         peopleList.append( thisAccount )
                    #         para = {"phoneNumber": address, 'x_01': myAccount, 'x_02': name, 'x_03': "0",
                    #                 'x_06': 'normal', 'x_20': thisAccount}
                    #         self.repo.PostInformation( repo_group_id, para )
                else:
                    while not obj.exists:
                        d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                        z.sleep(1)
                        d.dump( compressed=False )
                        # obj = d( index=1, className="android.widget.GridView" ).child( index=i,
                        #                                                                className="android.widget.RelativeLayout" )
                        # if not obj.exists:
                        #     break



            n = n + 1
        z.toast("模块完成")
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return TIMGroupChatSendTextForGroupFriends2

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("cda0ae8d")
    z = ZDevice("cda0ae8d")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_meg_id":"40","repo_group_id":"256","totalNumber":"5","time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)
    #
    # para = {"phoneNumber": "http://url.cn/5AfooBi#flyticket", "x_key": "x_02", "x_value": "M8"}
    # totalList = Repo( ).GetTIMInfomation( "256", para )
    # x = Repo().GetInformation("256","http://url.cn/5AfooBi#flyticket")
    # z.sleep(1)
