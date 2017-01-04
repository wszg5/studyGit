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

class MobilqqLogin:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum


    def action(self, d,z, args):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        codePng = os.path.join(base_dir, "%s_c.png" % (self.GetUnique()))


        cate_id = args["repo_cate_id"]
        numbers = self.repo.GetAccount(cate_id, 120, 1)
        print(numbers)
        wait = 1
        while wait == 1:  # 判断仓库是否有东西
            try:
                QQNumber = numbers[0]['number']  # 即将登陆的QQ号
                wait = 0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到号码\"")
                time.sleep(20)
        QQPassword = numbers[0]['password']
        time.sleep(1)
        t=1
        while t ==1:
            d.server.adb.cmd("shell","pm clear com.tencent.mobileqq").wait()  # 清除缓存
            d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
            time.sleep(5)
            d(text='登 录',resourceId='com.tencent.mobileqq:id/btn_login').click()
            d(className='android.widget.EditText',text='QQ号/手机号/邮箱').set_text(836201593)    #﻿1918697054----xiake1234.  QQNumber
            d(resourceId='com.tencent.mobileqq:id/password',description='密码 安全').set_text('13141314abc')    #Bn2kJq5l     QQPassword
            d(text='登 录',resourceId='com.tencent.mobileqq:id/login').click()
            while d(className='android.widget.LinearLayout').child(text='登录中',resourceId='com.tencent.mobileqq:id/name').exists:
                time.sleep(1)
            # time.sleep(6)
            d.watcher('pop').when(text= u'马上绑定').click(text=u'消息')


            # d.watcher('success').when(text='搜索').when(resourceId='com.tencent.tim:id/name')

            # if d(text='搜索',resourceId='com.tencent.tim:id/name').exists:       #直接登陆成功的情况
            #     return  # 放到方法里改为return


            # if d(text='帐号无法登录', resourceId='com.tencent.eim:id/dialogTitle').exists:  # 帐号被冻结
            #     self.repo.SetAccount(cate_id, 'frozen', QQNumber)
            #     break

            if d(resourceId='com.tencent.mobileqq:id/name', index='2', className="android.widget.EditText").exists:        #需要验证码的情况
                co = RClient()
                im_id = ""
                for i in range(0, 30, +1):         #打码循环
                    if i > 0:
                        co.rk_report_error(im_id)
                    obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.ImageView')
                    obj = obj.info
                    print(obj)
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

                    d(resourceId='com.tencent.mobileqq:id/name', index='2', className="android.widget.EditText").set_text(code)
                    time.sleep(3)
                    d(text='完成', resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText').click()
                    time.sleep(2)


                    if d(text='登 录').exists:  # 密码错误
                        self.repo.SetAccount(cate_id, 'locked', QQNumber)
                        break

                    if d(text='帐号无法登录', resourceId='com.tencent.mobileqq:id/dialogTitle').exists:  # 帐号被冻结
                        self.repo.SetAccount(cate_id, 'frozen', QQNumber)
                        break
                    if d(text='身份过期',resourceId='com.tencent.mobileqq:id/dialogTitle').exists:
                        break

                    d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
                    d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来




            if d(text='搜索', resourceId='com.tencent.mobileqq:id/name').exists:       #不需要验证码的情况
                # t=2
                return  # 放到方法里改为return
            if d(text='马上绑定').exists:
                # t=2
                return


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
    return MobilqqLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT536SK01667")
    z = ZDevice("HT536SK01667")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()


    # d.dump(compressed=False)
    args = {"repo_cate_id":"53","time_limit":"120","time_delay":"3"};    #cate_id是仓库号，length是数量
    util.doInThread(runwatch, d, 0, t_setDaemon=True)

    o.action(d,z, args)