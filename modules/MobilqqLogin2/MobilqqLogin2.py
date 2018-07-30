# coding:utf-8
import datetime
import os
import random
import time

from PIL import Image

import util
from Repo import *
from imageCode import imageCode
from slot import Slot
from uiautomator import Device
from zservice import ZDevice


class MobilqqLogin2:
    def __init__(self):
        self.type = 'mobileqq'
        self.repo = Repo()
        self.slot = Slot('', self.type)
        self.logger = util.logger

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum


    def login(self,d,args,z):
        z.heartbeat()
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        codePng = os.path.join(base_dir, "%s_c.png" % (self.GetUnique()))
        cate_id = args["repo_cate_id"]

        while True:
            time_limit1 = args['time_limit1']
            numbers = self.repo.GetAccount(cate_id, time_limit1, 1)
            t = 30
            while len(numbers) == 0:
                z.heartbeat()

                z.toast('QQ帐号库%s号仓库无%s分钟未用，即将跳出 %s' % (cate_id,time_limit1, t ))
                numbers = self.repo.GetAccount(cate_id, time_limit1, 1)
                z.sleep(2)
                t = t - 2
                if t <=0 :
                    return None

            QQNumber = numbers[0]['number']  # 即将登陆的QQ号
            QQPassword = numbers[0]['password']
            z.sleep(1)
            z.heartbeat()
            z.cmd("shell", "pm clear com.tencent.mobileqq")  # 清除缓存
            z.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity")  # 拉起来
            while d(textContains='正在更新数据').exists:
                z.sleep(3)

            z.heartbeat()
            t = 15
            z.toast("等待 登录 按钮出现")
            while not d(resourceId='com.tencent.mobileqq:id/btn_login').exists:
                z.toast("等待 登录 按钮出现 %s" % t)
                dumpStr = d.dump(compressed=False)
                z.sleep(2)
                if t == 9:
                    self.logger.war(dumpStr)
                t = t - 2
            d(resourceId='com.tencent.mobileqq:id/btn_login').click()

            z.sleep(1)
            d(className='android.widget.EditText', index=0).click()
            d(className='android.widget.EditText', index=0).set_text(QQNumber)  # ﻿1918697054----xiake1234.  QQNumber
            z.sleep(1)
            d(resourceId='com.tencent.mobileqq:id/password').set_text(QQPassword)  # Bn2kJq5l     QQPassword
            z.heartbeat()
            print('QQ号:%s,QQ密码：%s'%(QQNumber,QQPassword))
            d(resourceId='com.tencent.mobileqq:id/login').click()
            if d(text='QQ').exists:
                d(text='QQ').click()
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()
            z.sleep(1)
            while d(text='登录中').exists:
                z.sleep(2)
            z.sleep(4)
            z.heartbeat()
            if d(resourceId='com.tencent.mobileqq:id/name', index='2',className="android.widget.EditText").exists:  # 需要验证码的情况
                icode = imageCode()
                im_id = ""
                for i in range(0, 30, +1):  # 打码循环
                    if i > 0:
                        icode.reportError(im_id)
                    obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.ImageView')      #当弹出选择QQ框的时候，定位不到验证码图片
                    obj = obj.info
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

                    codeResult = icode.getCode(im, icode.CODE_TYPE_4_NUMBER_CHAR)

                    code = codeResult["Result"]
                    im_id = codeResult["Id"]
                    os.remove(sourcePng)
                    os.remove(codePng)
                    z.heartbeat()
                    d(resourceId='com.tencent.mobileqq:id/name', index='2',className="android.widget.EditText").set_text(code)
                    z.sleep(3)
                    d(text='完成', resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText').click()
                    z.sleep(6)
                    z.heartbeat()
                    while d(className='android.widget.ProgressBar',index=0).exists:        #网速不给力时，点击完成后仍然在加载时的状态
                        z.sleep(2)
                    z.sleep(3)
                    z.heartbeat()
                    if d(text='输入验证码',resourceId='com.tencent.mobileqq:id/ivTitleName').exists:
                        continue
                    else:
                        break

            else:
                d.server.adb.cmd("shell", "am force-stop com.tencent1314.mobileqq").communicate()  # 强制停止
                z.sleep(1)
                d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
                z.sleep(4)
            z.heartbeat()
            if d(text='搜索', resourceId='com.tencent.mobileqq:id/name').exists:  # 不需要验证码的情况
                return QQNumber
            z.sleep(1)
            if d(text='马上绑定').exists:
                return QQNumber
            z.sleep(1)
            if d(text='通讯录').exists:              #登陆上后弹出t通讯录的情况
                return QQNumber
            if d(textContains='更换主题').exists:
                return QQNumber
            if d(text='寻找好友').exists:
                return QQNumber
            if d(textContains='密码错误').exists:
                self.logger.info('===========密码错误==============帐号:%s,密码:%s' % (QQNumber, QQPassword))
            z.heartbeat()
            self.repo.BackupInfo(cate_id, 'frozen', QQNumber, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
            z.sleep(1)
            if d(text='帐号无法登录').exists:
                d(text='取消').click()
            continue

    def action(self, d,z, args):
        z.heartbeat()
        d.dump(compressed=False)
        time_limit = args['time_limit']
        cate_id = args["repo_cate_id"]
        slotnum = self.slot.getEmpty()  # 取空卡槽

        print(slotnum)
        if slotnum == 0:    #没有空卡槽的话
            slotnum = self.slot.getSlot(d, time_limit)  # 没有空卡槽，取２小时没用过的卡槽
            print(slotnum)
            while slotnum == 0:  # 2小时没有用过的卡槽也为空的情况
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ卡槽全满，无间隔时间段未用\"").communicate()
                z.heartbeat()
                z.sleep(30)
                slotnum = self.slot.getSlot(d, time_limit)
            z.heartbeat()
            d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存

            getSerial = self.repo.Getserial(cate_id,'%s_%s_%s' % (d.server.adb.device_serial(),self.type, slotnum))     #得到之前的串号
            time.sleep(1)
            if len(getSerial)==0:      #之前的信息保存失败的话
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"串号获取失败，重新设置\"" ).communicate()   #在５１上测时库里有东西但是王红机器关闭后仍获取失败
                print('切换失败')
                getSerial = z.generateSerial("788")  # 修改信息
            else:
                getSerial = getSerial[0]['imei']      #如果信息保存成功但串号没保存成功的情况
                print('卡槽切换时的sereial%s'%getSerial)
                if getSerial is None:          #如果串号为空，在该卡槽下保存新的串号
                    getSerial = z.generateSerial("788")  # 修改信息
                else:
                    z.generateSerial(getSerial)  # 将串号保存
            z.heartbeat()
            self.slot.restore(d, slotnum)  # 有time_limit分钟没用过的卡槽情况，切换卡槽
            z.heartbeat()
            while True:
                ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
                print(ping)
                if 'icmp_seq'and 'bytes from'and'time' in ping[0]:
                    break
                z.sleep(2)
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为"+str(slotnum)+"号\"").communicate()
            z.sleep(2)
            if d(textContains='主题装扮').exists:
                d(text='关闭').click()
                z.sleep(1)

            d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            z.sleep(2)
            z.heartbeat()
            while d(textContains='正在更新数据').exists:
                z.sleep(2)
            z.sleep(5)
            z.heartbeat()
            if d(textContains='主题装扮').exists:
                d(text='关闭').click()
                z.sleep(1)



            loginedFlag = True

            seconds = 15
            while seconds > 0:
                z.toast('检查是否出现登录界面%s' % seconds)
                seconds = seconds - 1
                z.sleep(1)

                if z.checkTopActivity("com.tencent.mobileqq/.activity.RegisterGuideActivity") \
                    or z.checkTopActivity("com.tencent.mobileqq/.activity.LoginActivity") \
                    or d(textContains='身份过期').exists:
                    loginedFlag = False
                    break


            obj = self.slot.getSlotInfo(d, slotnum)  # 得到切换后的QQ号
            QQnumber = obj['info']  # info为QQ号
            if loginedFlag:
                z.toast(u'卡槽恢复成功')
                z.heartbeat()
                self.slot.backup(d, slotnum, QQnumber)  # 设备信息，卡槽号，QQ号
                self.repo.BackupInfo(cate_id, 'using', QQnumber,getSerial,'%s_%s_%s' % (d.server.adb.device_serial(),self.type, slotnum))  # 仓库号，状态，QQ号，备注设备id_卡槽id
            else:        #切换不成功的情况
                #z.toast(u'卡槽恢复失败，开始补登')
                self.repo.BackupInfo(cate_id, 'frozen', QQnumber, '','')  # 标记卡槽号码为冻结，仓库号，状态，QQ号，备注设备id_卡槽id
                z.cmd("shell", "pm clear com.tencent.mobileqq")  # 清除缓存
                serialinfo = z.generateSerial("788")  # 修改信息
                z.heartbeat()
                z.toast(u'卡槽恢复失败，开始补登')
                QQnumber = self.login(d, args,z)  # 帐号无法登陆则登陆,重新登陆
                if QQnumber:
                    self.slot.backup(d, slotnum, QQnumber)  # 登陆之后备份,将备份后的信息传到后台　仓库号，状态，QQ号，备注设备id_卡槽id
                    self.repo.BackupInfo(cate_id, 'using', QQnumber,serialinfo,'%s_%s_%s' % (d.server.adb.device_serial(), self.type, slotnum))  # 仓库号,使用中,QQ号,设备号_卡槽号

                else:
                    z.toast(u'补登失败了 :(')

        else:  # 有空卡槽的情况
            d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存

            z.heartbeat()
            while True:
                ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
                print(ping)
                if 'icmp_seq'and 'bytes from'and'time' in ping[0]:
                    break
                z.sleep(2)
            serialinfo = z.generateSerial("788")    #修改串号等信息
            print('登陆时的serial%s'%serialinfo)
            z.heartbeat()
            QQnumber = self.login(d,args,z)
            z.heartbeat()
            self.slot.backup(d, str(slotnum)+'_'+QQnumber)                   #设备信息，卡槽号，QQ号
            self.repo.BackupInfo(cate_id, 'using', QQnumber,serialinfo,'%s_%s_%s' % (d.server.adb.device_serial(), self.type,slotnum))  # 仓库号,使用中,QQ号,设备号_卡槽号

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))



def getPluginClass():
    return MobilqqLogin2

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()


    d = Device("25424f9")
    z = ZDevice("25424f9")
    args = {"repo_cate_id":"331","time_limit":"120","time_limit1":"120","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
