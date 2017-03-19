# coding:utf-8
from PIL import Image
from uiautomator import Device
import util
from Repo import *
from RClient import *
import time, datetime, random
from zservice import ZDevice
from slot import slot
import os

class MobilqqLoginNoImei:
    def __init__(self):
        self.type = 'mobileqq'
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
        cate_id = args["repo_cate_id"]

        while True:
            time_limit1 = args['time_limit1']
            numbers = self.repo.GetAccount(cate_id, time_limit1, 1)
            if len(numbers) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"QQ帐号库%s号仓库为空，等待中\"" % cate_id).communicate()
                time.sleep(10)
                return
            QQNumber = numbers[0]['number']  # 即将登陆的QQ号
            QQPassword = numbers[0]['password']
            time.sleep(1)
            z.heartbeat()
            d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存
            d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            while d(textContains='正在更新数据').exists:
                time.sleep(2)
            time.sleep(4)
            z.heartbeat()
            d(text='登 录', resourceId='com.tencent.mobileqq:id/btn_login').click()
            time.sleep(1)
            d(className='android.widget.EditText', index=0).set_text(QQNumber)  # ﻿1918697054----xiake1234.  QQNumber
            time.sleep(1)
            d(resourceId='com.tencent.mobileqq:id/password', index=2).set_text(QQPassword)  # Bn2kJq5l     QQPassword
            logger = util.logger
            print('QQ号:%s,QQ密码：%s'%(QQNumber,QQPassword))
            d(text='登 录', resourceId='com.tencent.mobileqq:id/login').click()
            time.sleep(1)
            while d(text='登录中').exists:
                time.sleep(2)
            z.heartbeat()
            if d(resourceId='com.tencent.mobileqq:id/name', index='2',className="android.widget.EditText").exists:  # 需要验证码的情况
                co = RClient()
                im_id = ""
                for i in range(0, 30, +1):  # 打码循环
                    if i > 0:
                        co.rk_report_error(im_id)
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
                    im = open(codePng, 'rb').read()

                    codeResult = co.rk_create(im, 3040)
                    code = codeResult["Result"]
                    im_id = codeResult["Id"]
                    os.remove(sourcePng)
                    os.remove(codePng)
                    z.heartbeat()
                    d(resourceId='com.tencent.mobileqq:id/name', index='2',className="android.widget.EditText").set_text(code)
                    time.sleep(3)
                    d(text='完成', resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText').click()
                    time.sleep(6)
                    z.heartbeat()
                    while d(className='android.widget.ProgressBar',index=0).exists:        #网速不给力时，点击完成后仍然在加载时的状态
                        time.sleep(2)
                    time.sleep(3)
                    z.heartbeat()
                    if d(text='输入验证码',resourceId='com.tencent.mobileqq:id/ivTitleName').exists:
                        continue
                    else:
                        break

            else:
                d.server.adb.cmd("shell", "am force-stop com.tencent1314.mobileqq").communicate()  # 强制停止
                time.sleep(1)
                d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
                time.sleep(4)
            z.heartbeat()
            if d(text='搜索', resourceId='com.tencent.mobileqq:id/name').exists:  # 不需要验证码的情况
                return QQNumber
            time.sleep(1)
            if d(text='马上绑定').exists:
                return QQNumber
            time.sleep(1)
            if d(text='通讯录').exists:              #登陆上后弹出t通讯录的情况
                return QQNumber
            if d(textContains='更换主题').exists:
                return QQNumber
            if d(text='寻找好友').exists:
                return QQNumber
            if d(textContains='密码错误').exists:
                logger.info('===========密码错误==============帐号:%s,密码:%s' % (QQNumber, QQPassword))
            z.heartbeat()
            self.repo.BackupInfo(cate_id, 'frozen',QQNumber, '','')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
            time.sleep(1)
            if d(text='帐号无法登录').exists:
                d(text='取消').click()
            continue

    def action(self, d,z, args):
        z.heartbeat()
        time_limit = args['time_limit']
        cate_id = args["repo_cate_id"]
        name = self.slot.getEmpty(d)  # 取空卡槽
        print(name)
        if name == 0:    #没有空卡槽的话
            name = self.slot.getSlot(d, time_limit)  # 没有空卡槽，取２小时没用过的卡槽
            print(name)
            while name == 0:  # 2小时没有用过的卡槽也为空的情况
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ卡槽全满，无间隔时间段未用\"").communicate()
                time.sleep(30)
                name = self.slot.getSlot(d, time_limit)

            d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存
            z.heartbeat()
            z.set_mobile_data(False)
            time.sleep(5)
            self.slot.restore(d, name)  # 有time_limit分钟没用过的卡槽情况，切换卡槽
            z.set_mobile_data(True)
            time.sleep(8)
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为"+str(name)+"号\"").communicate()
            time.sleep(1)
            d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            time.sleep(2)
            while d(textContains='正在更新数据').exists:
                time.sleep(2)
            time.sleep(10)
            z.heartbeat()
            if d(resourceId='com.tencent.mobileqq:id/name', index=1).child(className='android.widget.ImageView',index=0).exists:  # 不停的加载的情况,登录失败的情况，其它都是成功的情况
                z.heartbeat()
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"该帐号失效，将重新登录\"").communicate()
                info = self.login(d, args)  # 帐号无法登陆则登陆,重新登陆
                self.slot.backup(d, name, info)  # 登陆之后备份,将备份后的信息传到后台　仓库号，状态，QQ号，备注设备id_卡槽id
                self.repo.BackupInfo(cate_id, 'using', info,'%s_%s_%s' % (d.server.adb.device_serial(), self.type, name))  # 仓库号,使用中,QQ号,设备号_卡槽号
            elif d(text='搜索',resourceId='com.tencent.mobileqq:id/name').exists:
                z.heartbeat()
                obj = self.slot.getSlotInfo(d, name)  # 得到切换后的QQ号
                info = obj['info']  # info为QQ号
                self.repo.BackupInfo(cate_id, 'using', info,'%s_%s_%s' % (d.server.adb.device_serial(),self.type, name))  # 仓库号，状态，QQ号，备注设备id_卡槽id
            elif d(text='消息').exists:
                z.heartbeat()
                obj = self.slot.getSlotInfo(d, name)  # 得到切换后的QQ号
                info = obj['info']  # info为QQ号
                self.repo.BackupInfo(cate_id, 'using', info, '%s_%s_%s' % (d.server.adb.device_serial(), self.type, name))  # 仓库号，状态，QQ号，备注设备id_卡槽id
            elif d(text='主题装扮').exists:
                z.heartbeat()
                obj = self.slot.getSlotInfo(d, name)  # 得到切换后的QQ号
                info = obj['info']  # info为QQ号
                self.repo.BackupInfo(cate_id, 'using', info, '%s_%s_%s' % (d.server.adb.device_serial(), self.type, name))  # 仓库号，状态，QQ号，备注设备id_卡槽id
            elif d(text ='马上绑定').exists:
                z.heartbeat()
                obj = self.slot.getSlotInfo(d, name)  # 得到切换后的QQ号
                info = obj['info']  # info为QQ号
                self.repo.BackupInfo(cate_id, 'using', info, '%s_%s_%s' % (d.server.adb.device_serial(), self.type, name))  # 仓库号，状态，QQ号，备注设备id_卡槽id
            elif d(text='寻找好友').exists:
                z.heartbeat()
                obj = self.slot.getSlotInfo(d, name)  # 得到切换后的QQ号
                info = obj['info']  # info为QQ号
                self.repo.BackupInfo(cate_id, 'using', info, '%s_%s_%s' % (d.server.adb.device_serial(), self.type, name))  # 仓库号，状态，QQ号，备注设备id_卡槽id
            else:        #切换不成功的情况
                z.heartbeat()
                info = self.login(d, args)  # 帐号无法登陆则登陆,重新登陆
                z.heartbeat()
                self.slot.backup(d, name, info)  # 登陆之后备份,将备份后的信息传到后台　仓库号，状态，QQ号，备注设备id_卡槽id
                self.repo.BackupInfo(cate_id, 'using', info,'%s_%s_%s' % (d.server.adb.device_serial(), self.type, name))  # 仓库号,使用中,QQ号,设备号_卡槽号


        else:  # 有空卡槽的情况

            z.set_mobile_data(False)
            time.sleep(5)
            z.set_mobile_data(True)
            time.sleep(8)
            z.heartbeat()
            info = self.login(d,args)
            z.heartbeat()
            self.slot.backup(d, name, info)                   #设备信息，卡槽号，QQ号
            self.repo.BackupInfo(cate_id, 'using', info,'%s_%s_%s' % (d.server.adb.device_serial(), self.type,name))  # 仓库号,使用中,QQ号,设备号_卡槽号

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))








