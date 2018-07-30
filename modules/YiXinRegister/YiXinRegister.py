# coding:utf-8
import colorsys
import os
import random
import string

from PIL import Image

from imageCode import imageCode
from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from Repo import *
from zservice import ZDevice


class YiXinRegister:
    def __init__(self):
        self.repo = Repo()
        self.type = 'yixin'
        self.flag = False
        self.number = ''
        self.find = False

    def GenPassword(self, numOfNum=4, numOfLetter=4):
        # 选中numOfNum个数字
        slcNum = [random.choice(string.digits) for i in range(numOfNum)]
        # 选中numOfLetter个字母
        slcLetter = [random.choice(string.lowercase) for i in range(numOfLetter)]
        slcChar = slcLetter + slcNum
        genPwd = ''.join([i for i in slcChar])
        return genPwd

    def register(self, d, z, args, password):
        self.scode = smsCode(d.server.adb.device_serial())
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        z.toast(u"开始注册")
        d.server.adb.cmd("shell", "pm clear im.yixin").communicate()  # 清除缓存
        d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate()  # 拉起易信
        z.sleep(10)
        z.heartbeat()

        if d(resourceId='im.yixin:id/register_btn').exists:  # 点击注册
            d(resourceId='im.yixin:id/register_btn').click()
            z.sleep(2)

        # 取呢称素材库获取注册昵称
        material_cate_id = args['repo_material_id']
        # material_time_limit = args['material_time_limit']
        nicknameLsit = self.repo.GetMaterial(material_cate_id, 0, 1)
        if len(nicknameLsit) == 0:
            d.server.adb.cmd("shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"昵称素材库%s号仓库为空\"" % material_cate_id).communicate()
            self.flag = True
            return False

        nickname = nicknameLsit[0]['content']

        while True:
            z.heartbeat()
            z.toast(u'开始获取手机号')

            numberText = d(resourceId='im.yixin:id/register_phone_number_edittext').info['text']  # 将之前消息框的内容删除
            if numberText != '请输入手机号':  # 清空文本框上次输入的号码
                for objText in numberText:
                    d.press.delete()

            # 取号码库获取注册号码
            number_cate_id = args['repo_number_id']
            # number_time_limit = int(args['number_time_limit'])  # 号码提取时间间隔
            exist_numbers = self.repo.GetNumber(number_cate_id, 0, 1, 'exist')
            remain = 1 - len(exist_numbers)
            normal_numbers = self.repo.GetNumber(number_cate_id, 0, remain, 'normal')

            numbers = exist_numbers + normal_numbers
            if len(numbers) == 0:
                d.server.adb.cmd("shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空\"" % number_cate_id).communicate()
                self.flag = True
                return False

            number = numbers[0]["number"]

            if d(resourceId='im.yixin:id/register_phone_number_edittext').exists:
                d(resourceId='im.yixin:id/register_phone_number_edittext').click()

            # try:
            #     PhoneNumber = self.scode.GetPhoneNumber(self.scode.WECHAT_REGISTER, number)  # 获取接码平台手机号码
            # except:
            #     PhoneNumber = None

            PhoneNumber = self.scode.GetPhoneNumber(self.scode.WECHAT_REGISTER)  # 获取接码平台手机号码

            if PhoneNumber is None:
                self.scode.defriendPhoneNumber(PhoneNumber, self.scode.WECHAT_REGISTER)
                z.toast(u'讯码查不无此号,重新获取')
                continue
            else:
                z.toast(u'成功获取到手机号')

            z.input(PhoneNumber)

            if not d(text='中国', resourceId='im.yixin:id/tv_register_country').exists:
                d(resourceId='im.yixin:id/tv_register_country').click()
                z.sleep(1)
                while True:
                    if d(text='中国').exists:
                        d(text='中国').click()
                        break
                    else:
                        d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)

            if d(text='下一步').exists:
                d(text='下一步').click()
                z.sleep(8)

            if d(textContains='该手机号已被注册，是否现在登录').exists:
                d(text='是').click()
                z.sleep(2)

                if d(text='找回密码').exists:
                    d(text='找回密码').click()

                if d(text='下一步').exists:
                    d(text='下一步').click()
                    z.sleep(3)

                self.find = True

            z.heartbeat()
            if d(text='为了验证身份，我们将会发送短信验证码到你的手机').exists:
                self.scode.defriendPhoneNumber(PhoneNumber, self.scode.WECHAT_REGISTER)
                continue

            if d(textContains='验证码短信已发送至').exists:
                break

        try:
            code = self.scode.GetVertifyCode(PhoneNumber, self.scode.WECHAT_REGISTER, 4)  # 获取接码验证码
        except:
            code = ''

        self.scode.defriendPhoneNumber(PhoneNumber, self.scode.WECHAT_REGISTER)
        if code == '':
            z.toast(PhoneNumber + '手机号,获取不到验证码')
            return False

        for codeStr in code:
            z.input(codeStr)

        z.sleep(2)

        if self.find:
            z.input(password)
            z.sleep(2)

            d(text='完成').click()
            z.sleep(5)

        if d(resourceId='im.yixin:id/register_username_edittext').exists:
            d(resourceId='im.yixin:id/register_username_edittext').click()
            z.input(nickname)

        if d(resourceId='im.yixin:id/register_password_edittext').exists:
            d(resourceId='im.yixin:id/register_password_edittext').click()
            z.input(password)

        if d(text='下一步').exists:
            d(text='下一步').click()
            z.sleep(3)

        if d(text='完善信息').exists:
            d(index=1).click()
            z.sleep(1)
            ageArray = ['00后', '95后', '90后', '85后']
            age = ageArray[random.randint(0, 3)]
            if d(text=age).exists:
                d(text=age).click()

            if d(text='开启易信').exists:
                d(text='开启易信').click()
                z.sleep(10)

        if d(text='同意').exists:
            d(text='同意').click()

        while d(text='允许').exists:
            d(text='允许').click()
            z.sleep(2)

        z.heartbeat()
        if d(text='立即更新').exists and d(text='下次再说').exists:
            d(text='下次再说').click()

        if d(text='易信').exists and d(text='发现').exists and d(text='好友').exists and d(text='我').exists:
            z.toast(u'注册成功')
            self.number = PhoneNumber
            return True
        else:
            z.toast(u'注册失败，重新注册')
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
        featureCodeInfo = ''
        if len(remarkArr) == 3:
            slotInfo = d.server.adb.device_serial() + '_' + self.type + '_' + slotnum
            cateId = remarkArr[2]
            numbers = self.repo.Getserial(cateId, slotInfo)
            if len(numbers) > 0:
                featureCodeInfo = numbers[0]['imei']
                z.set_serial("im.yixin", featureCodeInfo)

        d.server.adb.cmd("shell", "pm clear im.yixin").communicate()  # 清除缓存

        self.slot.restore(slotnum)  # 有time_limit分钟没用过的卡槽情况，切换卡槽

        d.server.adb.cmd("shell",
                          "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为" + slotnum + "号\"").communicate()
        z.sleep(2)

        d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate()  # 拉起易信
        z.sleep(10)
        z.heartbeat()

        if d(text='很抱歉，“易信”已停止运行。').exists:
            d(text='确定').click()

        d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate()  # 拉起易信
        z.sleep(15)
        z.heartbeat()

        if d(text='同意').exists:
            d(text='同意').click()

        if d(text='立即更新').exists and d(text='下次再说').exists:
            d(text='下次再说').click()

        if d(text='你被服务器禁止登录，详询客服').exists:
            z.toast(u'切换帐号异常，重新补登')
            self.slot.clear(slotnum)  # 清空改卡槽，并补登
            if cateId != '':
                self.repo.BackupInfo(cateId, 'frozen', remarkArr[1], featureCodeInfo, '')  # 仓库号,使用中,QQ号,设备号_卡槽号
            return False

        if d(text='易信').exists and d(text='发现').exists and d(text='好友').exists and d(text='我').exists:
            self.flag = False
            return True
        else:
            z.toast(u'切换失败，重新补登')
            self.slot.clear(slotnum)  # 清空改卡槽，并补登
            if cateId != '':
                self.repo.BackupInfo(cateId, 'normal', remarkArr[1], featureCodeInfo, '')  # 仓库号,使用中,QQ号,设备号_卡槽号
            return False

    def action(self, d, z, args):

        while True:
            z.toast(u"正在ping网络是否通畅")
            while True:
                ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
                print(ping)
                if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                    z.toast(u"开始执行：易信注册模块　有卡槽")
                    break
                z.sleep(2)

            z.generate_serial("im.yixin")  # 随机生成手机特征码
            z.toast(u"随机生成手机特征码")

            serial = d.server.adb.device_serial()
            self.slot = Slot(serial, self.type)
            slotnum = self.slot.getEmpty()  # 取空卡槽

            if slotnum == 0 or self.flag:  # 没有空卡槽的话
                if self.qiehuan(d, z, args):
                    z.toast(u'切换成功,程序退出。')
                    break

            else:

                password = self.GenPassword()
                if self.register(d, z, args, password):
                    if self.number != '':
                        # 入库
                        featureCodeInfo = z.get_serial("im.yixin")
                        self.repo.RegisterAccount(self.number, password, "", args['repo_account_id'], "using", featureCodeInfo, '%s_%s_%s' % (
                                                       d.server.adb.device_serial(), self.type, slotnum))
                        # 入卡槽
                        self.slot.backup(slotnum, str(slotnum) + '_' + self.number + '_' + args['repo_account_id'])  # 设备信息，卡槽号，QQ号

                        break

        if (args['time_delay']):
            z.sleep(int(args['time_delay']))

def getPluginClass():
    return YiXinRegister

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("465b4e4b")
    z = ZDevice("465b4e4b")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "356", "repo_number_id": "305", "repo_material_id": "139", "slot_time_limit": "2", "time_delay": "3"};
    o.action(d, z, args)
    # slot = Slot(d.server.adb.device_serial(),'yixin')
    # slot.clear(1)
    # slot.clear(2)
    # d.server.adb.cmd("shell", "pm clear im.yixin").communicate()  # 清除缓存
    # slot.restore(1)
    # d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate()  # 拉起易信


