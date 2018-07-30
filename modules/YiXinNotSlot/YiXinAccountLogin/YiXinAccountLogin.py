# coding:utf-8
import random
import string
from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from Repo import *
from zservice import ZDevice


class YiXinAccountLogin:
    def __init__(self):
        self.repo = Repo()
        self.type = 'yixin'
        self.featureCodeInfo = ''
        self.PhoneNumber = ''

    def login(self, d, z, args):
        z.toast("开始登录")
        d.server.adb.cmd("shell", "pm clear im.yixin").communicate()  # 清除缓存
        d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate()  # 拉起易信
        z.sleep(int(args['pull_up_time']))
        z.heartbeat()
        if d(text='很抱歉，“易信”已停止运行。').exists:
            d(text='确定').click()
            return False

        # d.server.adb.cmd("shell", "am force-stop im.yixin").communicate()  # 强制停止
        # d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate()  # 拉起易信
        # z.sleep(5)
        # z.heartbeat()
        # if d(text='很抱歉，“易信”已停止运行。').exists:
        #     d(text='确定').click()
        #     return 'fail'

        if d(text='接受', resourceId='im.yixin:id/easy_dialog_positive_btn').exists:
            d(text='接受', resourceId='im.yixin:id/easy_dialog_positive_btn').click()
            z.sleep(2)

        if d(resourceId='im.yixin:id/login_btn').exists:
            d(resourceId='im.yixin:id/login_btn').click()
            z.sleep(2)

        if d(resourceId='im.yixin:id/login_btn').exists:
            d(resourceId='im.yixin:id/login_btn').click()
            z.sleep(2)

        z.toast(u"开始获取手机号码")
        while True:
            cate_id = args["repo_account_id"]
            account_time_limit = args['account_time_limit']
            numbers = self.repo.GetAccount(cate_id, account_time_limit, 1)
            if len(numbers) == 0:
                z.heartbeat()
                d.server.adb.cmd("shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ帐号库%s号仓库无%s分钟未用,开始切换卡槽\"" % (
                                      cate_id, account_time_limit)).communicate()
                z.sleep(2)
            else:
                break

        featureCodeInfo = numbers[0]['imei']
        if not featureCodeInfo is None:
            z.set_serial("im.yixin", featureCodeInfo)
        else:
            z.generate_serial("im.yixin")  # 随机生成手机特征码
            self.featureCodeInfo = z.get_serial("im.yixin")
            z.toast("随机生成手机特征码")

        PhoneNumber = numbers[0]['number']  # 即将登陆的QQ号
        Password = numbers[0]['password']
        self.PhoneNumber = PhoneNumber

        if d(resourceId='im.yixin:id/editUserid').exists:
            d(resourceId='im.yixin:id/editUserid').click.bottomright()
            z.sleep(1)
            d(resourceId='im.yixin:id/editUserid').click()
            z.input(PhoneNumber)

        if d(resourceId='im.yixin:id/editPassword').exists:
            d(resourceId='im.yixin:id/editPassword').click.bottomright()
            z.sleep(1)
            d(resourceId='im.yixin:id/editPassword').click()
            z.input(Password)

        if d(resourceId='im.yixin:id/btn_login').exists:
            d(resourceId='im.yixin:id/btn_login').click()
            z.sleep(15)

        z.heartbeat()
        if d(text='同意').exists:
            d(text='同意').click()

        while d(text='允许').exists:
            d(text='允许').click()
            z.sleep(2)

        z.sleep(5)
        z.heartbeat()
        if d(text='立即更新').exists and d(text='下次再说').exists:
            d(text='下次再说').click()

        if d(text='易信').exists and d(text='发现').exists and d(text='好友').exists and d(text='我').exists:
            z.toast(u'登录成功')
            return True
        else:
            z.toast(u'登录失败，重新登录')
            return False

    def action(self, d, z, args):

        while True:
            z.toast("正在ping网络是否通畅")
            while True:
                ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
                print(ping)
                if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                    z.toast("开始执行：易信登录模块　无卡槽")
                    break
                z.sleep(2)

            if self.login(d, z, args):

                self.repo.BackupInfo( args["repo_account_id"], 'using', self.PhoneNumber, self.featureCodeInfo, '')  # 仓库号,使用中,QQ号,设备号_卡槽号
                break

            else:
                if d(textContains='您的帐号暂时无法使用').exists:
                    self.repo.BackupInfo(args["repo_account_id"], 'frozen', self.PhoneNumber, '', '')  # 仓库号,使用中,QQ号
                else:
                    self.repo.BackupInfo(args["repo_account_id"], 'normal', self.PhoneNumber, '', '')  # 仓库号,使用中,QQ号

        if (args['time_delay']):
            z.sleep(int(args['time_delay']))



def getPluginClass():
    return YiXinAccountLogin

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT537SK00345")
    z = ZDevice("HT537SK00345")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "356", "account_time_limit": "0", "pull_up_time": "20", "time_delay": "3"}
    o.action(d, z, args)

    # slot = Slot(d.server.adb.device_serial(),'yixin')
    # slot.clear(1)
    # slot.clear(2)
    # d.server.adb.cmd("shell", "pm clear im.yixin").communicate()  # 清除缓存
    # slot.restore(1)
    # d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate()  # 拉起易信

