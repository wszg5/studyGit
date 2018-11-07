# coding:utf-8
import base64
import colorsys
import datetime
import os
import random
import time
import uuid

from PIL import Image

import util
from CodeDLL import *
from Repo import *
from imageCode import imageCode
from uiautomator import Device
from zservice import ZDevice


class MobilqqLogin:
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

    def WebViewBlankPages(self, d, z):
        z.toast("判断是否是滑块")
        Str = d.info  # 获取屏幕大小等信息
        height = float(Str["displayHeight"])
        width = float(Str["displayWidth"])

        W_H = width / height
        screenScale = round(W_H, 2)

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))

        if screenScale == 0.56:
            left = 115  # 验证码的位置信息
            top = 670
            right = 185
            bottom = 720
        if screenScale == 0.61:
            left = 115  # 验证码的位置信息
            top = 670
            right = 185
            bottom = 720

        d.screenshot(sourcePng)  # 截取整个输入验证码时的屏幕

        img = Image.open(sourcePng)
        box = (left, top, right, bottom)  # left top right bottom
        region = img.crop(box)  # 截取验证码的图片
        # show(region)    #展示资料卡上的信息
        image = region.convert('RGBA')
        # 生成缩略图，减少计算量，减小cpu压力
        image.thumbnail((200, 200))
        max_score = None
        dominant_color = None
        for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
            # 跳过纯黑色
            if a == 0:
                continue
            saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
            y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
            y = (y - 16.0) / (235 - 16)
            # 忽略高亮色
            if y > 0.9:
                continue

            score = (saturation + 0.1) * count
            if score > max_score:
                max_score = score
                dominant_color = (r, g, b)  # 红绿蓝
        return dominant_color

    def WebViewPlayCode(self, d, z):
        z.toast("非空白页，开始截图打码")

        Str = d.info  # 获取屏幕大小等信息
        height = float(Str["displayHeight"])
        width = float(Str["displayWidth"])
        W_H = width / height
        screenScale = round(W_H, 2)

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        # icode = imageCode()
        im_id = ""
        for i in range(0, 1):  # 打码循环
            if i > 0:
                pass

            d.screenshot(sourcePng)  # 截取整个输入验证码时的屏幕
            if screenScale == 0.61:
                p = {"x1": 30 / width, "y1": 200 / height, "x2": 271 / width, "y2": 300 / height}
            if screenScale == 0.56:
                p = {"x1": 40 / width, "y1": 270 / height, "x2": 362 / width, "y2": 400 / height}
            cropedImg = z.img_crop(sourcePng, p)
            # im = open(cropedImg, 'rb')
            with open( cropedImg, 'rb' ) as f:
                # file = f.read()
                file = "data:image/jpeg;base64," + base64.b64encode( f.read( ) )
                da = {"IMAGES": file}
                path = "/ocr.index"
                headers = {"Content-Type": "application/x-www-form-urlencoded",
                           "Connection": "Keep-Alive"}
                conn = httplib.HTTPConnection( "162626i1w0.51mypc.cn", 10082, timeout=30 )
                params = urllib.urlencode( da )
                conn.request( method="POST", url=path, body=params, headers=headers )
                response = conn.getresponse( )
                if response.status == 200:
                    code = response.read( )
            os.remove(sourcePng)
            z.heartbeat()
            z.sleep(5)
            if screenScale == 0.61:
                d.click(360, 240)
            if screenScale == 0.56:
                d.click(500, 350)
            z.input(code)
            z.sleep(2)
            if screenScale == 0.61:
                d.click(270, 450)
            if screenScale == 0.56:
                d.click(360, 600)

            while d(className='android.widget.ProgressBar', index=0).exists:  # 网速不给力时，点击完成后仍然在加载时的状态
                z.sleep(2)
            z.sleep(8)

            if not d(textContains='验证码').exists:
                z.toast("机器人打码跳出－－")
                break

    # def playCode(self, codeImgObj, type):
    #     z.toast("非网页视图打码")
    #     self.scode = smsCode(d.server.adb.device_serial())
    #     base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
    #     if not os.path.isdir(base_dir):
    #         os.mkdir(base_dir)
    #     sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
    #     codePng = os.path.join(base_dir, "%s_c.png" % (self.GetUnique()))
    #     icode = imageCode()
    #     im_id = ""
    #     for i in range(0, 4):  # 打码循环
    #         if i > 0:
    #             icode.reportError(im_id)
    #         obj = d(resourceId='com.tencent.mobileqq:id/name',
    #                  className='android.widget.ImageView')  # 当弹出选择QQ框的时候，定位不到验证码图片
    #         if not obj.exists:
    #             obj = d(index='2', className='android.widget.Image')
    #         obj = obj.info
    #         obj = obj['bounds']  # 验证码处的信息
    #         left = obj["left"]  # 验证码的位置信息
    #         top = obj['top']
    #         right = obj['right']
    #         bottom = obj['bottom']
    #
    #         d.screenshot(sourcePng)  # 截取整个输入验证码时的屏幕
    #
    #         img = Image.open(sourcePng)
    #         box = (left, top, right, bottom)  # left top right bottom
    #         region = img.crop(box)  # 截取验证码的图片
    #
    #         img = Image.new('RGBA', (right - left, bottom - top))
    #         img.paste(region, (0, 0))
    #
    #         img.save(codePng)
    #
    #         with open(codePng, 'rb') as im:
    #             codeResult = icode.getCode(im, icode.CODE_TYPE_4_NUMBER_CHAR, 60)
    #
    #         code = codeResult["Result"]
    #         im_id = codeResult["Id"]
    #         os.remove(sourcePng)
    #         os.remove(codePng)
    #         z.heartbeat()
    #         z.sleep(5)
    #         if type == 0:
    #             d(resourceId='com.tencent.mobileqq:id/name', index='2',
    #                className="android.widget.EditText").set_text(code)
    #         else:
    #             codeImgObj.set_text(code)
    #         z.sleep(3)
    #         if d(descriptionContains='验证', className='android.view.View').exists:
    #             d(descriptionContains='验证', className='android.view.View').click()
    #         else:
    #             d(text='完成', resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText').click()
    #         z.sleep(6)
    #         z.heartbeat()
    #         while d(className='android.widget.ProgressBar', index=0).exists:  # 网速不给力时，点击完成后仍然在加载时的状态
    #             z.sleep(2)
    #         z.sleep(3)
    #         z.heartbeat()
    #         if codeImgObj.exists:
    #             continue
    #         else:
    #             break
    #     z.sleep(5)
    #     if d(textContains='验证码').exists:
    #         return False
    #     else:
    #         return True

    def login(self, d, args, z, numbers):

        QQNumber = numbers[0]['number']  # 即将登陆的QQ号
        QQPassword = numbers[0]['password']

        z.heartbeat()
        d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存
        d.server.adb.cmd("shell","am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(5)
        while d(textContains='正在更新数据').exists:
            z.sleep(2)

        z.sleep(15)
        z.heartbeat()
        d.dump(compressed=False)
        if d(text='登 录',resourceId='com.tencent.mobileqq:id/btn_login').exists:
            d(text='登 录').click()

        z.sleep(1)
        d(className='android.widget.EditText', index=0).click()  # ﻿1918697054----xiake1234.  QQNumber
        z.input(QQNumber)

        z.sleep(1)
        d(resourceId='com.tencent.mobileqq:id/password').click()  # Bn2kJq5l     QQPassword
        z.input(QQPassword)

        z.heartbeat()
        print('QQ号:%s,QQ密码：%s' % (QQNumber, QQPassword))
        d.dump(compressed=False)
        d(text='登 录', resourceId='com.tencent.mobileqq:id/login').click()
        z.sleep(3)
        while d(text='登录中').exists:
            z.sleep(2)
        z.sleep(20)

        z.heartbeat()
        detection_robot = d(index='3', className="android.widget.EditText")
        not_detection_robot = d(resourceId='com.tencent.mobileqq:id/name', index='2',
                                 className="android.widget.EditText")
        if detection_robot.exists:  # 需要验证码的情况
            if not self.playCode(detection_robot, 1):
                return False

        if not_detection_robot.exists:
            if not self.playCode(not_detection_robot.exists, 0) == "nothing":
                return False

        if d(className='android.webkit.WebView').exists:
            if self.WebViewBlankPages(d, z)[2] < 200:
                self.WebViewPlayCode(d, z)
            else:
                y = 555
                for r in range(1, 3):
                    d.swipe(155, 703, y, 703)
                    z.sleep(2)
                    if not d(text='验证码', resourceId='com.tencent.mobileqq:id/ivTitleName').exists:
                        break
                    else:
                        y += 20

                if d(text='验证码', resourceId='com.tencent.mobileqq:id/ivTitleName').exists or d(text='去安全中心').exists:
                    self.repo.BackupInfo(args["repo_cate_id"], 'frozen', QQNumber, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                    return False

        z.sleep(5)
        z.heartbeat()
        loginStatusList = z.qq_getLoginStatus(d)
        if loginStatusList is None:
            if d(text='消息').exists and d(text='联系人').exists and d(text='动态').exists:
                loginStatusList = {'success': True}
            elif d(textContains="请在小米神隐模式中将TIM设置为“无限制”。").exists:
                z.toast("我是小米神隐")
                d(text='我知道了').click()
            else:
                loginStatusList = {'success': False}

        loginStatus = loginStatusList['success']
        if loginStatus:
            z.toast("QQ状态正常，继续执行")
            return True
        else:
            if d(text='去安全中心').exists:
                self.repo.BackupInfo(args["repo_cate_id"], 'frozen', QQNumber, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber

            else:
                self.repo.BackupInfo(args["repo_cate_id"], 'normal', QQNumber, '', '')

            z.toast("卡槽QQ状态异常，跳过此模块")
            return False

        # if d(text='马上绑定').exists:
        #     self.BindAddressBook(z, d, args)


    def action(self, d, z, args):
        while True:
            z.heartbeat()
            z.generate_serial("com.tencent.mobileqq") # 随机生成手机特征码
            cate_id = args["repo_cate_id"]

            time_limit = args['time_limit']
            numbers = self.repo.GetAccount(cate_id, time_limit, 1)
            if len(numbers) == 0:
                z.toast("%s 号仓库为空")
                return

            z.heartbeat()
            if self.login(d, args, z, numbers):
                z.heartbeat()
                z.toast("登陆成功")
                break

        if args["time_delay"]:
            z.sleep(int(args["time_delay"]))



def getPluginClass():
    return MobilqqLogin

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("cc0e9474")
    z = ZDevice("cc0e9474")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_cate_id": "374", "time_limit": "2", "time_delay": "3"};    #cate_id是仓库号，length是数量
    # z.server.install()
    o.action(d, z, args)
    # serial = d.server.adb.device_serial()
    # type = 'qqmail'
    # slot = Slot(serial, type)
    # slot.clear("1")
    # for i in range(1,200):
    #     slot.clear(i)
    #     print('已经清除')
    # print('全部清除')
    # d.server.adb.cmd("shell", "pm clear com.tencent.androidqqmail").communicate()  # 清除缓存

    # d.server.adb.cmd("shell", "am start -n com.tencent.androidqqmail/com.tencent.qqmail.launcher.third.LaunchComposeMail").communicate()  # 拉起QQ邮箱

    # d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity").communicate() 拉起易信



