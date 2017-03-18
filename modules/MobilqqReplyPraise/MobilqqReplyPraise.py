# coding:utf-8
from RClient import *
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice
from XunMa import *
import traceback
from PIL import Image
import colorsys


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

    def Gender(self, d,i):
        z.heartbeat()
        co = RClient()
        im_id = ""
        co.rk_report_error(im_id)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        obj = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=i) \
            .child(className='android.widget.RelativeLayout', index=1).child(
            resourceId='com.tencent.mobileqq:id/lastMsgTime')  # 得到QQ号
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

    def action(self, d,z,args):
        z.heartbeat()
        gender = args['gender']
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(8)
        d(className='android.widget.TabWidget',index=2).child(className='android.widget.FrameLayout',index=2).child(className='android.widget.RelativeLayout',index=0).click()
        d(text='附近').click()
        while True:
            if d(text='新鲜事').exists:
                break
            else:
                time.sleep(2)
        z.heartbeat()
        d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=2).child(className='android.widget.LinearLayout',index=0).click()     #点击进入自己的主页
        d(descriptionContains='赞').child(className='android.view.View').click()
        # d(descriptionContains='帐户及设置').click()
        # d(descriptionContains='等级').click()
        # d(descriptionContains='赞').click()
        time.sleep(3)
        obj4 = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=1) \
            .child(className='android.widget.RelativeLayout', index=1).child(
            className='android.widget.LinearLayout')  # 用来点击的
        if not obj4.exists:      #没有人赞我情况
            return
        z.heartbeat()
        set1 = set()
        i = 1
        t = 1
        add_count = int(args['EndIndex'])  # 要给多少人发
        while t < add_count + 1:
            obj = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=i) \
                .child(className='android.widget.RelativeLayout', index=1).child(
                className='android.widget.LinearLayout')  # 用来点击的
            obj1 = obj.child(className='android.widget.TextView')
            obj3 = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=i) \
            .child(className='android.widget.RelativeLayout', index=1).child(
            resourceId='com.tencent.mobileqq:id/lastMsgTime')  # 看性别是否存在
            if not gender=='不限':       #给赞我的人发消息，看性别是否有要求
                if obj3.exists:    #对性别有要求的情况，看性别是否有显示
                    z.heartbeat()
                    genderfrom = self.Gender(d,i)    #得到第ｉ个人的真实性别
                    print(genderfrom)
                    if genderfrom != gender:
                        i = i+1
                        continue
                else:
                    z.heartbeat()
                    if d(textContains='暂无更多').exists:
                        break
                    if d(textContains='显示更多').exists:
                        d(textContains='显示更多').click()
                    d.swipe(width / 2, height * 4 / 5, width / 2, height / 5)

                    i = 1
                    continue
            if obj1.exists:    #当对性别没要求时，就判断昵称是否存在
                z.heartbeat()
                obj1 = obj1.info
                name = obj1['text']
                if name in set1:  # 判断是否已经关注过该联系人
                    i = i + 1
                    continue
                else:
                    set1.add(name)
                    print(name)
                obj.click()
                while d(textContains='正在加载').exists:
                    time.sleep(2)
                z.heartbeat()
                d(text='发消息').click()
                d(className='android.widget.EditText').click()
                cate_id = args["repo_material_id"]
                Material = self.repo.GetMaterial(cate_id, 0, 1)
                if len(Material) == 0:
                    d.server.adb.cmd("shell",
                                     "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                    time.sleep(10)
                    return
                Material = Material[0]['content']  # 从素材库取出的要发的材料
                z.heartbeat()
                z.input(Material)
                d(text='发送').click()
                d(text='返回').click()
                i = i+1
                t = t+1

            else:
                if d(textContains='暂无更多').exists:
                    break
                if d(textContains='显示更多').exists:
                    d(textContains='显示更多').click()
                d.swipe(width / 2, height * 4 / 5, width / 2, height / 5)
                i = 1
                continue

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqReplyPraise

if __name__ == "__main__":
    import os
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id":"40",'gender':"不限",'EndIndex':'40',"time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)



















