# coding:utf-8
from smsCode import smsCode
from uiautomator import Device
from Repo import *
from Inventory import *
import os, time, datetime, random
from zservice import ZDevice
from PIL import Image
import colorsys



class TIMCollectData16:

    def __init__(self):
        self.repo = Repo()
        self.inventory = Inventory()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def Bind(self, d,z):
        self.scode = smsCode(d.server.adb.device_serial())
        newStart = 1
        while newStart == 1:
            GetBindNumber = self.scode.GetPhoneNumber(self.scode.QQ_CONTACT_BIND)
            print(GetBindNumber)
            z.sleep(2)
            d(text='请输入你的手机号码', className='android.widget.EditText').set_text(
                GetBindNumber)  # GetBindNumber
            z.heartbeat()
            z.sleep(1)
            d(text='下一步').click()
            z.sleep(3)
            if d(text='下一步', resourceId='com.tencent.mobileqq:id/name', index=2).exists:  # 操作过于频繁的情况
                return 'false'

            if d(text='确定', resourceId='com.tencent.mobileqq:id/name',
                 index='2').exists:  # 提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d(text='确定', resourceId='com.tencent.mobileqq:id/name', index='2').click()

            code = self.scode.GetVertifyCode(GetBindNumber, self.scode.QQ_CONTACT_BIND, '4')
            newStart = 0

            d(text='请输入验证码', className='android.widget.EditText').set_text(code)
            z.heartbeat()
            d(text='完成', resourceId='com.tencent.mobileqq:id/name').click()
            z.sleep(5)
            if d(text='确定').exists:
                d(text='确定').click()

            if d(textContains='没有可匹配的').exists:
                return 'false'

        return 'true'

    def Gender(self,d):

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

            if None ==dominant_color:
                return '不限'
            red = dominant_color[0]
            blue = dominant_color[2]

            if red > blue:
                return '女'
            else:
                return '男'
        else:                          #没有基本资料的情况
            return '不限'


    def scrollCell(self, d):
        while d(text='正在发送请求', className='android.widget.TextView').exists:
            time.sleep(2)

        if d(text='启用').exists:
            d(text='启用').click()

        if d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText',index=2).exists:  # 检查到尚未 启用通讯录
            if d(text=' +null', resourceId='com.tencent.mobileqq:id/name').exists:
                d(text=' +null', resourceId='com.tencent.mobileqq:id/name').click()
                d(text='中国大陆', resourceId='com.tencent.mobileqq:id/name').click()

        text = self.Bind( d, z )  # 未开启通讯录的，现绑定通讯录

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
                        if number != '':
                            obj.click()
                            d(index=3, className='android.widget.ImageView').click()

                            phoneNumberStr = d( resourceId='com.tencent.tim:id/info', index=1 ).info['text']
                            phoneNumber = phoneNumberStr[3:len(phoneNumberStr)]
                            numberArr.append(phoneNumber)

                            ageAndarea = d(className='android.widget.LinearLayout', index=6 ).child(
                                resourceId='com.tencent.tim:id/name', className='android.widget.TextView',
                                index=0)

                            age = ''
                            area = ''
                            gender = ''
                            if ageAndarea.exists:
                                ageAndareaInfo = ageAndarea.info['text']
                                age = ageAndareaInfo[1:4]
                                area = ageAndareaInfo[5:len(ageAndareaInfo)]
                                gender = self.Gender(d)

                            para = {"phoneNumber": phoneNumber, 'x_01': gender, 'x_02': age, 'x_03': area}

                            self.repo.PostInformation(args['repo_cate_id'], para)

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


    def action(self, d, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(3)

        d(description='快捷入口', className='android.widget.ImageView').click()
        d(text = '加好友', className = 'android.widget.TextView').click()
        d(text='添加手机联系人', className='android.widget.TextView').click()
        time.sleep(2)

        self.scrollCell(d)

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMCollectData16

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("25424f9")
    z = ZDevice("25424f9")

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_cate_id":"349", "time_delay":"3"};    #cate_id是仓库号，length是数量
    # o.action(d, args)
    if d(text='验证手机号码').exists:  # 检查到尚未 启用通讯录
        if d( text=' +null').exists:
            d( text=' +null').click( )
            d( text='中国').click( )
    o.Bind( d, z )  # 未开启通讯录的，现绑定通讯录