# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class TIMGroupChatCheckGroupFriends:
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
        z.toast( "TIM群聊检存群聊成员" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM群聊发消息" )
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
        z.sleep(5)
        z.heartbeat()
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
        repo_group_id = int( args["repo_group_id"] )  # 得到取号码的仓库号
        n = 0
        repo_info_id = args["repo_info_id"]
        while n<totalNumber:
            nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" )  # 当前时间

            para = {"x_key": "", "x_value": ""}
            totalList = self.repo.GetTIMInfomation( repo_info_id, para )

            if len( totalList ) == 0:
                z.toast( "%s仓库可用数据为空" % repo_info_id )
                return
            num = random.randint( 0, len( totalList ) - 1 )
            address = totalList[num]["phonenumber"]
            address = address.encode( 'utf-8' )
            name = totalList[num]["x02"]
            if totalList[num]["x03"] == None:
                useCount = 0
            else:
                useCount = int( totalList[num]["x03"] )
            peopleCount = int( totalList[num]["x05"] )
            thisTime = totalList[num]["x04"]  # 仓库中数据：时间
            if useCount >= 5:
                if thisTime == None:
                    para = {"phoneNumber": address, 'x_01': myAccount,
                            'x_03': useCount, 'x_04': nowTime}
                    z.toast( "该地址已被超过五人使用,3小时候后才可被使用" )
                    self.repo.PostInformation( repo_info_id, para )
                    continue
                thisTime = self.getTimeSecond( thisTime )
                nowTime = self.getTimeSecond( nowTime )
                if nowTime - thisTime >= 3 * 60 * 60:
                    para = {"phoneNumber": address, 'x_01': myAccount,
                            'x_03': "0"}
                    self.repo.PostInformation( repo_info_id, para )
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
                peopleNumber = int( peopleNumber[7:][:-2] )
            else:
                z.toast( "浏览器加载不出来" )
                return

            i = 0
            peopleList=[]
            while True:
                if i ==peopleNumber:
                    para = {"phoneNumber": address, 'x_01': myAccount,
                            'x_03': useCount + 1}
                    self.repo.PostInformation( repo_info_id, para )
                    break
                obj = d(index=1,className="android.widget.GridView").child(index=i,className="android.widget.RelativeLayout")
                if obj.exists:
                    obj.click()
                    z.sleep(2)
                    z.heartbeat()
                    # obj = d( index=0, className="android.widget.LinearLayout" ).child( index=1,
                    #                                                                    className="android.widget.RelativeLayout" ).child(
                    #     index=1, className="android.widget.TextView" )
                    obj = d( text="帐号", className="android.widget.TextView" ).down( index=1,
                                                                                    className="android.widget.TextView" )
                    if obj.exists:
                        thisAccount = obj.info["text"]  # 获取的账号
                        z.sleep( 1 )
                        if thisAccount not in peopleList:
                            peopleList.append(thisAccount)
                            para = {"phoneNumber": address, 'x_01': myAccount,'x_02':name,'x_03': "0",
                                    'x_06': 'normal','x_20': thisAccount}
                            self.repo.PostInformation( repo_group_id, para )
                        z.sleep( 1 )
                        z.sleep( 2 )
                        z.heartbeat( )
                        if d(text="返回",resourceId="com.tencent.tim:id/ivTitleBtnLeft").exists:
                            d( text="返回", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click()
                    else:
                        z.toast( "获取不到账号" )
                    i = i + 1
                else:
                    d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                    d.dump( compressed=False )
                    obj = d( index=1, className="android.widget.GridView" ).child( index=i,className="android.widget.RelativeLayout" )
                    if not obj.exists:
                        break

        z.toast("模块完成")
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return TIMGroupChatCheckGroupFriends

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT524SK00685")
    z = ZDevice("HT524SK00685")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_info_id":"253","repo_group_id":"256","totalNumber":"5","time_delay":"3",}    #cate_id是仓库号，length是数量
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