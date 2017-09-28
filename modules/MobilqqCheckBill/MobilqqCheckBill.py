# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class MobilqqCheckBill:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.toast( "QQ查话费资料入库" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ查话费资料入库" )
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
            z.toast( "卡槽状态正常，继续执行" )
        else:
            z.toast( "卡槽状态异常，跳过此模块" )
            return
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        repo_phone_id = int( args["repo_phone_id"] )  # 得到取号码的仓库号
        phone = self.repo.GetNumber( repo_phone_id, 60, 1, "normal", "NO" )  # 取出t1条两小时内没有用过的号码
        if len( phone ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"手机号码库%s号仓库为空，等待中\"" % repo_phone_id ).communicate( )
            z.sleep( 10 )
            return
        phone = phone[0]['number']
        print(phone)

        repo_number_id = args["repo_number_id"]

        repo_number_id = int( args["repo_number_id"] )  # 得到取号码的仓库号
        numbers = self.repo.GetAccount( repo_number_id, 60, 1 )
        while len( numbers ) == 0:
            z.heartbeat( )
            d.server.adb.cmd( "shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ帐号库%s号仓库无%s分钟未用,开始切换卡槽\"" % (
                repo_number_id, 60) ).communicate( )
            z.sleep( 2 )
            return 0

        QQNumber = numbers[0]['number']  # 即将登陆的QQ号
        information = args["repo_information_id"]
        print( QQNumber )
        d( index=0, resourceId="com.tencent.mobileqq:id/et_search_keyword", descriptionContains="搜索",
           className="android.widget.EditText" ).click( )
        time.sleep( 1 )
        z.input( QQNumber )
        # z.input("445564338")
        if d(index=1,className="android.widget.RelativeLayout").exists:
            z.heartbeat( )
            d(index=1,className="android.widget.RelativeLayout").click()
            z.sleep(2)
            d(index=5,resourceId="com.tencent.mobileqq:id/inputBar",className="android.widget.LinearLayout").click()
            z.sleep(1)
            msg = "查话费"+phone
            z.input(msg)
            z.sleep(1)
            z.heartbeat()
            d(text="发送",resourceId="com.tencent.mobileqq:id/fun_btn").click()
            z.sleep(8)
            for i in range(0,10):
                obj = d(index=i,className="android.widget.RelativeLayout").child(index=1,className="android.widget.TextView",resourceId="com.tencent.mobileqq:id/chat_item_content_layout")
                if obj.exists:
                    text = obj.info["text"]
                    if text==msg:
                        obj2 = d(index=i+1,className="android.widget.RelativeLayout").child(index=1,className="android.widget.TextView",resourceId="com.tencent.mobileqq:id/chat_item_content_layout")
                        if obj2.exists:
                            text2 = obj2.info["text"]
                            self.repo.uploadPhoneNumber( text2, information )
                            break
                        else:
                            z.toast("没有收到消息,停止模块")
                            return
        elif d(text="网络查找人和群:").exists:
            z.heartbeat()
            z.toast("请先加为好友")
            return
            # d( text="网络查找人和群:" ).click()
            # z.sleep(1)
            # if d(index=0,className="android.widget.AbsListView").child(index=1,className="android.widget.LinearLayout").exists:
            #     d( index=0, className="android.widget.AbsListView" ).child( index=1,className="android.widget.LinearLayout" ).click()
            #     z.sleep(1)
            #     if d(text="加好友").exists:
            #         d(text="加好友").click()
            #         z.sleep(1)
            #         z.heartbeat()
            #     if d(text="发送").exists:
            #         z.sleep(1)
            #         z.heartbeat()
            #         d( text="发送" ).click()
            #     if d(text="返回",resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").exists:
            #         z.sleep(1)
            #         z.heartbeat()
            #         d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click()
            #     if d(text="取消",resourceId="com.tencent.mobileqq:id/btn_cancel_search").exists:
            #         d( text="取消", resourceId="com.tencent.mobileqq:id/btn_cancel_search" ).click()
            #         z.sleep(1)
            #         z.heartbeat()
            #     if d(text="取消",resourceId="com.tencent.mobileqq:id/btn_cancel_search").exists:
            #         d( text="取消", resourceId="com.tencent.mobileqq:id/btn_cancel_search" ).click()
            #         z.sleep(1)
            #         z.heartbeat()
def getPluginClass():
    return MobilqqCheckBill

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT524SK00685")
    z = ZDevice("HT524SK00685")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_number_id":"228","repo_phone_id":"230","repo_information_id":"231","time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)

