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


class MobilqqAddressList:
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

    def Gender(self,d):
        co = RClient()
        im_id = ""
        co.rk_report_error(im_id)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.TextView',descriptionContains='基本信息')  # 当弹出选择QQ框的时候，定位不到验证码图片
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
            # show(region)    #展示资料卡上的信息
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
                z.heartbeat()
                score = (saturation + 0.1) * count
                if score > max_score:
                    max_score = score
                    dominant_color = (r, g, b)
            # print("---------------------------------------------------------------------------")
            # print(dominant_color)
            z.heartbeat()
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






    def Bind(self,d):
        self.xuma = XunMa(d.server.adb.device_serial())
        newStart = 1
        while newStart == 1:
            GetBindNumber = self.xuma.GetPhoneNumber('2113')
            print(GetBindNumber)
            time.sleep(2)
            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(GetBindNumber)  #GetBindNumber
            z.heartbeat()
            time.sleep(1)
            d(text='下一步').click()
            time.sleep(3)
            if d(textContains='中国').exists:       #操作过于频繁的情况
                return 'false'

            if d(text='确定').exists:     #提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d(text='确定',).click()
                time.sleep(1)
                if d(text='确定').exists:
                    z.toast('请求失败，结束程序')
                    return 'false'
            z.heartbeat()
            code = self.xuma.GetVertifyCode(GetBindNumber, '2113','4')

            newStart = 0

            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(code)
            z.heartbeat()
            d(text='下一步').click()
            time.sleep(6)
            if d(textContains='访问你的通讯录').exists:
                d(text='好').click()
                time.sleep(5)

            if d(textContains='没有可匹配的').exists:
                return 'false'
            if d(textContains='验证短信').exists:    #验证码错误的情况
                return 'false'

            if d(text='匹配手机通讯录').exists:
                d(text='匹配手机通讯录').click()
                z.heartbeat()

        return 'true'

    def action(self, d,z, args):
        z.heartbeat()
        gender = args['gender']
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(6)
        if not d(text='搜索').exists:                    #到了通讯录这步后看号有没有被冻结
            return 2
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
            d(text='关闭').click()
            time.sleep(1)
        z.heartbeat()
        d(className='android.widget.TabWidget').child(className='android.widget.RelativeLayout',index=1).child(className='android.widget.ImageView',index=2).click()     #点击到联系人
        time.sleep(1)
        z.heartbeat()
        closecheck = d(className='android.view.View').child(className='android.widget.RelativeLayout',index=3).child(checked='true')
        if closecheck.exists:
            closecheck.click()
        closecheck = d(className='android.view.View').child(className='android.widget.RelativeLayout', index=4).child(checked='true')   #通讯录展开的情况，如果没匹配
        if not closecheck.exists:     #在通讯录好友没展开的情况，点击展开
            closecheck.click()
        if d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText',index=2).exists:  # 检查到尚未 启用通讯录,有输入框的情况
            if d(text=' +null', resourceId='com.tencent.mobileqq:id/name').exists:
                d(text=' +null', resourceId='com.tencent.mobileqq:id/name').click()
                d(text='中国', resourceId='com.tencent.mobileqq:id/name').click()
            z.heartbeat()
            text = self.Bind(d)  # 未开启通讯录的，现绑定通讯录
            z.heartbeat()
            if text == 'false':  # 操作过于频繁的情况
                return
            time.sleep(7)   #------------------------------
        if d(text='匹配手机通讯录').exists:
            d(text='匹配手机通讯录').click()
        if d(textContains='下线通知').exists:
            return
        if d(text='启用').exists:
            d(text='启用').click()
            time.sleep(6)
            d(text='返回').click()
        z.heartbeat()


        set1 = set()
        change = 0
        i = 5
        t = 1
        EndIndex = int(args['EndIndex'])
        while t < EndIndex+1:
            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                time.sleep(10)
                return
            message = Material[0]['content']  # 取出验证消息的内容
            forclick = d(className='android.widget.FrameLayout',index=i)
            if forclick.exists:
                forclick.click()
                phone = d(className='android.widget.RelativeLayout', index=1).child(className='android.widget.LinearLayout',index=1).child(className='android.widget.TextView').info['text']
                if phone in set1:
                    i = i+1
                    continue
                set1.add(phone)
                if gender!='不限':
                    getgender = d(className='android.widget.RelativeLayout', index=1).child(className='android.widget.TextView',index=2)
                    if getgender.exists:
                        getgender = getgender.info['text']
                        if getgender!=gender:
                            i = i+1
                            d(text='返回').click()
                            continue
                    else:
                        i = i+1
                        d(text='返回').click()
                        continue
                d(text='发消息').click()








            if '[姓名]' in message:
                obj1 = d(descriptionContains='QQ 昵称').child(className='android.widget.TextView', index=1).info
                obj1 = obj1['text']
                message = message.replace('[姓名]',obj1)  # -----------------------------------
            d(resourceId='com.tencent.mobileqq:id/txt', text='发消息').click()
            time.sleep(1)
            z.input(message)
            z.heartbeat()
            time.sleep(1)
            d(text='发送').click()
            i = i + 1
            t = t + 1
            d(resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft', description='返回消息界面').click()

            d(className='android.widget.TabWidget', resourceId='android:id/tabs').child(
                className='android.widget.FrameLayout').child(
                className='android.widget.RelativeLayout').click()  # 发完消息后点击到联系人
            z.heartbeat()
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqAddressList

if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("8HVSMZKBEQFIBQUW")
    z = ZDevice("8HVSMZKBEQFIBQUW")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()


    args = {"repo_material_id":"39",'gender':"不限",'EndIndex':'20',"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)
