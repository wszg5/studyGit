# coding:utf-8
import threading
import time
from PIL import Image
from uiautomator import Device
import os,re,subprocess
from Repo import *
from RClient import *
import time, datetime, random
from zservice import ZDevice
from slot import slot

class EIMLogin:
    def __init__(self):
        self.repo = Repo()
        self.slot = slot('eim')


    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def login(self):
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
        t = 1
        while t == 1:
            d.server.adb.cmd("shell", "pm clear com.tencent.eim").wait()  # 清除缓存
            d.server.adb.cmd("shell",
                             "am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
            time.sleep(8)
            d(className='android.widget.Button', index=1, clickable='true').click()
            d(className='android.widget.EditText', text='企业QQ号/手机号/邮箱').set_text(QQNumber)  # 3001313499  QQNumber
            d(resourceId='com.tencent.eim:id/password', description='请输入密码').set_text(QQPassword)  # Bn2kJq5l   QQPassword
            d(text='登 录', resourceId='com.tencent.eim:id/login').click()

            if d(text='搜索', resourceId='com.tencent.eim:id/name').exists:  # 直接登陆成功的情况
                return  QQNumber   # 放到方法里改为return

            if d(text='帐号无法登录', resourceId='com.tencent.eim:id/dialogTitle').exists:  # 帐号被冻结
                self.repo.SetAccount(cate_id, 'frozen', QQNumber)
                break

            co = RClient()
            im_id = ""

            for i in range(0, 30, +1):  # 打码循环
                if i > 0:
                    co.rk_report_error(im_id)
                obj = d(resourceId='com.tencent.eim:id/name', className='android.widget.ImageView')
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

                d(resourceId='com.tencent.eim:id/name', index='2', className="android.widget.EditText").set_text(code)
                time.sleep(1)
                d(text='完成', resourceId='com.tencent.eim:id/ivTitleBtnRightText').click()
                time.sleep(2)

                if d(text='登 录').exists:  # 密码错误
                    self.repo.SetAccount(cate_id, 'locked', QQNumber)
                    break

                if d(text='帐号无法登录', resourceId='com.tencent.eim:id/dialogTitle').exists:  # 帐号被冻结
                    self.repo.SetAccount(cate_id, 'frozen', QQNumber)
                    break
                #
                if d(text='搜索', resourceId='com.tencent.eim:id/name').exists:
                    return  QQNumber# 放到方法里改为return




    def action(self, d,z, args):
        name = self.slot.getEmpty(d)  # 取空卡槽

        if name == 0:
            name = self.slot.getSlot(d, 120)  # 没有空卡槽，取２小时没用过的卡槽
            while name == 0:  # 2小时没有用过的卡槽也为空的情况
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"卡槽全满，无2小时未用\"")
                time.sleep(30)
                name = self.slot.getSlot(d, 120)

            # d.open.quick_settings()
            # d(text='飞行模式').click()
            # if d(text='不要再显示此内容。', resourceId='android:id/text1').exists:
            #     time.sleep(2)
            #     d(text='不要再显示此内容。', resourceId='android:id/text1').click()
            #     d(text='确定').click()
            #     d.open.quick_settings()
            #     d(text='飞行模式').click()       #飞行模式开
            # on = 1
            # while on==1:
            #     device = self.dbapi.GetDevice(d.server.adb.device_serial())
            #     obj = device["airplaneMode"]
            #     print(obj)
            #     if obj == 'true':               #飞行模式打开成功
            #         on = 0
            #     else:
            #         time.sleep(2)

            self.slot.restore(d, name)  # 有２小时没用过的卡槽情况，切换卡槽

            # d.open.quick_settings()
            # d(text='飞行模式', resourceId='com.android.systemui:id/quick_setting_text').click()           #飞行模式关
            # on = 1
            # while on == 1:
            #     device = self.dbapi.GetDevice(d.server.adb.device_serial())
            #     obj = device["airplaneMode"]
            #     print(obj)
            #     if obj == 'False':  # 飞行模式打开成功
            #         on = 0
            #     else:
            #         time.sleep(2)

            d.server.adb.cmd("shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
            if d(text='帐号无法登录').exists:
                # d.open.quick_settings()
                # d(text='飞行模式').click()  # 飞行模式开
                # on = 1
                # while on == 1:
                #     device = self.dbapi.GetDevice(d.server.adb.device_serial())
                #     obj = device["airplaneMode"]
                #     print(obj)
                #     if obj == 'true':  # 飞行模式打开成功
                #         on = 0
                #     else:
                #         time.sleep(2)
                # d(text='飞行模式').click()           #飞行模式关
                # on = 1
                # while on == 1:
                #     device = self.dbapi.GetDevice(d.server.adb.device_serial())
                #     obj = device["airplaneMode"]
                #     print(obj)
                #     if obj == 'true':  # 飞行模式打开成功
                #         on = 0
                #     else:
                #         time.sleep(2)

                info = self.login()  # 帐号无法登陆则登陆,重新注册登陆
                self.slot.backup(d, name, info)  # 登陆之后备份

            else:
                return

        else:  # 有空卡槽的情况
            # d.open.quick_settings()
            # d(text='飞行模式').click()  # 飞行模式开
            # on = 1
            # while on == 1:
            #     device = self.dbapi.GetDevice(d.server.adb.device_serial())
            #     obj = device["airplaneMode"]
            #     print(obj)
            #     if obj == 'true':  # 飞行模式打开成功
            #         on = 0
            #     else:
            #         time.sleep(2)
            # d(text='飞行模式').click()  # 飞行模式关
            # on = 1
            # while on == 1:
            #     device = self.dbapi.GetDevice(d.server.adb.device_serial())
            #     obj = device["airplaneMode"]
            #     print(obj)
            #     if obj == 'true':  # 飞行模式打开成功
            #         on = 0
            #     else:
            #         time.sleep(2)

            info = self.login()
            self.slot.backup(d, name, info)



        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))
def getPluginClass():
    return EIMLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT4A3SK00853")
    z = ZDevice("HT4AVSK01106")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # d.dump(compressed=False)
    args = {"repo_cate_id":"55","time_limit":"120","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)