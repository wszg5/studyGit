# coding:utf-8
import threading
import time
from PIL import Image
from PIL.ImageShow import show
import colorsys
from uiautomator import Device
import os,re,subprocess
import util
from Repo import *
from RClient import *
import time, datetime, random
from zservice import ZDevice
from slot import slot
import optparse

class MobilqqLogin:
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
        co = RClient()
        im_id = ""
        co.rk_report_error(im_id)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))

        obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.TextView',descriptionContains='基本信息')  # 当弹出选择QQ框的时候，定位不到验证码图片
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
            print("---------------------------------------------------------------------------")
            print(dominant_color)
            red = dominant_color[0]
            blue =  dominant_color[2]

            if red>blue:
                print('女')
            else:
                print('男')
            return dominant_color
        else:
            return '妖'


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    # slot = slot('mobileqq')
    # slot.restore(d, 5)  # 有time_limit分钟没用过的卡槽情况，切换卡槽

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存
    # slot.restore(d, 9)

    # d.dump(compressed=False)
    args = {"repo_cate_id":"59","time_limit":"30","time_limit1":"120","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
