# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from imageCode import imageCode
from PIL import Image
import os

class QLJudgeQQBind:
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

        while True:
            d.server.adb.cmd("shell", "pm clear com.tencent.qqlite").communicate()  # 清除缓存
            d.server.adb.cmd("shell", "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 将qq拉起来
            time.sleep(8)

            d(text='登 录').click()
            d(textContains='QQ号').click()
            cate_id = args["repo_cate_id"]
            time_limit1 = args['time_limit1']
            numbers = self.repo.GetAccount(cate_id, time_limit1, 1)
            if len(numbers) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"QQ帐号库%s号仓库为空，等待中\"" % cate_id).communicate()
                time.sleep(10)
                return
            QQNumber = numbers[0]['number']  # 即将登陆的QQ号
            QQPassword = numbers[0]['password']
            z.input(QQNumber)
            d(description='请输入密码').click()
            z.input(QQPassword)
            d(text='登 录').click()
            while d(textContains='登录中').exists:
                time.sleep(2)
            time.sleep(3)

            if d(textContains='输入验证码').exists:
                icode = imageCode()
                im_id = ""
                for i in range(0, 30, +1):  # 打码循环
                    if i > 0:
                        icode.reportError(im_id)
                    obj = d(className='android.widget.ImageView')  # 当弹出选择QQ框的时候，定位不到验证码图片
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
                    code = codeResult["Result"]
                    im_id = codeResult["Id"]
                    os.remove(sourcePng)
                    os.remove(codePng)
                    z.input(code)
                    d(text='完成').click()
                    while d(className='android.widget.ProgressBar', index=0).exists:  # 网速不给力时，点击完成后仍然在加载时的状态
                        time.sleep(2)
                    time.sleep(3)
                    if d(text='输入验证码').exists:
                        continue
                    else:
                        break
            if d(textContains='无法登录').exists:
                self.repo.BackupInfo(cate_id, 'frozen', QQNumber, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                continue
            if d(text='联系人').exists:
                self.repo.BackupInfo(cate_id, 'using', QQNumber, '','')  # 仓库号,使用中,QQ号,设备号_卡槽号
                break



        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return QLJudgeQQBind

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # z.input('177751880')
    # z.input('13141314abcd')
    # z.input('brbd')
    args = {"repo_cate_id":"135","time_limit":"0","time_limit1":"120","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)




















