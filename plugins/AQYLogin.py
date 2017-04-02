# coding:utf-8
from uiautomator import Device
from Repo import *
from PIL import Image
import time
import os
from RClient import *
from zservice import ZDevice
import time, datetime, random


class AQYLogin:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z,args):
        cateId = args['number_id']

        d.server.adb.cmd("shell", "pm clear com.qiyi.video").communicate()  # 清除缓存
        d.server.adb.cmd("shell","am start -n com.qiyi.video/org.qiyi.android.video.MainActivity").communicate()  # main拉起

        wait = 1
        while wait == 1:  # 判断仓库是否有东西
            try:
                numbers = self.repo.GetAccount(cateId, 120, 1)
                qqNumber = numbers[0]['number']  # 即将登陆的QQ号
                wait = 0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到号码\"")
                time.sleep(5)
        qqPassword = numbers[0]['password']

        while 1:
            time.sleep(1)
            if d(text='我的', className='android.widget.RadioButton').exists:
                break

        d(text='我的', className='android.widget.RadioButton').click()
        d(text='我的', className='android.widget.RadioButton').click()
        d(text='登录', className='android.widget.TextView').click()

        d(text='其他方式登录', className='android.widget.TextView').click()
        d(textContains='QQ', className='android.widget.TextView').click()

        while 1:
            time.sleep(1)
            if d(index=1, className='android.webkit.WebView').exists:
                break

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.click(width / 2, height * 121 / 444)
        z.input(qqNumber)
        d.click(270, height * 151 / 444)
        z.input(qqPassword)
        d.click(270, height * 401 / 888)

        time.sleep(4)
        if not d(text='绑定手机', className='android.widget.TextView').exists:
            self.heatCode(d,z)

        d.press("back")
        d.press("back")
        d(index=0, className='android.widget.RelativeLayout').child(index=1,className='android.widget.ImageView').click()
        d(text='通讯录', className='android.widget.TextView').click()


        while 1:
            time.sleep(1)
            if d(text='聊天', className='android.widget.TextView').exists:
                break

        self.scrollCell(d, z, args)

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


    def scrollCell(self, d, z, args):
        materialId = args["material_id"]

        info = d(index=3, className='android.widget.ListView').info
        bHeight = info["visibleBounds"]["bottom"] - info["visibleBounds"]["top"]
        bBottom = info["visibleBounds"]["bottom"]
        bWidth = info["visibleBounds"]["right"] - info["visibleBounds"]["left"]
        count = d(index=3, className='android.widget.ListView').info['childCount']
        numberArr = []
        judge = True

        while judge==True:
            if judge == False:
                break
            for i in range(0, count):

                obj = d(index=3, className='android.widget.ListView').child(index=i,className='android.widget.RelativeLayout')
                if obj.exists:
                    obj1 = obj.child(index=0,className='android.widget.TextView')
                    if obj1.exists:
                        text= obj1.info["text"]
                        if text in numberArr:
                            ok='ok'
                        else:
                            if text.isdigit():
                                numberArr.append(text)

                                if obj.child(text='聊天', className='android.widget.TextView').exists:
                                    while 1:
                                        material = self.repo.GetMaterial(materialId, 0, 1)
                                        if len(material) == 0:
                                            d.server.adb.cmd("shell","am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % materialId).communicate()
                                            time.sleep(5)
                                        else:
                                            break
                                    message = material[0]['content']  # 取出验证消息的内容

                                    obj.child(text='聊天', className='android.widget.TextView').click()
                                    d(index=0, className='android.widget.EditText').click()
                                    z.input(message)
                                    d(text='发送', className='android.widget.TextView').click()
                                    d(text='返回', className='android.widget.TextView').click()
                                    print text

                    if count == i + 1:
                        time.sleep(1)
                        d.swipe(bWidth / 2, bHeight, bWidth / 2, 0)
                        nstr = d(index=3, className='android.widget.ListView').child(index=i,className='android.widget.RelativeLayout').child(index=0,className='android.widget.TextView')
                        if nstr.exists:
                            nstr = nstr.info["text"]
                            if nstr == numberArr[-1]:
                                judge = 'False'
                                break

                else:
                    if i==0:
                        continue
                    else:
                        judge = 'False'
                        break


    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum


    def heatCode(self,d,z):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        codePng = os.path.join(base_dir, "%s_c.png" % (self.GetUnique()))

        if 1:  # 需要验证码的情况
            co = RClient()
            im_id = ""
            for i in range(0, 30, +1):  # 打码循环
                if i > 0:
                    co.rk_report_error(im_id)
                str = d.info  # 获取屏幕大小等信息
                height = str["displayHeight"]
                width = str["displayWidth"]
                left = width*31/540  # 验证码的位置信息
                top = height*249/888
                right = width*271/540
                bottom = height*348/888

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

                d.click(width*391/540,height*298/888)
                z.input(code)
                time.sleep(1)
                d.click(width/2,height*456.5/888)
                time.sleep(4)
                if d(text='绑定手机', className='android.widget.TextView').exists:
                    break


def getPluginClass():
    return AQYLogin

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT52ESK00321")
    z = ZDevice("HT52ESK00321")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # d.server.adb.cmd("shell", "am start -a android.intent.action.MAIN -n com.android.settings/.Settings").communicate()    #打开android设置页面

    args = {"material_id": "40","number_id":"137", "time_delay": "1"};
    o.action(d, z, args)
    # o.scrollCell(d,args)
