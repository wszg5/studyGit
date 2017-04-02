# coding:utf-8
import threading
import time
from PIL import Image
from uiautomator import Device

from imageCode import imageCode

from Repo import *
import time, datetime, random
from zservice import ZDevice
from slot import slot
import os


class EIMTemporaryCut:
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

    def login(self,d,args,z):

        z.heartbeat()

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        codePng = os.path.join(base_dir, "%s_c.png" % (self.GetUnique()))
        z.sleep(1)

        t = 1
        while t == 1:         #直到登陆成功为止
            time_limit1 = args['time_limit1']
            cate_id = args["repo_cate_id"]
            numbers = self.repo.GetAccount(cate_id, time_limit1, 1)
            if len(numbers) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"EIM%s号帐号库为空，等待中\"" % cate_id).communicate()
                z.sleep(10)
                return
            QQNumber = numbers[0]['number']  # 即将登陆的QQ号
            QQPassword = numbers[0]['password']
            print('QQ号是：%s,QQ密码是：%s'%(QQNumber,QQPassword))
            d.server.adb.cmd("shell", "pm clear com.tencent.eim").communicate()  # 清除缓存
            d.server.adb.cmd("shell", "am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
<<<<<<< HEAD
            z.sleep(3)
            while d(textContains='正在更新').exists:
                z.sleep(2)
            z.sleep(6)
=======
            z.sleep(5)

>>>>>>> 4e4f21f1884a754d94ef7f78793387f981d2652c
            z.heartbeat()

            d(className='android.widget.Button', index=1, clickable='true').click()
            z.sleep(2)
            d(className='android.widget.EditText', text='企业QQ号/手机号/邮箱').set_text(QQNumber)  # 3001313499  QQNumber  3001346198
            d(resourceId='com.tencent.eim:id/password', description='请输入密码').set_text(QQPassword)  # Bn2kJq5l   QQPassword
            d(text='登 录').click()
            z.sleep(4)
            if d(text='企业QQ').exists:
                d(text='企业QQ').click()
<<<<<<< HEAD
            if d(text='仅此一次').exists:
                d(text='仅此一次').click()
=======
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()

>>>>>>> 4e4f21f1884a754d94ef7f78793387f981d2652c
            z.heartbeat()


            if d(text='搜索').exists:  # 直接登陆成功的情况

                return  QQNumber   # 放到方法里改为return

            if d(text='帐号无法登录', resourceId='com.tencent.eim:id/dialogTitle').exists:  # 帐号被冻结
                self.repo.BackupInfo(cate_id, 'frozen', QQNumber, '','')
                break

            icode = imageCode()
            im_id = ""
            for i in range(0, 30, +1):  # 打码循环
                if i > 0:
                    icode.reportError(im_id)

                obj = d(resourceId='com.tencent.eim:id/name', className='android.widget.ImageView')
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
                if codeResult is None:
                    z.toast('打码账号密码错误')
                    z.sleep(5)
                    return
                code = codeResult["Result"]

                im_id = codeResult["Id"]
                os.remove(sourcePng)
                os.remove(codePng)
                z.heartbeat()

                d(resourceId='com.tencent.eim:id/name', index='2', className="android.widget.EditText").set_text(code)
                z.sleep(1)
                d(text='完成').click()
                z.sleep(4)
                while d(className='android.widget.ProgressBar',index=0).exists:     #网速较慢，校验验证码未完成的情况

                    z.heartbeat()

                    z.sleep(2)

                if d(text='搜索', resourceId='com.tencent.eim:id/name').exists:
                    return  QQNumber# 放到方法里改为return
                if d(text='输入验证码').exists:           #验证码输入错误的情况

                    z.heartbeat()

                    continue
                else:
                    break


    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "settings put global airplane_mode_on 1").communicate()
        d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true").communicate()
        z.sleep(5)
        d.server.adb.cmd("shell", "settings put global airplane_mode_on 0").communicate()
        d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false").communicate()
        z.heartbeat()
        while True:
            ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                break
            z.sleep(2)
        z.heartbeat()
        serialinfo = z.generateSerial("788")  # 修改串号等信息
        print('登陆时的serial%s' % serialinfo)
        QQnumber = self.login(d, args,z)
        z.sleep(3)
        z.heartbeat()
        time.sleep(4)
        self.slot.backup(d,1, QQnumber)  # 设备信息，卡槽号，QQ号
        d.server.adb.cmd("shell", "pm clear com.tencent.eim").communicate()  # 清除缓存
        d.server.adb.cmd("shell", "am force-stop com.tencent.eim").wait()  # 强制停止

        gener = args['kind']
        if gener == '普通QQ':
            z.heartbeat()
            self.slot.restore(d, 1, "com.tencent.mobileqq")  # 有２小时没用过的卡槽情况，切换卡槽
            d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            z.heartbeat()
            z.sleep(2)
            while d(textContains='正在更新').exists:
                z.sleep(2)
            z.sleep(8)
            if d(textContains='登录').exists:
                d(textContains='登录').click()
                z.sleep(5)

        else:     #轻聊版
            z.heartbeat()
            self.slot.restore(d, 1, "com.tencent.qqlite")  # 有２小时没用过的卡槽情况，切换卡槽
            d.server.adb.cmd("shell", "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            z.heartbeat()
            z.sleep(2)
            while d(textContains='正在更新').exists:
                z.sleep(2)
            z.sleep(8)
            if d(textContains='登录').exists:
                d(textContains='登录').click()
                z.sleep(5)


        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return EIMTemporaryCut

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    d = Device("8HVSMZKBEQFIBQUW")
    z = ZDevice("8HVSMZKBEQFIBQUW")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_cate_id":"34","time_limit1":"10","kind":"轻聊版","time_delay":"3"};    #cate_id是仓库号，length是数量

    o = clazz()
    o.action(d,z, args)






