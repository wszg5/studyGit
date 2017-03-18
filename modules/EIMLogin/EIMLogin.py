# coding:utf-8
import threading
import time
from PIL import Image
from uiautomator import Device
import re,subprocess
from Repo import *
from RClient import *
import time, datetime, random
from zservice import ZDevice
from slot import slot
import os


class EIMLogin:
    def __init__(self):
        self.type = 'eim'
        self.repo = Repo()
        self.slot = slot(self.type)


    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def login(self,d,args):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        codePng = os.path.join(base_dir, "%s_c.png" % (self.GetUnique()))

        time.sleep(1)
        t = 1
        while t == 1:         #直到登陆成功为止
            time_limit1 = args['time_limit1']
            cate_id = args["repo_cate_id"]
            numbers = self.repo.GetAccount(cate_id, time_limit1, 1)
            if len(numbers) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"EIM%s号帐号库为空，等待中\"" % cate_id).communicate()
                time.sleep(10)
                return
            QQNumber = numbers[0]['number']  # 即将登陆的QQ号
            QQPassword = numbers[0]['password']
            print('QQ号是：%s,QQ密码是：%s'%(QQNumber,QQPassword))
            d.server.adb.cmd("shell", "pm clear com.tencent.eim").communicate()  # 清除缓存
            d.server.adb.cmd("shell", "am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            time.sleep(5)
            z.heartbeat()
            d(className='android.widget.Button', index=1, clickable='true').click()
            time.sleep(2)
            d(className='android.widget.EditText', text='企业QQ号/手机号/邮箱').set_text(QQNumber)  # 3001313499  QQNumber  3001346198
            d(resourceId='com.tencent.eim:id/password', description='请输入密码').set_text(QQPassword)  # Bn2kJq5l   QQPassword
            d(text='登 录').click()
            time.sleep(4)
            if d(text='企业QQ').exists:
                d(text='企业QQ').click()
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()
            z.heartbeat()
            if d(text='搜索').exists:  # 直接登陆成功的情况
                return  QQNumber   # 放到方法里改为return

            if d(text='帐号无法登录', resourceId='com.tencent.eim:id/dialogTitle').exists:  # 帐号被冻结
                self.repo.BackupInfo(cate_id, 'frozen', QQNumber, '','')
                break

            co = RClient()
            im_id = ""
            for i in range(0, 30, +1):  # 打码循环
                if i > 0:
                    co.rk_report_error(im_id)
                obj = d(resourceId='com.tencent.eim:id/name', className='android.widget.ImageView')
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
                im = open(codePng, 'rb').read()

                codeResult = co.rk_create(im, 3040)
                code = codeResult["Result"]
                im_id = codeResult["Id"]
                os.remove(sourcePng)
                os.remove(codePng)
                z.heartbeat()
                d(resourceId='com.tencent.eim:id/name', index='2', className="android.widget.EditText").set_text(code)
                time.sleep(1)
                d(text='完成').click()
                time.sleep(4)
                while d(className='android.widget.ProgressBar',index=0).exists:     #网速较慢，校验验证码未完成的情况
                    time.sleep(2)
                z.heartbeat()
                if d(text='搜索', resourceId='com.tencent.eim:id/name').exists:
                    return  QQNumber# 放到方法里改为return
                if d(text='输入验证码').exists:           #验证码输入错误的情况
                    continue
                else:
                    self.repo.BackupInfo(cate_id, 'frozen', QQNumber,'')  # 仓库号,使用中,QQ号,设备号_卡槽号
                    break

    def action(self, d,z, args):
        z.heartbeat()
        time_limit = args['time_limit']
        cate_id = args["repo_cate_id"]
        slotnum = self.slot.getEmpty(d)  # 取空卡槽
        print(slotnum)
        if slotnum == 0:
            slotnum = self.slot.getSlot(d, time_limit)  # 没有空卡槽，取time_limit小时没用过的卡槽
            while slotnum == 0:  # 2小时没有用过的卡槽也为空的情况
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"EIM卡槽全满，无间隔时间段未用\"").communicate()
                time.sleep(30)
                slotnum = self.slot.getSlot(d, time_limit)
            z.heartbeat()
            d.server.adb.cmd("shell", "pm clear com.tencent.eim").communicate()  # 清除缓存
            z.set_mobile_data(False)
            time.sleep(3)
            getSerial = self.repo.Getserial(cate_id,'%s_%s_%s' % (d.server.adb.device_serial(), self.type, slotnum))  # 得到之前的串号
            if len(getSerial) == 0:  # 之前的信息保存失败的话
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"串号获取失败，重新设置\"").communicate()  # 在５１上测时库里有东西但是王红机器关闭后仍获取失败
                getSerial = z.generateSerial("788")  # 修改信息
            else:
                getSerial = getSerial[0]['imei']      #如果信息保存成功但串号没保存成功的情况
                print('卡槽切换时的sereial%s'%getSerial)
                if getSerial is None:          #如果串号为空，在该卡槽下保存新的串号
                    getSerial = z.generateSerial("788")  # 修改信息
                else:
                    z.generateSerial(getSerial)  # 将串号保存
            z.heartbeat()
            self.slot.restore(d, slotnum)  # 有２小时没用过的卡槽情况，切换卡槽
            print("切换为"+str(slotnum))
            z.set_mobile_data(True)
            time.sleep(8)

            d.server.adb.cmd("shell","am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            time.sleep(2)
            z.heartbeat()
            while d(textContains='正在更新数据').exists:
                time.sleep(2)
            z.heartbeat()
            d.server.adb.cmd("shell","am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为%s号\""%slotnum).communicate()
            time.sleep(6)
            if d(textContains='开启精彩').exists:
                d(textContains='开启精彩').click()
            if d(descriptionContains='开启精彩').exists:
                d(descriptionContains='开启精彩').click()
            if d(resourceId='com.tencent.eim:id/name',className='android.widget.Button').exists:     #点击开始体验
                d(resourceId='com.tencent.eim:id/name', className='android.widget.Button').click()
                time.sleep(6)
            z.heartbeat()
            if d(text='搜索').exists:
                QQnumber = self.slot.getSlotInfo(d, slotnum)  # 得到切换后的QQ号
                QQnumber = QQnumber['info']  # info为QQ号
                self.slot.backup(d, slotnum, QQnumber)  # 设备信息，卡槽号，QQ号
                self.repo.BackupInfo(cate_id, 'using', QQnumber,getSerial,'%s_%s_%s' % (d.server.adb.device_serial(), self.type,slotnum))  # 仓库号，状态，QQ号，备注设备id_卡槽id
            else:  # 切换不成功的情况
                z.heartbeat()
                serialinfo = z.generateSerial("788")  # 修改串号等信息
                print('登陆时的serial%s' % serialinfo)
                QQnumber = self.login(d, args)
                self.slot.backup(d, slotnum, QQnumber)  # 设备信息，卡槽号，QQ号
                self.repo.BackupInfo(cate_id, 'using', QQnumber, serialinfo, '%s_%s_%s' % (d.server.adb.device_serial(), self.type, slotnum))  # 仓库号,使用中,QQ号,设备号_卡槽号

        else:  # 有空卡槽的情况
            z.heartbeat()
            z.set_mobile_data(False)
            time.sleep(3)
            z.set_mobile_data(True)
            time.sleep(8)
            serialinfo = z.generateSerial("788")  # 修改串号等信息
            print('登陆时的serial%s' % serialinfo)
            QQnumber = self.login(d, args)
            z.heartbeat()
            self.slot.backup(d, slotnum, QQnumber)  # 设备信息，卡槽号，QQ号
            self.repo.BackupInfo(cate_id, 'using', QQnumber,serialinfo,'%s_%s_%s' % (d.server.adb.device_serial(),self.type, slotnum))  # 仓库号,使用中,QQ号,设备号_卡槽号

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))
def getPluginClass():
    return EIMLogin

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # d.dump(compressed=False)
    # slot = slot('eim')
    # d(resourceId='com.tencent.eim:id/name', className='android.widget.Button').click()
    # slot.restore(d, 2)  # 有２小时没用过的卡槽情况，切换卡槽

    # z.input('gfdc')
    args = {"repo_cate_id":"34","time_limit":"3","time_limit1":"10","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)