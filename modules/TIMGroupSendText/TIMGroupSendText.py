# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class TIMGroupSendText:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.toast( "TIM群发消息" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM群发消息" )
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
        repo_meg_id = args["repo_meg_id"]
        repo_group_id = int( args["repo_group_id"] )  # 得到取号码的仓库号
        Material = self.repo.GetMaterial( repo_meg_id, 0, 1 )
        if len( Material ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % repo_group_id ).communicate( )
            z.sleep( 10 )
            return
        message = Material[0]['content']
        n = 0
        while n<totalNumber:
            numbers = self.repo.GetNumber( repo_group_id, 60, 1000, "normal", "NO",myAccount )  # 取出t1条两小时内没有用过的号码
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell","am broadcast -a com.zunyun.zime.toast --es msg \"群号码库%s号仓库中该账号对应的数据取完，等待中\"" % repo_group_id ).communicate( )
                z.sleep( 10 )
                return
            list = numbers  # 将取出的号码保存到一个新的集合
            # print( list )
            # z.sleep(15)
            num = random.randint(0,len(list)-1)
            group = list[num]['name']
            print(group)
            z.sleep(3)
            z.heartbeat()

            d.server.adb.cmd( "shell",
                              'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=group"' % group ) #唤醒群
            z.heartbeat( )
            z.sleep(2)
            if d( text='TIM' ).exists:
                d( text='TIM' ).click( )
                time.sleep( 0.5 )
                while d( text='仅此一次' ).exists:
                    d( text='仅此一次' ).click( )

            if d( text='申请加群' ).exists:
                z.toast("该群未加入")
                self.repo.savePhonenumberXM( myAccount, repo_group_id, "N", group )
                continue
            if d(text="发消息").exists:
                d( text="发消息" ).click()
                z.sleep(2)
                z.heartbeat()
                obj = d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).left( index=0,resourceId="com.tencent.tim:id/input",className="android.widget.EditText" )
                if obj.exists:
                    obj.click( )
                    z.sleep( 1 )
                    z.input(message)
                    z.sleep(1)
                    z.heartbeat( )
                    if d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).exists:
                        d( text="发送", resourceId="com.tencent.tim:id/fun_btn" ).click( )
                        z.sleep( 1 )
                        self.repo.savePhonenumberXM( myAccount, repo_group_id, "Y", group )
                        n = n + 1

        z.toast("模块完成")
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return TIMGroupSendText

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT524SK00685")
    z = ZDevice("HT524SK00685")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_meg_id":"40","repo_group_id":"249","totalNumber":"5","time_delay":"3"}    #cate_id是仓库号，length是数量
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