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

    def login(self,d,args):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        codePng = os.path.join(base_dir, "%s_c.png" % (self.GetUnique()))


        wait = 1
        while wait == 1:  # 判断仓库是否有东西
            cate_id = args["repo_cate_id"]
            time_limit = args['time_limit']
            numbers = self.repo.GetAccount(cate_id, time_limit, 1)
            print(numbers)

            try:
                QQNumber = numbers[0]['number']  # 即将登陆的QQ号
                wait = 0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到EIM账号\"").communicate()
                time.sleep(20)
        QQPassword = numbers[0]['password']
        time.sleep(1)
        t = 1
        while t == 1:
            d.server.adb.cmd("shell", "pm clear com.tencent.eim").communicate()  # 清除缓存
            d.server.adb.cmd("shell", "am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            time.sleep(5)
            d(className='android.widget.Button', index=1, clickable='true').click()
            d(className='android.widget.EditText', text='企业QQ号/手机号/邮箱').set_text(QQNumber)  # 3001313499  QQNumber  3001346198
            d(resourceId='com.tencent.eim:id/password', description='请输入密码').set_text(QQPassword)  # Bn2kJq5l   QQPassword
            d(text='登 录', resourceId='com.tencent.eim:id/login').click()
            time.sleep(4)
            if d(text='企业QQ').exists:
                d(text='企业QQ').click()
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()
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
                time.sleep(4)

                if d(text='登 录').exists:  # 密码错误
                    self.repo.BackupInfo(cate_id, 'locked', QQNumber, '')  # 仓库号,使用中,QQ号,设备号_卡槽号
                    break

                if d(text='帐号无法登录', resourceId='com.tencent.eim:id/dialogTitle').exists:  # 帐号被冻结
                    self.repo.BackupInfo(cate_id, 'frozen', QQNumber, '')
                    break

                if d(text='身份过期', resourceId='com.tencent.eim:id/dialogTitle').exists:
                    self.repo.BackupInfo(cate_id, 'expired', QQNumber, '')
                    break

                if d(text='搜索', resourceId='com.tencent.eim:id/name').exists:
                    return  QQNumber# 放到方法里改为return




    def action(self, d,z, args):
        time_limit = args['time_limit']
        cate_id = args["repo_cate_id"]
        name = self.slot.getEmpty(d)  # 取空卡槽
        print(name)
        if name == 0:
            name = self.slot.getSlot(d, time_limit)  # 没有空卡槽，取２小时没用过的卡槽
            while name == 0:  # 2小时没有用过的卡槽也为空的情况
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"卡槽全满，无间隔时间段未用\"").communicate()
                time.sleep(30)
                name = self.slot.getSlot(d, time_limit)

            z.set_mobile_data(False)
            time.sleep(3)
            self.slot.restore(d, name)  # 有２小时没用过的卡槽情况，切换卡槽
            print("切换为"+str(name))
            z.set_mobile_data(True)
            time.sleep(8)
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"卡槽成功切换为"+str(name)+"号\"").communicate()
            time.time(1)
            d.server.adb.cmd("shell","am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            time.sleep(5)
            if d(text='搜索', resourceId='com.tencent.eim:id/name').exists:
                obj = self.slot.getSlotInfo(d, name)  # 得到切换后的QQ号
                info = obj['info']  # info为QQ号
                self.repo.BackupInfo(cate_id, 'using', info,'%s_%s' % (d.server.adb.device_serial(), name))  # 仓库号，状态，QQ号，备注设备id_卡槽id
            else:  # 切换不成功的情况
                info = self.login(d, args)  # 帐号无法登陆则登陆,重新登陆
                self.slot.backup(d, name, info)  # 登陆之后备份,将备份后的信息传到后台　仓库号，状态，QQ号，备注设备id_卡槽id
                self.repo.BackupInfo(cate_id, 'using', info, '%s_%s' % (
                d.server.adb.device_serial(), name))  # 将登陆上的仓库cate_id,设备号d，卡槽号name，qq号info，备份到仓库





            if d(text='帐号无法登录') or d(text='身份过期').exists:
                info = self.login(d,args)  # 帐号无法登陆则登陆,重新注册登陆
                self.repo.BackupInfo(cate_id,d,name,info)      #将登陆上的仓库cate_id,设备号d，卡槽号name，qq号info，备份到仓库
                self.slot.backup(d, name, info)  # 登陆之后备份

            else:
                return

        else:  # 有空卡槽的情况
            z.set_mobile_data(False)
            time.sleep(3)
            z.set_mobile_data(True)
            time.sleep(8)
            info = self.login(d, args)
            self.slot.backup(d, name, info)  # 设备信息，卡槽号，QQ号
            self.repo.BackupInfo(cate_id, 'using', info,'%s_%s' % (d.server.adb.device_serial(), name))  # 仓库号,使用中,QQ号,设备号_卡槽号

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))
def getPluginClass():
    return EIMLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # d.dump(compressed=False)
    slot = slot('eim')

    slot.restore(d, 2)  # 有２小时没用过的卡槽情况，切换卡槽


    args = {"repo_cate_id":"55","time_limit":"120","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)