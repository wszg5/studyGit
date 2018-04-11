# coding:utf-8

import random
from uiautomator import Device
from Repo import *
from util import logger
from zservice import ZDevice


class QQMailLogin:
    def __init__(self):
        self.repo = Repo()
        self.type = 'qqmail'

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 1000)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum


    def action(self, d,z,args):
        z.toast("正在ping网络是否通畅")
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast(u"网络通畅。开始执行：QQ邮箱登录 无卡槽" )
                break
            z.sleep(2)
        if i > 200:
            z.toast(u"网络不通，请检查网络状态" )
            return

        while True:
            try:
                d.server.adb.cmd("shell", "pm clear com.tencent.androidqqmail").communicate()  # 清除QQ邮箱缓存
                d.server.adb.cmd("shell",
                                  "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail").communicate()  # 拉起QQ邮箱

                z.sleep(8)
                z.heartbeat()
                if d(resourceId='com.tencent.androidqqmail:id/ea').exists:   # 选择QQ邮箱点击进入登陆页面
                    d(resourceId='com.tencent.androidqqmail:id/ea').click()
                    z.sleep(1)

                accounts = []
                while len(accounts) == 0:
                    accounts = self.repo.GetAccount( args['repo_account_id'], args['account_time_limit'], 1)  # 去仓库获取QQ邮箱帐号
                    if len(accounts) == 0:
                        z.toast(u"帐号库为空")

                account = accounts[0]['number']
                password = accounts[0]['password']

                if d(resourceId='com.tencent.androidqqmail:id/bi').exists:   # 输入邮箱帐号
                    d(resourceId='com.tencent.androidqqmail:id/bi').click()
                    z.input(account)

                if d(resourceId='com.tencent.androidqqmail:id/bs').exists:   # 输入邮箱密码
                    d(resourceId='com.tencent.androidqqmail:id/bs').click()
                    z.input(password)

                if d(resourceId='com.tencent.androidqqmail:id/a_').exists:   # 点击登录按钮
                    d(resourceId='com.tencent.androidqqmail:id/a_').click()

                z.sleep(12)
                z.heartbeat()
                if d(textContains='你有多个应用同时收到').exists:
                    d(text='确定').click()
                    z.sleep(2)

                if d(text='收件箱​').exists:
                    z.toast(u"登录成功。退出模块")
                    d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止
                    break
            except:
                logging.exception("exception")
                z.toast(u"程序出现异常，模块退出")
                d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止
                break




def getPluginClass():
    return QQMailLogin

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("25424f9")
    z = ZDevice("25424f9")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "331", "account_time_limit": "15"}
    o.action(d, z, args)

    # slot = Slot(d.server.adb.device_serial(),'qqmail')
    # slot.clear(2)
    # d.server.adb.cmd( "shell", "pm clear com.tencent.androidqqmail" ).communicate( )  # 清除缓存
    # slot.restore( 1 )
    # d.server.adb.cmd( "shell",
    #                   "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱

