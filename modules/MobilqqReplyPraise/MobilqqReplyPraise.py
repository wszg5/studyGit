# coding:utf-8
from RClient import *
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
from XunMa import *
import traceback
from PIL import Image
import colorsys
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MobilqqReplyPraise:
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
        co = RClient()
        im_id = ""
        co.rk_report_error(im_id)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.TextView',
                descriptionContains='基本信息')  # 当弹出选择QQ框的时候，定位不到验证码图片
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

    def action(self, d,z,args):
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(8)
        d(descriptionContains='帐户及设置').click()
        d(descriptionContains='等级').click()
        d(descriptionContains='赞').click()
        d(className='android.widget.AbsListView').child()

        set1 = set()
        change = 0
        i = 1
        t = 1
        ending = 0  # 用来判断是否到底
        EndIndex = int(args['EndIndex'])  # ------------------
        while t < EndIndex + 1:
            cate_id = args["repo_material_id"]  # ------------------
            Material = self.repo.GetMaterial(cate_id, 0, 1)

            try:
                Material = Material[0]['content']  # 从素材库取出的要发的材料
                wait = 0
            except Exception:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()

            time.sleep(1)
            obj = d(className='android.widget.ListView').child(className='android.widget.RelativeLayout', index=i).child(
                className='android.widget.LinearLayout').child(className='android.widget.TextView')  # 得到QQ号
            if obj.exists:
                change = 1  # 好友存在且未被添加的情况出现，change值改变
                obj1 = obj.info
                name = obj1['text']
                if name in set1:  # 判断是否已经给该人发过消息
                    i = i + 1
                    continue
                else:
                    set1.add(name)
                    print(name)
                obj.click()
                GenderFrom = args['gender']  # -------------------------------
                if GenderFrom != '不限':
                    obj = d(className='android.widget.LinearLayout', index=1).child(
                        className='android.widget.LinearLayout').child(className='android.widget.ImageView',
                                                                       index=1)  # 看性别是否有显示
                    if obj.exists:
                        Gender = obj.info
                        Gender = Gender['contentDescription']
                        if Gender == GenderFrom:
                            print()
                        else:  # 如果性别不符号的情况
                            d(description='返回').click()
                            i = i + 1
                            continue
                    else:  # 信息里没有显示出性别的话
                        d(description='返回').click()
                        i = i + 1
                        continue

                d(text='发消息').click()

                time.sleep(1)
                obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
                obj = obj['text']
                lenth = len(obj)
                m = 0
                while m < lenth:
                    d.press.delete()
                    m = m + 1
                d(className='android.widget.EditText').click()
                z.input(Material)  # ----------------------------------------
                d(text='发送').click()
                time.sleep(1)
                d(description='返回').click()
                d(text='通讯录').click()
                i = i + 1
                t = t + 1
                continue

            else:
                if change == 0:  # 一次还没有点击到人
                    i = i + 1
                    continue
                else:
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    time.sleep(2)

                    if ending == 1:  # 结束条件
                        return
                    if d(textContains='位联系人').exists:
                        ending = 1

                        # return
                    for g in range(0, 12, +1):
                        time.sleep(0.5)
                        obj = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',
                                                                           index=g).child(
                            className='android.widget.LinearLayout').child(className='android.view.View')  # 得到微信名
                        obj = obj.info
                        Tname = obj['text']
                        if Tname == name:
                            break
                    i = g + 1
                    continue

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqReplyPraise

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # str = d.info  # 获取屏幕大小等信息
    # height = str["displayHeight"]
    # width = str["displayWidth"]
    # while True:
    #     d.swipe(width / 2, height * 4 / 5, width / 2, height / 4)

    args = {"repo_number_cate_id":"38","add_count":"3","time_delay":"3"}    #cate_id是仓库号，length是数量

    o.action(d,z, args)



















