# coding:utf-8
import random
import string
from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from Repo import *
from zservice import ZDevice


class YiXinLoginHaveSolt:
    def __init__(self):
        self.repo = Repo()
        self.type = 'yixin'
        self.flag = False
        self.featureCodeInfo = ''
        self.PhoneNumber = ''

    def login(self, d, z, args):
        z.toast("开始登录")
        d.server.adb.cmd("shell", "pm clear im.yixin").communicate()  # 清除缓存
        d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate()  # 拉起易信
        z.sleep(int(args['pull_up_time']))
        z.heartbeat()
        if d(text='很抱歉，“易信”已停止运行。').exists:
            if d(text='确定').exists:
                d(text='确定').click()
            if d(text='取消').exists:
                d(text='取消').click()
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

        cate_id = args["repo_account_id"]
        account_time_limit = args['account_time_limit']
        numbers = self.repo.GetAccount(cate_id, account_time_limit, 1)
        if len(numbers) == 0:
            z.heartbeat()
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ帐号库%s号仓库无%s分钟未用,开始切换卡槽\"" % (cate_id, account_time_limit)).communicate()
            self.flag = True
            return False


        featureCodeInfo = numbers[0]['imei']
        if not featureCodeInfo is None:
            z.set_serial("im.yixin", featureCodeInfo)
        else:
            z.generate_serial("im.yixin")  # 随机生成手机特征码
            self.featureCodeInfo = z.get_serial("im.yixin")

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

        z.sleep(int(args["pull_up_time"]))
        z.heartbeat()
        if d(text='立即更新').exists and d(text='下次再说').exists:
            d(text='下次再说').click()

        if d(text='易信').exists and d(text='发现').exists and d(text='好友').exists and d(text='我').exists:
            z.toast(u'登录成功')
            return True
        else:
            z.toast(u'登录失败，重新登录')
            return False

    def qiehuan(self, d, z, args):
        z.toast("开始切换卡槽")
        slot_time_limit = int(args['slot_time_limit'])  # 卡槽提取时间间隔
        try:
            slotObj = self.slot.getAvailableSlot(slot_time_limit)  # 取空卡槽，取N小时没用过的卡槽
        except:
            z.toast(u'获取卡槽异常')
            return False

        slotnum = None
        if not slotObj is None:
            slotnum = slotObj['id']

        while slotObj is None:  # 2小时没用过的卡槽也为没有的情况
            d.server.adb.cmd("shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"QQ卡槽全满，无间隔时间段未用\"").communicate()
            z.heartbeat()
            z.sleep(10)
            slotObj = self.slot.getAvailableSlot(slot_time_limit)
            if not slotObj is None:
                slotnum = slotObj['id']

        z.heartbeat()
        print(slotnum)

        obj = self.slot.getSlotInfo(slotnum)
        remark = obj['remark']
        remarkArr = remark.split("_")
        cateId = ''
        if len(remarkArr) == 3:
            slotInfo = d.server.adb.device_serial() + '_' + self.type + '_' + slotnum
            cateId = remarkArr[2]
            numbers = self.repo.Getserial(cateId, slotInfo)
            if len(numbers) > 0:
                featureCodeInfo = numbers[0]['imei']
                if not featureCodeInfo is None:
                    z.set_serial("im.yixin", featureCodeInfo)
                else:
                    z.generate_serial("im.yixin")  # 随机生成手机特征码
                    self.featureCodeInfo = z.get_serial("im.yixin")

        d.server.adb.cmd("shell", "pm clear im.yixin").communicate()  # 清除缓存

        self.slot.restore(slotnum)  # 有time_limit分钟没用过的卡槽情况，切换卡槽

        d.server.adb.cmd("shell",
                          "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为" + slotnum + "号\"").communicate()
        z.sleep(2)

        d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate()  # 拉起易信
        z.sleep(int(args['pull_up_time']))
        z.heartbeat()

        if d(text='很抱歉，“易信”已停止运行。').exists:
            if d(text='确定').exists:
                d(text='确定').click()
            if d(text='取消').exists:
                d(text='取消').click()

        d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate()  # 拉起易信
        z.sleep(int(args['pull_up_time']))
        z.heartbeat()

        if d(text='同意').exists:
            d(text='同意').click()

        z.sleep(int(args["pull_up_time"]))
        z.heartbeat()

        if d(text='立即更新').exists and d(text='下次再说').exists:
            d(text='下次再说').click()

        if d(text='你被服务器禁止登录，详询客服').exists or d(textContains='您的帐号暂时无法使用').exists:
            z.toast(u'切换帐号已被冻结，重新补登')
            self.slot.clear(slotnum)  # 清空改卡槽，并补登
            if cateId != '':
                self.repo.BackupInfo(cateId, 'frozen', remarkArr[1], self.featureCodeInfo, '')  # 仓库号,使用中,QQ号,设备号_卡槽号
            return False

        if d(text='易信').exists and d(text='发现').exists and d(text='好友').exists and d(text='我').exists:
            return True
        else:
            z.toast(u'切换失败，重新补登')
            self.slot.clear(slotnum)  # 清空改卡槽，并补登
            if cateId != '':
                self.repo.BackupInfo(cateId, 'normal', remarkArr[1], self.featureCodeInfo, '')  # 仓库号,使用中,QQ号,设备号_卡槽号
            return False

    def action(self, d, z, args):

        while True:
            z.toast("正在ping网络是否通畅")
            while True:
                ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
                print(ping)
                if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                    z.toast("开始执行：易信登录模块　有卡槽")
                    break
                z.sleep(2)

            serial = d.server.adb.device_serial()
            self.slot = Slot(serial, self.type)
            slotnum = self.slot.getEmpty()  # 取空卡槽

            if slotnum == 0 or self.flag:  # 没有空卡槽的话

                if self.qiehuan(d, z, args):
                    z.toast(u'切换成功,程序退出。')
                    break
            else:

                if self.login(d, z, args):

                    self.repo.BackupInfo(args["repo_account_id"], 'using', self.PhoneNumber, self.featureCodeInfo, '%s_%s_%s' % (
                                                       d.server.adb.device_serial(), self.type, slotnum))  # 仓库号,使用中,QQ号,设备号_卡槽号

                    self.slot.backup(slotnum, str(slotnum) + '_' + self.PhoneNumber + '_' + args['repo_account_id'])  # 设备信息，卡槽号，QQ号
                    break

                else:
                    if self.PhoneNumber != '':
                        if d(textContains='您的帐号暂时无法使用').exists:
                            self.repo.BackupInfo(args["repo_account_id"], 'frozen', self.PhoneNumber, '', '')  # 仓库号,使用中,QQ号
                        else:
                            self.repo.BackupInfo(args["repo_account_id"], 'normal', self.PhoneNumber, '', '')  # 仓库号,使用中,QQ号

                self.PhoneNumber = ''

        if (args['time_delay']):
            z.sleep(int(args['time_delay']))



def getPluginClass():
    return YiXinLoginHaveSolt

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT537SK00345")
    z = ZDevice("HT537SK00345")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "356", "slot_time_limit": "2", "account_time_limit": "0", "pull_up_time": "20", "time_delay": "3"}
    o.action(d, z, args)

    # slot = Slot(d.server.adb.device_serial(),'yixin')
    # slot.clear(1)
    # slot.clear(2)
    # d.server.adb.cmd("shell", "pm clear im.yixin").communicate()  # 清除缓存
    # slot.restore(1)
    # d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate()  # 拉起易信

