# coding:utf-8
import threading
import time
from PIL import Image
from uiautomator import Device
import os,re,subprocess
import util
from Repo import *
from RClient import *
import time, datetime, random
from zservice import ZDevice

class MobilqqLoginSolt:
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


    def login(self,d,args):
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
                time.sleep(10)
                return
            QQNumber = numbers[0]['number']  # 即将登陆的QQ号
            QQPassword = numbers[0]['password']
            time.sleep(1)


            d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存
            d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            time.sleep(8)
            d(text='登 录', resourceId='com.tencent.mobileqq:id/btn_login').click()
            time.sleep(1)
            d(className='android.widget.EditText', text='QQ号/手机号/邮箱').set_text(QQNumber)  # ﻿1918697054----xiake1234.  QQNumber
            time.sleep(1)
            d(resourceId='com.tencent.mobileqq:id/password', description='密码 安全').set_text(QQPassword)  # Bn2kJq5l     QQPassword
            d(text='登 录', resourceId='com.tencent.mobileqq:id/login').click()
            time.sleep(1)
            while d(text='登录中').exists:
                time.sleep(2)

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

                    d(resourceId='com.tencent.mobileqq:id/name', index='2',className="android.widget.EditText").set_text(code)
                    time.sleep(3)
                    d(text='完成', resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText').click()
                    time.sleep(6)
                    while d(className='android.widget.ProgressBar',index=0).exists:        #网速不给力时，点击完成后仍然在加载时的状态
                        time.sleep(2)
                    if d(text='输入验证码',resourceId='com.tencent.mobileqq:id/ivTitleName').exists:
                        continue
                    else:
                        break

            else:
                d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
                time.sleep(1)
                d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
                time.sleep(4)

            if d(text='搜索', resourceId='com.tencent.mobileqq:id/name').exists:  # 不需要验证码的情况
                return QQNumber
            time.sleep(1)
            if d(text='马上绑定').exists:
                return QQNumber
            time.sleep(1)
            if d(text='通讯录').exists:              #登陆上后弹出t通讯录的情况
                return QQNumber
            else:
                time.sleep(1)
                if d(text='帐号无法登录').exists:
                    d(text='取消').click()
                continue

    def action(self, d,z, args):
        z.set_mobile_data(False)
        time.sleep(5)
        z.set_mobile_data(True)
        time.sleep(8)
        self.login(d,args)

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
    return MobilqqLoginSolt

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT49XSK01858")
    z = ZDevice("HT49XSK01858")

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存
    # slot.restore(d, 9)

    # d.dump(compressed=False)
    args = {"repo_cate_id":"59","time_limit":"1","time_delay":"3"};    #cate_id是仓库号，length是数量
    util.doInThread(runwatch, d, 0, t_setDaemon=True)

    o.action(d,z, args)