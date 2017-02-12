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

class EIMLoginNoSlot:
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
            time_limit = args['time_limit']         #帐号提取时间间隔
            wait = 1
            while wait == 1:  # 判断仓库是否有东西　　　　　　　直到仓库有东西为止
                cate_id = args["repo_cate_id"]
                numbers = self.repo.GetAccount(cate_id, time_limit, 1)
                print(numbers)
                try:
                    QQNumber = numbers[0]['number']  # 即将登陆的QQ号
                    wait = 0
                except Exception:
                    d.server.adb.cmd("shell","am broadcast -a com.zunyun.zime.toast --es msg \"EIM%s号帐号库为空，等待中\""%cate_id).communicate()
                    time.sleep(20)
            QQPassword = numbers[0]['password']
            d.server.adb.cmd("shell", "pm clear com.tencent.eim").communicate()  # 清除缓存
            d.server.adb.cmd("shell", "am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            time.sleep(5)
            d(className='android.widget.Button', index=1, clickable='true').click()
            time.sleep(2)
            d(className='android.widget.EditText', text='企业QQ号/手机号/邮箱').set_text(QQNumber)  # 3001313499  QQNumber  3001346198
            d(resourceId='com.tencent.eim:id/password', description='请输入密码').set_text(QQPassword)  # Bn2kJq5l   QQPassword
            d(text='登 录', resourceId='com.tencent.eim:id/login').click()
            time.sleep(4)
            if d(text='企业QQ').exists:        #这些判断为直接登陆成功的情况
                d(text='企业QQ').click()
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()
            if d(text='搜索', resourceId='com.tencent.eim:id/name').exists:  # 直接登陆成功的情况
                return  QQNumber   # 放到方法里改为return

            if d(text='帐号无法登录', resourceId='com.tencent.eim:id/dialogTitle').exists:  # 帐号被冻结
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
                while d(className='android.widget.ProgressBar',index=0).exists:     #网速较慢，校验验证码未完成的情况
                    time.sleep(2)

                if d(text='搜索', resourceId='com.tencent.eim:id/name').exists:
                    return  QQNumber# 放到方法里改为return
                if d(text='输入验证码').exists:           #验证码输入错误的情况
                    continue
                else:
                    break

    def action(self, d,z, args):
        z.set_mobile_data(False)
        time.sleep(5)
        z.set_mobile_data(True)
        time.sleep(8)
        info = self.login(d, args)

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))
def getPluginClass():
    return EIMLoginNoSlot

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT49XSK01858")
    z = ZDevice("HT49XSK01858")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()



    args = {"repo_cate_id":"55","time_limit":"0","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)