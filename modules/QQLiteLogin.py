# coding:utf-8
import threading
import time
from PIL import Image
from uiautomator import Device
import os,re,subprocess
from Repo import *
from RClient import *
import time, datetime, random
from dbapi import dbapi
from const import const

class QQLiteLogin:
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
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png"%(self.GetUnique()) )
        codePng = os.path.join(base_dir, "%s_c.png"%(self.GetUnique()) )



        d.server.adb.cmd("shell", "pm clear com.tencent.qqlite").wait()  # 清除缓存
        while True:
            d.server.adb.cmd("shell", "am force-stop com.tencent.qqlite").wait()  # 将qq强制停止
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"上一轮没有登陆成功，再次登陆QQ\"")

            d.server.adb.cmd("shell",
                             "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity").wait()  # 将qq拉起来
            time.sleep(3)

            cate_id = args["repo_cate_id"]
            numbers = self.repo.GetAccount(cate_id, 120, 1)

            wait = 1
            while wait==1:                   #判断仓库是否有东西
                try:
                    QQNumber = numbers[0]['number']       #即将登陆的QQ号
                    wait=0
                except Exception :
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到号码\"")
                    time.sleep(20)
            QQPassword = numbers[0]['password']
            time.sleep(1)
            d(text='登 录').click()
            time.sleep(1)
            d(text='QQ号/手机号/邮箱').set_text(QQNumber)    #QQNumber


            time.sleep(1)
            d(resourceId='com.tencent.qqlite:id/password').set_text(QQPassword)     #QQPassword
            time.sleep(1)
            d(text='登 录').click()
            time.sleep(2)
            if d(text='QQ轻聊版').exists:
                return  # 放到方法里改为return
            if d(text='启用通讯录').exists:
                return  # 放到方法里改为return
            if d(text='帐号无法登录', resourceId='com.tencent.qqlite:id/dialogTitle').exists:  # 帐号被冻结
                break

            co = RClient()
            im_id = ""

            for i in range(0, 30 , +1):
                if i > 0:
                    co.rk_report_error(im_id)
                obj = d(resourceId='com.tencent.qqlite:id/0', className='android.widget.ImageView')
                obj = obj.info
                obj = obj['bounds']         #验证码处的信息
                left = obj["left"]          #验证码的位置信息
                top = obj['top']
                right = obj['right']
                bottom = obj['bottom']

                d.screenshot(sourcePng)       #截取整个输入验证码时的屏幕


                img = Image.open(sourcePng)
                box = (left, top, right, bottom)  # left top right bottom
                region = img.crop(box)        #截取验证码的图片

                img = Image.new('RGBA', (right - left, bottom - top))
                img.paste(region, (0, 0))

                img.save(codePng)
                im = open(codePng, 'rb').read()

                codeResult = co.rk_create(im, 3040)
                code = codeResult["Result"]
                im_id = codeResult["Id"]
                os.remove(sourcePng)
                os.remove(codePng)


                d(resourceId='com.tencent.qqlite:id/0',index='2',className="android.widget.EditText").set_text(code)
                time.sleep(1)
                d(text='完成',resourceId='com.tencent.qqlite:id/ivTitleBtnRightText').click()
                time.sleep(2)
                if d(text='登 录').exists:    #密码错误
                    # self.repo.SetAccount(cate_id,'locked',QQNumber)
                    break

                if d(text='帐号无法登录',resourceId='com.tencent.qqlite:id/dialogTitle').exists:         #帐号被冻结
                    # self.repo.SetAccount(cate_id,'frozen',QQNumber)
                    break

                if d(text='QQ轻聊版').exists:
                    return  # 放到方法里改为return
                # region = region.transpose(Image.ROTATE_180)    #用来将图片旋转
                # region.show()
                # im.paste(region, box)
                # im.show()
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return QQLiteLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    import base64
    # s=u'在吗？朋友.。。交流空间来看'
    d.server.adb.cmd("shell",
                     "ime set com.zunyun.qk/.ZImeService").wait()
    from zservice import ZDevice
    z = ZDevice("HT4A4SK00901")
    # z.input(s)
    # d.dump(compressed=False)
    args = {"repo_cate_id":"37","time_limit":"120","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)