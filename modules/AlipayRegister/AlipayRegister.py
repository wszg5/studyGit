# coding:utf-8
from uiautomator import Device
from Repo import *
from zservice import ZDevice
from smsCode import smsCode

class AlipayRegister:
    def __init__(self):
        self.repo = Repo()
        self.__apk_pkgname = 'com.eg.android.AlipayGphone'

    def CheckLogined(self,d, z ):
        z.cmd("shell", "am force-stop com.eg.android.AlipayGphone")  # 强制停止
        z.cmd("shell", "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin")
        z.sleep(15)
        if d(textContains='口碑').exists:
            return True
        return False

    def action(self, d,z, args):
        z.heartbeat()
        pkginfo = z.server.adb.package_info(self.__apk_pkgname)
        if pkginfo is None:
            z.toast("没有安装支付宝，开始自行安装APP")
            z.cmd("shell", "pm uninstall com.eg.android.AlipayGphone")
            z.cmd("shell", "su -c 'rm -rf /data/data/com.eg.android.AlipayGphone'")
            z.cmd("install", "/apps/alipay.apk")
        elif args["checkLogin"] == "是" and self.CheckLogined(d, z) :
            z.toast("检测到已经登录，跳过注册")
            return

        #z.generateSerial()
        self.scode = smsCode(d.server.adb.device_serial())
        while True:
            z.heartbeat()
            d.server.adb.cmd("shell", "pm clear com.eg.android.AlipayGphone").communicate()  # 清除缓存
            # d.server.adb.cmd("shell", "am force-stop com.eg.android.AlipayGphone").wait()  # 强制停止
            d.server.adb.cmd("shell", "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin").communicate()  # 拉起来

            while not d(resourceId='com.ali.user.mobile.security.ui:id/registerButton').exists:
                z.toast("等待 新用户注册 按钮出现")
                d.dump(compressed=False)
                z.sleep(5)

            d(resourceId='com.ali.user.mobile.security.ui:id/registerButton').click()

            while not d(text='中国大陆').exists:
                d(resourceId='com.ali.user.mobile.security.ui:id/reg_region_name').click();
                z.sleep(1)
                d(text='中国大陆').click()

            if d(description='清空输入内容').exists:
                d(description='清空输入内容').click()

            #d(className='android.widget.ScrollView').child(className='android.widget.RelativeLayout',index=2).click()
            #d(text='请输入您的手机号').click()
            GetBindNumber = self.scode.GetPhoneNumber(self.scode.ALIPAY_REGISTER)

            d(resourceId='com.ali.user.mobile.security.ui:id/content').click()
            for i in GetBindNumber:
                z.input(i)


            #z.input(GetBindNumber)
            z.sleep(1)
            z.heartbeat()
            d(text='注册').click()


            if d(textContains='您的操作频率过快').exists or d(textContains='请将球滑向篮球框中').exists:
                self.scode.ReleasePhone(GetBindNumber, self.scode.ALIPAY_REGISTER)
                seconds = 5 * 60
                while seconds > 0:
                    z.heartbeat()
                    seconds = seconds - 5
                    z.toast("操作频率过快，休眠中，还剩余%s秒" % seconds)
                    z.sleep(5)
                z.toast("开始重装支付宝APP")
                z.cmd("shell", "pm uninstall com.eg.android.AlipayGphone")
                z.cmd("shell", "su -c 'rm -rf /data/data/com.eg.android.AlipayGphone'")
                z.cmd("install", "/apps/alipay.apk")
                z.cmd("shell", "reboot")



            code = self.scode.GetVertifyCode(GetBindNumber, self.scode.ALIPAY_REGISTER, 4)
            self.scode.ReleasePhone(GetBindNumber, self.scode.ALIPAY_REGISTER)

            if code == "":
                continue

            d(resourceId='com.ali.user.mobile.security.ui:id/box_input_wrapper').child(index=0).set_text(code)
            z.heartbeat()
            z.sleep(10)

            if d(textContains='立即登录').exists:
                d(text='立即登录').click()
                z.heartbeat()
                z.sleep(30)


            if d(textContains='设置登录密码').exists:
                password = 'Hello1234'
                d(text='请设置').set_text(password)
                z.sleep(1)
                d(text="确定").click()
                z.sleep(5)
                if args["repo_cate_id"]:
                    self.repo.RegisterAccount(GetBindNumber, password, GetBindNumber,  args["repo_cate_id"])
                    z.toast("账号已经入库")


            if d(textContains='身份验证').exists:
                continue

            if d(textContains='是我的，立即登录').exists:
                d(text='是我的，立即登录').click()

            times = 10
            while (times > 0):
                z.sleep(1)
                times = times - 1
                if d(description='全屏广告').exists:
                    d(description='推荐广告').click()
                    z.sleep(5)
                    d(description='返回').click()
                    break

            break

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return AlipayRegister

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("emulator-5554")
    z = ZDevice("emulator-5554")
    print (z.getTopActivity())
    z.generateSerial()

    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").wait()
    args = {"checkLogin": "否","repo_number_id": "136","time_delay": "3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

