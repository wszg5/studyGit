# coding:utf-8
import colorsys
import os

import datetime
import random

from PIL import Image

from uiautomator import Device
import  time
from zservice import ZDevice


class MobilqqCancel:

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(8)
        z.heartbeat()
        d(description='帐户及设置').click()
        z.sleep(1.5)
        d(text="设置", resourceId="com.tencent.mobileqq:id/name").click()
        time.sleep(2)
        d( text="辅助功能", resourceId="com.tencent.mobileqq:id/name" ).click( )
        time.sleep(2)
        clickList = [6,14,15,16,17,19]
        Str = d.info  # 获取屏幕大小等信息
        height = Str["displayHeight"]
        width = Str["displayWidth"]
        for i in clickList:
            obj = d( className='com.tencent.widget.Switch', index=i ).child( className="android.widget.CompoundButton",
                                                                             index=1 )
            # obj = d( className='com.tencent.widget.Switch', index=8 ).child( className="android.widget.CompoundButton",index=1 )
            # (77, 217, 101)
            color = self.getColor( d, z, obj )
            if color == (77, 217, 101):
                obj.click( )
            if i <=15:
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                time.sleep(1)



        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def getColor(self,d,z,obj):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        # obj = d(className='com.tencent.widget.Switch', index=6).child(className="android.widget.CompoundButton", index=1)  # 当弹出选择QQ框的时候，定位不到验证码图片
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
            # print("---------------------------------------------------------------------------")
            # print(dominant_color)
            z.heartbeat()
            if None == dominant_color:
                # print('见鬼了')
                return
            return dominant_color

def getPluginClass():
    return MobilqqCancel

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("cc0e9474")
    z = ZDevice("cc0e9474")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, z,args)
