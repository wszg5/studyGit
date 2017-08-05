# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from PIL import Image
import colorsys

class WXYaoYiYao:

    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def Gender(self, d):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        obj = d(descriptionContains='相距').child(className='android.widget.LinearLayout', index=0).child(
            className='android.widget.ImageView')
        if obj.exists:
            z.heartbeat()
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
            # show(region)　　　　　　　#展示资料卡上的信息
            image = region.convert('RGBA')
            # 生成缩略图，减少计算量，减小cpu压力
            image.thumbnail((200, 200))
            max_score = None
            dominant_color = None
            for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
                # 跳过纯黑色
                if a == 0:
                    continue
                saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
                y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
                y = (y - 16.0) / (235 - 16)
                # 忽略高亮色
                if y > 0.9:
                    continue

                score = (saturation + 0.1) * count
                if score > max_score:
                    max_score = score
                    dominant_color = (r, g, b)
            z.heartbeat()
            # print("---------------------------------------------------------------------------")
            # print(dominant_color)
            if None == dominant_color:
                # print('见鬼了')
                return '不限'
            red = dominant_color[0]
            blue = dominant_color[2]

            if red > blue:
                # print('女')
                return '女'
            else:
                # print('男')
                return '男'
        else:  # 没有基本资料的情况
            return '不限'

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(5)

        gender1 = args['gender']

        if d(text='我知道了').exists:
            d(text='我知道了').click()
            z.sleep(2)
        EndIndex = int(args['EndIndex'])         #------------------
        z.wx_action("openyaoyiyao")
        if d(text='我知道了').exists:
            d(text='我知道了').click()
        z.heartbeat()
        t = 0
        while True:
            if t<EndIndex:
                cate_id = args["repo_material_id"]  # ------------------
                Material = self.repo.GetMaterial(cate_id, 0, 1)
                if len(Material) == 0:
                    d.server.adb.cmd("shell",
                                     "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                    z.sleep(10)
                    return
                message = Material[0]['content']  # 从素材库取出的要发的材料
                z.heartbeat()
                z.wx_yaoyiyao()
                z.sleep(5)
                while d(textContains='正在搜').exists:
                    z.sleep(2)
                z.heartbeat()
                if gender1 != '不限':
                    z.heartbeat()
                    gender2 = self.Gender(d)
                    z.heartbeat()
                    if gender1 == gender2:  # gender1是外界设定的，gender2是读取到的
                        time.sleep(0.5)
                    else:
                        continue
                z.heartbeat()
                if d(textContains='打招呼消息').exists:
                    d(textContains='打招呼消息').click()
                    z.sleep(1)
                    d(text='返回').click()
                d(textContains='相距').click()
                d(text='打招呼').click()
                d(className='android.widget.EditText').click()
                z.input(message)     #message
                d(text='发送').click()
                t = t+1
                z.heartbeat()
                d(description='返回').click()
            else:
                break
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return WXYaoYiYao

if __name__ == "__main__":
    import os
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")
    # z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id": "39",'EndIndex':'1000','gender':"不限","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
