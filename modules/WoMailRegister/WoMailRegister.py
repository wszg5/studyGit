# coding:utf-8
import random
import re
import string
from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from Repo import *
from zservice import ZDevice


class WoMailRegister:
    def __init__(self):
        self.repo = Repo()
        self.type = ''

    def register(self, d, z, args):
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd( "shell", "pm clear com.asiainfo.android" ).communicate( )  # 清除缓存

        d.server.adb.cmd( "shell",
                          "am start -n com.asiainfo.android/com.asiainfo.mail.ui.mainpage.SplashActivity" ).communicate( )  # 拉起沃邮箱

        z.sleep(8)
        if d(text='任意账号登录').exists:
            for k in range(1, 10):
                d.swipe( width * 0.75, height * 0.5, width * 0.05, height * 0.5, 10 )
                time.sleep(2)
                if d(text='便捷任务管理').exists:
                    d( resourceId='com.asiainfo.android:id/guide_startbtn', index=2, text='全新体验 马上开始' ).click( )
                    z.sleep(3)
                    break

        i = 0
        while d(text='没邮箱？小沃送您啦').exists:
            d( text='没邮箱？小沃送您啦' ).click( )
            z.sleep( 20 )
            if d(text='没邮箱？小沃送您啦').exists:
                if i == 3:
                    break
                else:
                    i += 1
                    continue
        d.server.adb.cmd( "shell",
                          "am start -n com.asiainfo.android/com.asiainfo.mail.ui.mainpage.SplashActivity" ).communicate( )  # 拉起沃邮箱
        z.sleep(5)
        if d(text='【添加】更多邮箱账号').exists:
            d(text='取消').click()
            z.sleep(2)

        if d(text='好记的别名').exists:
            d(text='先用着').click()
            z.sleep(2)

        if d(text='中国联通沃邮箱欢迎邮件').exists:
            d(text='中国联通沃邮箱欢迎邮件').click()
            z.sleep(2)

        if d(resourceId='com.asiainfo.android:id/iv_task').exists:
            d( resourceId='com.asiainfo.android:id/iv_task' ).click()
            woMail_info = d(resourceId='com.asiainfo.android:id/activity_newtask_content').info['text']
            account_start = woMail_info.find( '账号：' ) + 3
            account_end = woMail_info.find( ' 密码：' )
            account =  woMail_info[account_start:account_end]

            password_start = woMail_info.find('密码：') + 3
            password_end = woMail_info.find(' 祝您')
            password = woMail_info[password_start:password_end]

            result = account + "/" + password

            return result

        else:
            z.toast("注册失败，重新注册。")
            return 'fail'



    def action(self, d, z, args):
        while True:
            z.toast( "正在ping网络是否通畅" )
            while True:
                ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
                print(ping)
                if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                    z.toast("开始执行：沃邮箱注册模块　有卡槽")
                    break
                z.sleep( 2 )

            z.generate_serial( "com.asiainfo.android" )
            z.toast("随机生成特征码")

            saveCate = args['repo_account_id']
            register_result = self.register(d, z, args)
            featureCodeInfo = z.get_serial( "com.asiainfo.android" )
            if register_result == "fail":
                continue

            else:
                # 入库
                info = register_result.split("/")
                self.repo.RegisterAccount( info[0], info[1], "", saveCate, "using", featureCodeInfo )
                break

        if (args['time_delay']):
            z.sleep(int(args['time_delay']))



def getPluginClass():
    return WoMailRegister

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("25424f9")
    z = ZDevice("25424f9")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "293", "slot_time_limit": "2", "account_time_limit": "0", "time_delay": "3"};
    o.action(d, z, args)



        # d.server.adb.cmd( "shell", "pm clear com.asiainfo.android" ).communicate( )  # 清除缓存
    #
    # d.server.adb.cmd( "shell", "am start -n com.asiainfo.android/com.asiainfo.mail.ui.mainpage.SplashActivity" ).communicate()  # 拉起沃邮箱
    # d.server.adb.cmd( "shell", "am force-stop com.asiainfo.android" ).communicate( )  # 强制停止
    # d.server.adb.cmd( "shell",
    #                   "am start -n com.asiainfo.android/com.asiainfo.mail.ui.mainpage.SplashActivity" ).communicate( )  # 拉起沃邮箱
    # d.server.adb.cmd( "shell",
    #                   "am start -n com.asiainfo.android/com.asiainfo.mail.ui.mainpage.MainActivity").communicate( )  # 拉起沃邮箱

