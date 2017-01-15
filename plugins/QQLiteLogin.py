# coding:utf-8
import threading
import time
from PIL import Image
from uiautomator import Device
import os,re,subprocess
from Repo import *
from RClient import *
import time, datetime, random
from XunMa import *
from slot import slot
from zservice import ZDevice


class QQLiteLogin:
    def __init__(self):
        self.type = 'qqlite'
        self.repo = Repo()
        self.XunMa = XunMa()
        self.slot = slot(self.type)

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum
    def login(self,d,z,args):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        codePng = os.path.join(base_dir, "%s_c.png" % (self.GetUnique()))

        d.server.adb.cmd("shell", "pm clear com.tencent.qqlite").wait()  # 清除缓存
        while True:
            # d.server.adb.cmd("shell", "am force-stop com.tencent.qqlite").wait()  # 将qq强制停止
            d.server.adb.cmd("shell",
                             "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity").wait()  # 将qq拉起来
            time.sleep(3)

            cate_id = args["repo_cate_id"]
            numbers = self.repo.GetAccount(cate_id, 120, 1)

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
            d(text='登 录').click()
            time.sleep(1)
            d(text='QQ号/手机号/邮箱').set_text(QQNumber)  # QQNumber

            time.sleep(1)
            d(resourceId='com.tencent.qqlite:id/password').set_text(QQPassword)  # QQPassword
            time.sleep(1)
            d(text='登 录').click()
            time.sleep(2)
            if d(text='QQ轻聊版').exists:  # 登陆成功
                return  # 放到方法里改为return
            if d(text='启用通讯录').exists:  # 登陆成功
                return  # 放到方法里改为return
            if d(text='帐号无法登录', resourceId='com.tencent.qqlite:id/dialogTitle').exists:  # 帐号被冻结
                d.press.home()
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"上一轮没有登陆成功，再次登陆QQ\"")
                continue

            co = RClient()
            im_id = ""

            for i in range(0, 30, +1):  # 打码的
                if i > 0:
                    co.rk_report_error(im_id)
                obj = d(resourceId='com.tencent.qqlite:id/0', className='android.widget.ImageView')
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

                d(resourceId='com.tencent.qqlite:id/0', index='2', className="android.widget.EditText").set_text(code)
                time.sleep(1)
                d(text='完成', resourceId='com.tencent.qqlite:id/ivTitleBtnRightText').click()
                time.sleep(2)
                if d(text='登 录').exists:  # 密码错误
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"上一轮没有登陆成功，再次登陆QQ\"")
                    self.repo.SetAccount(cate_id, 'passwordEror', QQNumber)
                    break

                if d(text='帐号无法登录', resourceId='com.tencent.qqlite:id/dialogTitle').exists:  # 帐号被冻结
                    d.press.home()
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"上一轮没有登陆成功，再次登陆QQ\"")
                    self.repo.SetAccount(cate_id, 'frozen', QQNumber)
                    break

                if d(text='QQ轻聊版').exists:
                    return  # 放到方法里改为return
                    # region = region.transpose(Image.ROTATE_180)    #用来将图片旋转
                    # region.show()
                    # im.paste(region, box)
                    # im.show()



    def action(self, d,z, args):
        time_limit = args['time_limit']
        cate_id = args["repo_cate_id"]
        name = self.slot.getEmpty(d)  # 取空卡槽
        print(name)
        if name == 0:
            name = self.slot.getSlot(d, time_limit)  # 没有空卡槽，取time_limit小时没用过的卡槽
            while name == 0:  # 2小时没有用过的卡槽也为空的情况
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.qk.toast --es msg \"EIM卡槽全满，无间隔时间段未用\"").communicate()
                time.sleep(30)
                name = self.slot.getSlot(d, time_limit)

            z.set_mobile_data(False)
            time.sleep(3)
            self.slot.restore(d, name)  # 有２小时没用过的卡槽情况，切换卡槽
            print("切换为" + str(name))
            z.set_mobile_data(True)
            time.sleep(8)

            d.server.adb.cmd("shell",
                             "am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            while d(textContains='正在更新数据').exists:
                time.sleep(2)
            time.sleep(4)
            d.server.adb.cmd("shell",
                             "am broadcast -a com.zunyun.qk.toast --es msg \"卡槽成功切换为" + str(name) + "号\"").communicate()
            time.sleep(6)
            if d(textContains='开启精彩').exists:
                d(textContains='开启精彩').click()
            if d(descriptionContains='开启精彩').exists:
                d(descriptionContains='开启精彩').click()

            if d(text='搜索', resourceId='com.tencent.eim:id/name').exists:
                obj = self.slot.getSlotInfo(d, name)  # 得到切换后的QQ号
                info = obj['info']  # info为QQ号
                self.repo.BackupInfo(cate_id, 'using', info, '%s_%s_%s' % (
                d.server.adb.device_serial(), self.type, name,))  # 仓库号，状态，QQ号，备注设备id_卡槽id
            else:  # 切换不成功的情况
                info = self.login(d, args)  # 帐号无法登陆则登陆,重新登陆
                self.slot.backup(d, name, info)  # 登陆之后备份,将备份后的信息传到后台　仓库号，状态，QQ号，备注设备id_卡槽id
                self.repo.BackupInfo(cate_id, 'using', info, '%s_%s_%s' % (
                d.server.adb.device_serial(), self.type, name))  # 将登陆上的仓库cate_id,设备号d，卡槽号name，qq号info，备份到仓库

        else:  # 有空卡槽的情况
            z.set_mobile_data(False)
            time.sleep(3)
            z.set_mobile_data(True)
            time.sleep(8)
            info = self.login(d,z, args)
            self.slot.backup(d, name, info)  # 设备信息，卡槽号，QQ号
            # self.repo.BackupInfo(cate_id, 'using', info,'%s_%s' % (d.server.adb.device_serial(), name))  # 仓库号,使用中,QQ号,设备号_卡槽号


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return QQLiteLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    # type = 'qqlite'
    # slot = slot(type)
    # slot.restore(d, 4)  # 有２小时没用过的卡槽情况，切换卡槽

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    # d.dump(compressed=False)
    args = {"repo_cate_id":"59","time_limit":"3","time_limit1":"120","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)