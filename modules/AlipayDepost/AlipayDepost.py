# coding:utf-8
from uiautomator import Device
from Repo import *
from RClient import *
import os, datetime, string, random
from zservice import ZDevice
import sys
reload(sys)
from PIL import Image
import colorsys
from XunMa import *
from Inventory import *

class AlipayRegister:
    def __init__(self):
        self.repo = Repo()
        self.xuma = None

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def Gender(self,d,obj):
        co = RClient()
        im_id = ""
        co.rk_report_error(im_id)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
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


    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.eg.android.AlipayGphone").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin").communicate()  # 拉起来
        d(resourceId='com.alipay.mobile.socialwidget:id/contact_container').click()
        d(text='新的朋友').click()
        d(text='添加手机联系人').click()#支付宝通讯录检存，（字段：手机号码*，*昵称，*会员级别，*支付宝账户，*性别，是否实名，*地区，星座，*真实姓名，是否一对多
        # 【附带字段：身高，体重，年龄，职业，收入，兴趣爱好】）#支付宝账号如果遇到一对多的账户，选择第一个作为参考资料，同时字段做个标记。
        while not d(text='搜索').exists:
            time.sleep(2)
        i = 0
        set1 = set()
        while True:
            judexist = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=i)\
                .child(className='android.widget.LinearLayout').child(className='android.widget.TextView',index=0)
            if judexist.exists:
                phoneNumber = judexist.info['text']
                print(phoneNumber)      #要保存的电话号码
                if phoneNumber in set1:
                    i = i+1
                    continue
                set1.add(phoneNumber)
                judexist.click()        #点击第i个人
                d(text='显示更多').click()
                if d(className='android.widget.ListView').child(className='android.widget.FrameLayout').child(className='android.widget.TextView').exists:
                    nickname = d(className='android.widget.ListView').child(className='android.widget.FrameLayout').child(className='android.widget.TextView').info['text']   #要保存的昵称
                else:
                    nickname = '空'
                if d(text='支付宝账户').exists:
                    account = d(textStartsWith='1').info['text']     #要保存的帐号
                else:
                    account = '空'
                if d(text='真实姓名').exists:
                    path = d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=2) \
                        .child(className='android.widget.LinearLayout', index=0).child(
                        className='android.widget.LinearLayout', index=0) \
                        .child(className='android.widget.LinearLayout', index=1).child(
                        className='android.widget.TextView', index='1')
                    gender = self.Gender(d,path)


                if d(text='地区').exists:
                    area = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=2)\
                        .child(className='android.widget.LinearLayout',index=0).child(className='android.widget.LinearLayout',index=0)\
                        .child(className='android.widget.LinearLayout',index=2).child(className='android.widget.TextView',index='1').info['text']
                else:
                    area = '空'
                if d(text='星座').exists:
                    zodiac = d(textContains='座',index=1).info['text']
                else:
                    zodiac = '空'
                d(text='转账').click()
                realname = d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout',index=0).child(className='android.widget.RelativeLayout',index=1).child(className='android.widget.TextView').info['text']




                para = {"sex": "1", "x_01": "a66669ea", "qq_nickname": "qq_nickname", "x_03": "3333a66669ea", "phone": 13234104557}
                con = inventory.postData(para)
                print(con)



        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return AlipayRegister

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()

    args = {"repo_name_id": "102","repo_number_id": "136","time_delay": "3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

