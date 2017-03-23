# coding:utf-8
import threading
import time
from PIL import Image
from uiautomator import Device
import re,subprocess
import util
from Repo import *
from imageCode import imageCode
import time, datetime, random
from zservice import ZDevice
import os


class MobilqqLoginNoSolt:
    def __init__(self):
        self.type = 'mobileqq'
        self.repo = Repo()


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

        cate_id = args["repo_cate_id"]      #仓库号
        while True:
            time_limit = args['time_limit']         #帐号提取时间间隔
            numbers = self.repo.GetAccount(cate_id, time_limit, 1)
            if len(numbers) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"QQ帐号库%s号仓库为空，等待中\"" % cate_id).communicate()
                z.sleep(10)
                return
            QQNumber = numbers[0]['number']  # 即将登陆的QQ号
            QQPassword = numbers[0]['password']
            z.sleep(1)

            z.heartbeat()
            d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存
            d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            z.sleep(8)
            d(text='登 录', resourceId='com.tencent.mobileqq:id/btn_login').click()
            z.sleep(1)
            d(className='android.widget.EditText', text='QQ号/手机号/邮箱').set_text(QQNumber)  # ﻿1918697054----xiake1234.  QQNumber
            z.sleep(1)
            d(resourceId='com.tencent.mobileqq:id/password', description='密码 安全').set_text(QQPassword)  # Bn2kJq5l     QQPassword
            z.heartbeat()
            print('帐号:%s,密码：%s'%(QQNumber,QQPassword))
            d(text='登 录', resourceId='com.tencent.mobileqq:id/login').click()
            z.sleep(1)
            while d(text='登录中').exists:
                z.sleep(2)
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
                    while d(className='android.widget.ProgressBar',index=0).exists:        #网速不给力时，点击完成后仍然在加载时的状态
                        z.sleep(2)
                    z.heartbeat()
                    if d(text='输入验证码',resourceId='com.tencent.mobileqq:id/ivTitleName').exists:
                        continue
                    else:
                        break

            else:
                d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
                z.sleep(1)
                d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
                z.sleep(4)
                z.heartbeat()
            z.heartbeat()
            if d(text='搜索', resourceId='com.tencent.mobileqq:id/name').exists:  # 不需要验证码的情况
                return QQNumber
            z.sleep(1)
            if d(text='马上绑定').exists:
                return QQNumber
            z.sleep(1)
            if d(text='通讯录').exists:              #登陆上后弹出t通讯录的情况
                return QQNumber
            else:
                z.sleep(1)
                if d(text='帐号无法登录').exists:
                    d(text='取消').click()
                continue

    def action(self, d,z, args):
        z.heartbeat()
        z.set_mobile_data(False)
        z.sleep(5)
        z.set_mobile_data(True)
        z.sleep(8)
        z.heartbeat()
        serialinfo = z.generateSerial("788")  # 修改串号等信息
        self.login(d,args,z)
        z.heartbeat()
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))








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
    return MobilqqLoginNoSolt

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT49XSK01858")
    z = ZDevice("HT49XSK01858")

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存
    # slot.restore(d, 9)

    # d.dump(compressed=False)
    args = {"repo_cate_id":"59","time_limit":"1","time_delay":"3"};    #cate_id是仓库号，length是数量
    util.doInThread(runwatch, d, 0, t_setDaemon=True)

    o.action(d,z, args)