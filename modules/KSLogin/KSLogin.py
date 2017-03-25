# coding:utf-8
from uiautomator import Device
from Repo import *
from PIL import Image
import os
from RClient import *
from zservice import ZDevice
import time, datetime, random


class KSLogin:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z,args):

        d.server.adb.cmd("shell", "pm clear com.smile.gifmaker").communicate()  # 清除缓存
        d.server.adb.cmd("shell","am start -n com.smile.gifmaker/com.yxcorp.gifshow.HomeActivity").communicate()  # main拉起
        z.generateSerial("888")

        time.sleep(5)
        while 1:
            time.sleep(1)
            if d(text='调整音量', className='android.widget.TextView').exists:
                d(text='确定', className='android.widget.Button').click()
                break
            elif d(descriptionContains='快手', className='android.widget.ImageView').exists:
                break



        d(index=0, className='android.widget.ImageButton').click()
        d(descriptionContains='腾讯', className='android.widget.ImageView').click()

        while 1:
            time.sleep(1)
            if d(text='切换帐号', className='android.widget.TextView').exists:
                d(text='切换帐号', className='android.widget.TextView').click()
                break
            elif d(text='添加帐号').exists:
                break

        if d(text='添加帐号', className='android.widget.TextView').exists:
            d(text='添加帐号', className='android.widget.TextView').click()
        cateId = args['number_id']
        while 1:  # 判断仓库是否有东西
            try:
                numbers = self.repo.GetAccount(cateId, 120, 1)
                qqNumber = numbers[0]['number']  # 即将登陆的QQ号
                break
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到号码\"")
                time.sleep(5)
        qqPassword = numbers[0]['password']

        d(textContains='QQ', className='android.widget.EditText').set_text(qqNumber)
        d(index=1, className='android.widget.EditText').set_text(qqPassword)
        d(text='登 录', className='android.widget.Button').click()
        time.sleep(2)
        if d(textContains='选择', className='android.widget.TextView').exists:
            d(text='QQ', className='android.widget.TextView').click()
            self.heatCode(d)

        while 1:
            time.sleep(1)
            if d(descriptionContains='快手', className='android.widget.ImageView').exists:
                break
        d(index=0, className='android.widget.ImageButton').click()
        d(text='查找', className='android.widget.TextView').click()
        d(text='手机通讯录', className='android.widget.TextView').click()

        while 1:
            time.sleep(1)
            if d(text='允许访问通讯录', className='android.widget.Button').exists:
                d(text='允许访问通讯录', className='android.widget.Button').click()
                break
            elif d(text='关注', className='android.widget.TextView').exists:
                break

        if d(text='绑定手机', className='android.widget.TextView').exists:
            d(text='以后再说', className='android.widget.Button').click()

        # self.scrollCell(d, z, args)

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


    def scrollCell(self, d, z, args):
        materialId = args["material_id"]

        info = d(index=1, className='android.support.v7.widget.RecyclerView').info
        bHeight = info["visibleBounds"]["bottom"] - info["visibleBounds"]["top"]
        bWidth = info["visibleBounds"]["right"] - info["visibleBounds"]["left"]
        count = d(index=1, className='android.support.v7.widget.RecyclerView').info['childCount']
        count =count-1
        numberArr = []
        judge = True

        while judge==True:
            if judge == False:
                break
            for i in range(0, count):

                obj = d(index=1, className='android.support.v7.widget.RecyclerView').child(index=i,className='android.widget.LinearLayout').child(index=1,className='android.widget.LinearLayout')
                if obj.exists:
                    obj1 = obj.child(index=1,className='android.widget.TextView')
                    if obj1.exists:
                        text= obj1.info["text"]
                        print text
                        if text in numberArr:
                            ok='ok'
                        else:
                            if text.isdigit():
                                numberArr.append(text)
                                obj.click()
                                while 1:
                                    material = self.repo.GetMaterial(materialId, 0, 1)
                                    if len(material) == 0:
                                        d.server.adb.cmd("shell",
                                                         "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % materialId).communicate()
                                        time.sleep(5)
                                    else:
                                        break
                                message = material[0]['content']  # 取出验证消息的内容
                                d(index=3, className='android.widget.ImageButton').click()
                                d(index=0, className='android.widget.EditText').click()
                                z.input(message)
                                d(text='发送', className='android.widget.Button').click()

                                d.click(40,75)
                                d.click(40, 75)
                                d(index=1, className='android.widget.ImageButton').click()


                    if count == i + 1:
                        d.swipe(bWidth / 2, bHeight, bWidth / 2, 0)
                        nstr = d(index=1, className='android.support.v7.widget.RecyclerView').child(index=i,className='android.widget.LinearLayout')
                        nstr =nstr.child(index=1,className='android.widget.LinearLayout').child(index=1,className='android.widget.TextView').info["text"]
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


    def heatCode(self,d):
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
                obj = d(index = 0, className = 'android.widget.ImageView')  # 获取屏幕大小等信息
                if obj.exists:
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

                d(index = 2, className = 'android.widget.EditText').set_text(code)
                d(text='完成', className='android.widget.TextView').click()
                while 1:
                    time.sleep(1)
                    if d(text='授权并登录', className='android.widget.Button').exists:
                        d(text='授权并登录', className='android.widget.Button').click()
                        break
                    elif d(text='看不清？换一张', className='android.widget.TextView').exists:
                        d(text='看不清？换一张', className='android.widget.TextView').click()
                        return self.heatCode(d)



def getPluginClass():
    return KSLogin

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"material_id": "40","number_id":"137", "time_delay": "1"};
    o.action(d, z, args)






