# coding:utf-8
from uiautomator import Device
from Repo import *
from zservice import ZDevice
from smsCode import smsCode

class AlipayLogin:
    def __init__(self):
        self.repo = Repo()

    def CheckLogined(self,d, z ):
        z.cmd("shell", "am force-stop com.eg.android.AlipayGphone")  # 强制停止
        z.cmd("shell", "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin")
        z.sleep(15)
        if d(textContains='口碑').exists:
            return True
        return False

    def action(self, d,z, args):
        z.heartbeat()
        if args["checkLogin"] == "是" and self.CheckLogined(d, z) :
            z.toast("检测到已经登录，跳过登录")
            return

        while True:
            z.heartbeat()
            d.server.adb.cmd("shell", "pm clear com.eg.android.AlipayGphone").communicate()  # 清除缓存
            # d.server.adb.cmd("shell", "am force-stop com.eg.android.AlipayGphone").wait()  # 强制停止
            d.server.adb.cmd("shell", "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin").communicate()  # 拉起来
            while not d(resourceId='com.ali.user.mobile.security.ui:id/loginButton').exists:
                z.toast("等待登录按钮出现")
                z.sleep(2)
            d(resourceId='com.ali.user.mobile.security.ui:id/loginButton').click()

            accountObj = self.repo.GetAccount(args["repo_cate_id"], args["account_pick_interval"], 1)
            while len(accountObj) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"帐号库%s号仓库为空，等待中\"" % args["repo_cate_id"]).communicate()
                z.sleep(10)

            aNumber = accountObj[0]['number']  # 即将登陆的QQ号
            aPassword = accountObj[0]['password']

            d(resourceId="com.ali.user.mobile.security.ui:id/content").set_text(aNumber)
            z.sleep(2)
            d(resourceId="com.ali.user.mobile.security.ui:id/userPasswordInput").set_text(aPassword)
            z.sleep(2)
            d(text='登录').click()
            z.sleep(2)

            if d(textContains='账号不存在').exists:
                self.repo.PostStatus(args["repo_cate_id"],"not_exist",aNumber)
                continue

            if d(textContains='您的操作频率过快').exists:
                z.generateSerial()
                z.sleep(5)
                z.cmd("shell", "reboot")

            if d(textContains='请将球滑向篮球框中').exists:
                z.generateSerial()
                z.sleep(5)
                z.cmd("shell", "reboot")


            times = 10
            while (times > 0):
                z.sleep(1)
                times = times - 1
                if d(description='全屏广告').exists:
                    d(description='推荐广告').click()
                    z.sleep(5)
                    break

            break

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return AlipayLogin

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4AVSK01106")
    z = ZDevice("HT4AVSK01106")
    z.server.install();
    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").wait()

    while not d(resourceId='com.ali.user.mobile.security.ui:id/loginButton').exists:
        z.toast("等待登录按钮出现")
        z.sleep(2)
    d(resourceId='com.ali.user.mobile.security.ui:id/loginButton').click()


    d(resourceId="com.ali.user.mobile.security.ui:id/content").set_text("13858528")
    d(resourceId="com.ali.user.mobile.security.ui:id/userPasswordInput").set_text("112233")

    d.server.adb.cmd("shell", "pm clear com.eg.android.AlipayGphone").communicate()  # 清除缓存
    # d.server.adb.cmd("shell", "am force-stop com.eg.android.AlipayGphone").wait()  # 强制停止
    d.server.adb.cmd("shell",
                     "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin").communicate()  # 拉起来

    if d(textContains='您的操作频率过快').exists:
        z.generateSerial()
        d(text='注册').click()

    if d(description='清空输入内容').exists:
        d(description='清空输入内容').click()
    #d(resourceId='com.ali.user.mobile.security.ui:id/box_input_wrapper').child(index=0).set_text("0222")
    #d(text="确定").click()
    # z.input('177751880')
    # z.input('13141314ABC')
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"checkLogin": "否","repo_number_id": "136","time_delay": "3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

