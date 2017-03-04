# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
from PIL import Image
import colorsys
from RClient import *


class TIMAddressCollectDataWithSex:

    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def Gender(self,d):
        co = RClient()
        im_id = ""
        co.rk_report_error(im_id)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        obj = d(index=0, className='android.widget.TextView',descriptionContains='基本信息')  # 当弹出选择QQ框的时候，定位不到验证码图片
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
            if None ==dominant_color:
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
        else:                          #没有基本资料的情况
            return '不限'


    def scrollCell(self, d, args):
        while d(text='正在发送请求', className='android.widget.TextView').exists:
            time.sleep(2)

        maleNumberCateId = args["repo_maleNumberCateId_id"]
        femaleNumberCateId = args["repo_femaleNumberCateId_id"]
        nullNumberCateId = args["repo_nullNumberCateId_id"]

        info = d(index=0, className='android.widget.AbsListView').info
        bHeight = info["visibleBounds"]["bottom"] - info["visibleBounds"]["top"]
        bWidth = info["visibleBounds"]["right"] - info["visibleBounds"]["left"]
        # info = d(index=0, className='android.widget.AbsListView').child(index=2,className='android.widget.LinearLayout').info
        # lHeight = info["visibleBounds"]["bottom"] - info["visibleBounds"]["top"]
        count = d(index=0, className='android.widget.AbsListView').info['childCount']
        numberArr = []
        judge = True

        while judge==True:
            if judge == False:
                break
            for i in range(0, count):

                obj = d(index=0, className='android.widget.AbsListView').child(index=i,className='android.widget.LinearLayout')
                if obj.exists:
                    number = obj.info["contentDescription"]
                    if number in numberArr:
                        ok='ok'
                    else:
                        if number.isdigit():
                            obj.click()
                            d(index=3, className='android.widget.ImageView').click()

                            numberArr.append(number)
                            gender = self.Gender(d)
                            if gender == '不限':  # gender是外界设定的，gender2是读取到的
                                self.repo.uploadPhoneNumber(number, nullNumberCateId)
                            elif gender == '男':
                                self.repo.uploadPhoneNumber(number, maleNumberCateId)
                            elif gender == '女':
                                self.repo.uploadPhoneNumber(number, femaleNumberCateId)
                            d(textContains='返回').click()
                            d(text='电话', className='android.widget.TextView').click()

                    if count == i + 1:
                        d.swipe(bWidth / 2, bHeight, bWidth / 2, 0)
                        nstr = d(index=0, className='android.widget.AbsListView').child(index=i,className='android.widget.LinearLayout').info["contentDescription"]
                        if nstr == numberArr[-1]:
                            judge = 'False'
                            break

                else:
                    if i==0:
                        continue
                    else:
                        judge = 'False'
                        break


    def action(self, d, z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(3)

        d(description='快捷入口', className='android.widget.ImageView').click()
        d(text = '加好友', className = 'android.widget.TextView').click()
        d(text='添加手机联系人', className='android.widget.TextView').click()
        time.sleep(2)

        self.scrollCell(d, args)

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMAddressCollectDataWithSex

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT52DSK00474")
    z = ZDevice("HT52DSK00474")
    # print(d.dump(compressed=False))
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_maleNumberCateId_id":"108","repo_femaleNumberCateId_id":"108","repo_nullNumberCateId_id":"108","time_delay":"3"};    #cate_id是仓库号，length是数量
    # o.action(d,z, args)
    # for i in range(0,10):
    #     obj = d(index=0, className='android.widget.AbsListView').child(index=i,className='android.widget.LinearLayout').child(
    #                 index=1, className='android.widget.TextView').info['text']
    #     print obj
