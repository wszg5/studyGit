# coding:utf-8
import colorsys
import os
import random

from PIL import Image

from imageCode import imageCode
from slot import Slot
from smsCode import smsCode
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

    def palyCode(self, d, z, picObj):
        self.scode = smsCode(d.server.adb.device_serial())
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        codePng = os.path.join(base_dir, "%s_c.png" % (self.GetUnique()))
        icode = imageCode()
        im_id = ""
        code = ""
        for i in range(0, 2):  # 打码循环
            if i > 0:
                icode.reportError(im_id)
            obj = picObj.info
            obj = obj['bounds']  # 验证码处的信息
            left = obj["left"]  # 验证码的位置信息
            top = obj['top']
            right = obj['right']
            bottom = obj['bottom']

            d.screenshot(sourcePng)  # 截取整个输入验证码时的屏幕

            img = Image.open(sourcePng)
            box = (left, top, right, bottom)  # left top right bottom
            region = img.crop(box)  # 截取验证码的图片

            img = Image.new('RGBA', (right - left, bottom - top))
            img.paste(region, (0, 0))

            img.save(codePng)
            im = open(codePng, 'rb')

            codeResult = icode.getCode(im, icode.CODE_TYPE_4_NUMBER_CHAR, 60)

            code = codeResult["Result"]
            im_id = codeResult["Id"]
            os.remove(sourcePng)
            os.remove(codePng)
            z.heartbeat()
            if code.isalpha() or code.isisdigitv() or code.isalnum():
                break
            else:
                continue

        return code


    def login(self, d, z, args, accounts):
        try:
            d.server.adb.cmd("shell", "pm clear com.tencent.androidqqmail").communicate()  # 清除QQ邮箱缓存
            d.server.adb.cmd("shell", "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail").communicate()  # 拉起QQ邮箱

            z.sleep(8)
            z.heartbeat()
            if d(resourceId='com.tencent.androidqqmail:id/ea').exists:  # 选择QQ邮箱点击进入登陆页面
                d(resourceId='com.tencent.androidqqmail:id/ea').click()
                z.sleep(1)

            account = accounts[0]['number']
            password = accounts[0]['password']

            if d(text='帐号密码登录').exists:
                d(text='帐号密码登录').click()

            if d(resourceId='com.tencent.androidqqmail:id/bi').exists:  # 输入邮箱帐号
                d(resourceId='com.tencent.androidqqmail:id/bi').click()
                z.input(account)

            if d(resourceId='com.tencent.androidqqmail:id/bs').exists:  # 输入邮箱密码
                d(resourceId='com.tencent.androidqqmail:id/bs').click()
                z.input(password)

            if d(resourceId='com.tencent.androidqqmail:id/a_').exists:  # 点击登录按钮
                d(resourceId='com.tencent.androidqqmail:id/a_').click()

            z.sleep(3)
            if d(resourceId='com.tencent.androidqqmail:id/a16').exists:  # 出现验证码
                picObj = d(resourceId='com.tencent.androidqqmail:id/a19', index=0)
                code = self.palyCode(d, z, picObj)
                if code == "":
                    return False
                if d(resourceId='com.tencent.androidqqmail:id/a17').exists:
                    d(resourceId='com.tencent.androidqqmail:id/a17').click()
                z.input(code)
                if d(resourceId='com.tencent.androidqqmail:id/a_').exists:  # 点击登陆
                    d(resourceId='com.tencent.androidqqmail:id/a_').click()

            z.sleep(12)
            z.heartbeat()
            if d(textContains='你有多个应用同时收到').exists:
                d(text='确定').click()
                z.sleep(2)

            if d(text='收件箱​').exists:
                z.toast(u"登录成功。退出模块")
                d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止
                return True
        except:
            logging.exception("exception")
            z.toast(u"程序出现异常，模块退出")
            d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止
            return False

    def qiehuan(self, d, z, args):
        time_limit = int(args['slot_time_limit'])
        serial = d.server.adb.device_serial()
        self.slot = Slot(serial, self.type)
        slotObj = self.slot.getAvailableSlot(time_limit)  # 没有空卡槽，取２小时没用过的卡槽

        slotnum = None
        if not slotObj is None:
            slotnum = slotObj['id']

        while slotObj is None:  # 2小时没用过的卡槽也为没有的情况
            d.server.adb.cmd("shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"QQ卡槽全满，无间隔时间段未用\"").communicate()
            z.heartbeat()
            z.sleep(30)
            slotObj = self.slot.getAvailableSlot(time_limit)
            if not slotObj is None:
                slotnum = slotObj['id']
                break

        z.heartbeat()
        d.server.adb.cmd("shell", "pm clear com.tencent.androidqqmail").communicate()  # 清除缓存

        obj = self.slot.getSlotInfo(slotnum)
        remark = obj['remark']
        remarkArr = remark.split("_")
        cateId = args['repo_account_id']
        if len(remarkArr) == 3:
            slotInfo = d.server.adb.device_serial() + '_' + self.type + '_' + slotnum
            cateId = remarkArr[2]
            numbers = self.repo.Getserial(cateId, slotInfo)
            if len(numbers) != 0:
                featureCodeInfo = numbers[0]['imei']
                z.set_serial("com.tencent.androidqqmail", featureCodeInfo)

        self.slot.restore(slotnum)  # 有time_limit分钟没用过的卡槽情况，切换卡槽
        z.sleep(2)

        d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为" + slotnum + "号\"").communicate()
        z.sleep(2)
        d.server.adb.cmd("shell", "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail").communicate()  # 拉起QQ邮箱
        z.sleep(5)
        while d(textContains='正在更新数据').exists:
            z.sleep(2)
        z.sleep(20)

        z.heartbeat()
        d.dump(compressed=False)
        if d(text='密码错误，请重新输入').exists or d(description='QQ邮箱').exists:
            QQnumber = remarkArr[1]
            self.repo.BackupInfo(cateId, 'normal', QQnumber, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber

            self.slot.clear(slotnum)  # 清空改卡槽，并补登
            z.toast("卡槽邮箱号状态异常，补登陆卡槽")
            return False

        else:
            z.toast("邮箱登陆状态正常，切换完毕。")
            return True

    def action(self, d, z, args):

        while True:
            z.toast("正在ping网络是否通畅")
            i = 0
            while i < 200:
                i += 1
                ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
                print(ping)
                if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                    z.toast(u"网络通畅。开始执行：QQ邮箱登录 有卡槽")
                    break
                z.sleep(2)
            if i > 200:
                z.toast(u"网络不通，请检查网络状态")
                return

            z.heartbeat()
            z.generate_serial("com.tencent.androidqqmail")  # 随机生成手机特征码

            accounts = self.repo.GetAccount(args['repo_account_id'], int(args['account_time_limit']), 1)  # 去仓库获取QQ邮箱帐号
            if len(accounts) == 0:
                z.toast(u"帐号库为空")

            serial = d.server.adb.device_serial()
            self.slot = Slot(serial, self.type)
            slotnum = self.slot.getEmpty()  # 取空卡槽
            if slotnum == 0 or len(accounts) == 0:  # 没有空卡槽的话或者仓库没有可登陆的帐号，进行卡槽切换。

                if self.qiehuan(d, z, args):
                    break
                else:
                    continue

            else:  # 有空卡槽的情况

                QQnumber = accounts[0]['number']
                print QQnumber
                if self.login(d, z, args, accounts):
                    z.heartbeat()
                    featureCodeInfo = z.get_serial("com.tencent.androidqqmail")
                    self.slot.backup(slotnum, str(slotnum) + '_' + QQnumber + '_' + args["repo_account_id"])  # 设备信息，卡槽号，QQ号
                    self.repo.BackupInfo(args["repo_account_id"], 'using', QQnumber, featureCodeInfo, '%s_%s_%s' % (
                        d.server.adb.device_serial(), self.type, slotnum))  # 仓库号,使用中,QQ号,设备号_卡槽号
                    break

                else:
                    self.slot.clear(slotnum)  # 清空改卡槽，并补登
                    continue



def getPluginClass():
    return QQMailLogin

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("465b4e4b")
    z = ZDevice("465b4e4b")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "331", "account_time_limit": "120", "slot_time_limit": "1"};
    o.action(d, z, args)
    # slot = Slot(d.server.adb.device_serial(),'qqmail')
    # slot.clear(1)
    # d.server.adb.cmd("shell", "pm clear com.tencent.androidqqmail").communicate()  # 清除缓存
    # slot.restore(1)
    # d.server.adb.cmd("shell",
    #                    "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail").communicate()  # 拉起QQ邮箱
    # picObj = d(resourceId='com.tencent.androidqqmail:id/a19', className='android.widget.ImageView')
    # if picObj.exists:
    #     code = o.palyCode(d, z, picObj)
    # if d(description='QQ邮箱').exists:
    #     d(description='QQ邮箱').click()
    #
    # if d(resourceId='com.tencent.androidqqmail:id/ea').exists:
    #     d(resourceId='com.tencent.androidqqmail:id/ea').click()

