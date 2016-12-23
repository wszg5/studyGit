# coding:utf-8
import threading
import time
from PIL import Image
from uiautomator import Device
import os,re,subprocess
from Repo import *
from RClient import *
import time, datetime, random
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


    def action(self, d, args):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png"%(self.GetUnique()) )
        codePng = os.path.join(base_dir, "%s_c.png"%(self.GetUnique()) )

        d.server.adb.cmd("shell", "pm clear com.tencent.qqlite").wait()  # 清除缓存
        d.server.adb.cmd("shell",
                         "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity").wait()  # 将qq拉起来
        time.sleep(8)

        cate_id = args["cate_id"]
        numbers = self.repo.GetAccount(cate_id, 120, 1)
        QQNumber = numbers[0]['number']
        QQPassword = numbers[0]['password']
        d(text='登 录').click()
        time.sleep(1)
        d(text='QQ号/手机号/邮箱').set_text(QQNumber)
        time.sleep(2)
        d(resourceId='com.tencent.qqlite:id/password').set_text(QQPassword)
        time.sleep(2)
        d(text='登 录').click()
        time.sleep(2)
        if d(text='QQ轻聊版').exists:
            return  # 放到方法里改为return
        if d(text='启用通讯录').exists:
            return  # 放到方法里改为return
        for i in range(0, 10, +1):
            obj = d(resourceId='com.tencent.qqlite:id/0', className='android.widget.ImageView')
            obj = obj.info
            print (obj)
            obj = obj['bounds']         #验证码处的信息
            print (obj)
            left = obj["left"]          #验证码的位置信息
            top = obj['top']
            right = obj['right']
            bottom = obj['bottom']
            print (left)
            print (top)
            print (right)
            print (bottom)

            d.screenshot(sourcePng)       #截取整个输入验证码时的屏幕


            img = Image.open(sourcePng)
            box = (left, top, right, bottom)  # left top right bottom
            region = img.crop(box)        #截取验证码的图片

            img = Image.new('RGBA', (right - left, bottom - top))
            img.paste(region, (0, 0))

            img.save(codePng)
            im = open(codePng, 'rb').read()




            co = RClient()
            codeResult = co.rk_create(im, 3040)
            code = codeResult["Result"]
            print (code)
            time.sleep(3)
            d(resourceId='com.tencent.qqlite:id/0',index='2',className="android.widget.EditText").set_text(code)
            time.sleep(2)
            d(text='完成',resourceId='com.tencent.qqlite:id/ivTitleBtnRightText').click()
            time.sleep(2)
            if d(text='QQ轻聊版').exists:
                return  # 放到方法里改为return
            # region = region.transpose(Image.ROTATE_180)    #用来将图片旋转
            # region.show()
            # im.paste(region, box)
            # im.show()
        if (args["time_delay"]):
            time.sleep(args["time_delay"])

def getPluginClass(self):
    return QQLiteLogin

if __name__ == "__main__":
    c = QQLiteLogin()
    d = Device("HT49PSK05055")
    d.dump(compressed=False)
    args = {"cate_id":"6","length":"1"};    #cate_id是仓库号，length是数量
    c.action(d, args)