def runwatch(d, data):                                  #watcher除了点击还可以做什么，watcher到可以结束方法吗，可以改变参数吗
    times = 120
    while True:
        if data == 1:
            return True
        # d.watchers.reset()
        d.watchers.run()                      #强制运行所有watchers
        times -= 1
        if times == 0:
            break
        else:
            time.sleep(0.5)

def getPluginClass():
    return MobilqqLoginNoImei

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT52DSK00474")
    z = ZDevice("HT52DSK00474")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # repo = Repo()
    # serial = z.generateSerial("788")
    # print(serial)
    # repo.BackupInfo(37, 'using','1953350195', serial,'%s_%s_%s' % (d.server.adb.device_serial(), 'qq', 1))
    #
    # getSerial = repo.Getserial(37, '%s_%s_%s' % (d.server.adb.device_serial(), 'qq', 1))  # 从备份里取出
    # getSerial = getSerial['imei']
    # z.generateSerial(getSerial)
    # z.input('1633132378')
    # d.dump(compressed=False)
    # judge = z.get_mobile_data_state()
    # print(judge)
    # if judge==True:
    #     print(111)
    # if judge==False:
    #     print(222)
    args = {"repo_cate_id":"134","time_limit":"0","time_limit1":"120","time_delay":"3"};    #cate_id是仓库号，length是数量
    util.doInThread(runwatch, d, 0, t_setDaemon=True)

    o.action(d,z, args)
    # serial = z.generateSerial("788")登录进去之前修改串号，将串号保存到仓库，所有登录之前都这么做，卡槽恢复之前根据设备号和卡槽号取到串号，调z.generateSerial(serial)将串号恢复