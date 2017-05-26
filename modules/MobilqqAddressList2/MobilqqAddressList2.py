# coding:utf-8
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
from PIL import Image
import colorsys


class MobilqqAddressList2:
    def __init__(self):
        self.repo = Repo()
        self.scode = None

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum


    def Gender(self,d,z):
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






    def Bind(self,d,z):
        circle = 0
        self.scode = smsCode(d.server.adb.device_serial())
        newStart = 1
        while newStart == 1:
            GetBindNumber = self.scode.GetPhoneNumber(self.scode.QQ_CONTACT_BIND)
            print(GetBindNumber)
            z.sleep(2)
            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(GetBindNumber)  #GetBindNumber
            z.heartbeat()
            z.sleep(1)
            d(text='下一步').click()
            z.sleep(3)
            if d(text='下一步').exists:       #操作过于频繁的情况
                return 'false'

            if d(text='确定').exists:     #提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d(text='确定',).click()
            z.heartbeat()
            code = self.scode.GetVertifyCode(GetBindNumber, self.scode.QQ_CONTACT_BIND, '4')
            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(code)
            print(code)
            newStart = 0
            if d(text='请输入短信验证码').exists:
                if circle < 4:
                    z.toast('没有接收到验证码')
                    d(textContains='返回').click()
                    if d(text='确定').exists:
                        d(text='返回').click()
                        z.sleep(1)
                    d(description='删除 按钮').click()
                    circle = circle+1
                    newStart = 1
                    continue
                else:
                    z.toast('程序结束')
                    print(circle)
                    return 'false'
            z.heartbeat()
            d(text='完成', resourceId='com.tencent.mobileqq:id/name').click()
            z.sleep(10)
            if d(textContains='没有可匹配的').exists:
                return 'false'

        return 'true'

    def action(self, d,z, args):
        z.heartbeat()
        gender1 = args['gender']
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(6)
        if not d(text='搜索').exists:
            return 2
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
            d(text='关闭').click()
            z.sleep(1)
        z.heartbeat()
        z.sleep(1)
        if d(textContains='主题装扮').exists:
            d(text='关闭').click()
        d(className='android.widget.TabWidget',resourceId='android:id/tabs').child(className='android.widget.FrameLayout').child(className='android.widget.RelativeLayout').click()     #点击到联系人
        z.sleep(4)

        if d(text='主题装扮').exists:
            d(text='关闭').click()
        if d(text='马上绑定').exists:
            d(text='关闭').click()
        if d(text='通讯录').exists:
            d(text='关闭').click()

        z.heartbeat()

        if not d(text='联系人',resourceId='com.tencent.mobileqq:id/ivTitleName').exists:       #如果没到联系人界面
            d(className='android.widget.TabWidget', resourceId='android:id/tabs').child(
                className='android.widget.FrameLayout').child(className='android.widget.RelativeLayout').click()  # 点击到联系人
        wait = 1
        while wait == 1:
            obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.CheckBox',      #刚进联系人界面看是否有展开的列表
                    checked='true')  # 看是否有展开的
            if obj.exists:
                obj.click()                     #将展开的全部收起来
                continue
            d.swipe(width / 2, height * 4 / 5, width / 2, height / 5)
            z.sleep(2)
            wait = 0
        z.heartbeat()
        z.sleep(1)
        wait1 = 1
        while wait1 == 1:
            obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.CheckBox',
                    checked='true')  # 防止有多列分组，滑动之后再看有没有展开的列表
            z.sleep(2)
            if obj.exists:
                obj.click()
                continue
            wait1 = 0
        z.heartbeat()

        for i in range(11, 1, -1):       #收起通讯录之后，再倒序确定通讯录的位置，点击展开并滑动，未绑定通讯录的,先绑定再发消息
            if d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i).exists:
                d(resourceId='com.tencent.mobileqq:id/elv_buddies', className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i - 1).click()    #点击通讯录
                z.sleep(2)
                if d(resourceId='com.tencent.mobileqq:id/name',className='android.widget.EditText',index=2).exists:       #检查到尚未 启用通讯录
                    if d(text=' +null',resourceId='com.tencent.mobileqq:id/name').exists:
                        d(text=' +null', resourceId='com.tencent.mobileqq:id/name').click()
                        d(text='中国',resourceId='com.tencent.mobileqq:id/name').click()
                    z.heartbeat()
                    text = self.Bind(d,z)                                 #未开启通讯录的，现绑定通讯录
                    z.heartbeat()
                    if text=='false':                          #操作过于频繁的情况
                        return
                    z.sleep(7)
                    if d(resourceId='com.tencent.mobileqq:id/nickname',className='android.widget.TextView').exists:      #通讯录展开后在另一个页面的情况
                        d(text='返回',resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft').click()
                    z.sleep(7)
                    d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i - 1).click()

                if d(text='匹配手机通讯录').exists:
                    d(text='匹配手机通讯录').click()
                    z.heartbeat()
                    while not d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i - 1).exists:
                        z.sleep(2)
                        if d(textContains='下线通知').exists:
                            return
                    d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i - 1).click()
                z.heartbeat()
                z.sleep(1)
                if d(text='启用').exists:
                    d(text='启用').click()
                    z.sleep(6)
                    d(text='返回').click()
                    obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.CheckBox',
                            # 刚进联系人界面看是否有展开的列表
                            checked='true')  # 看是否有展开的
                    if obj.exists:
                        obj.click()
                    d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i - 1).click()

                clickCondition = d(className='android.widget.AbsListView')
                obj = clickCondition.info
                obj = obj['visibleBounds']
                top = int(obj['top'])
                clickCondition = d(className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i - 1).info['visibleBounds']
                top1 = int(clickCondition['top'])
                y = top1 - top
                d.swipe(width / 2, y, width / 2, 0)
                z.sleep(2)
                z.heartbeat()
                break
            else:
                continue           #直到找到通讯录为止

        z.heartbeat()
        set1 = set()
        change = 0
        i = 1
        t = 1
        EndIndex = int(args['EndIndex'])
        while t < EndIndex+1:
            obj = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i).child(
                resourceId='com.tencent.mobileqq:id/text1',index=1,className='android.view.View')  # 点击第ｉ个人

            time.sleep(0.5)

            if obj.exists:
                # print(i)
                z.heartbeat()
                change = 1
                z.sleep(1)
                obj.click()
                if not d(descriptionContains='昵称:').exists:
                    i = 3
                    continue
                phone = d(descriptionContains='昵称:').info
                phone = phone['text']      #得到电话号码，并保存到set集合中成为唯一标识
                if phone in set1:
                    d(textContains='返回').click()
                    i = i+1
                    continue
                else:
                    set1.add(phone)
                    print(phone)
                z.heartbeat()
                if gender1 != '不限':
                    gender2 = self.Gender(d,z)
                    z.heartbeat()
                    if gender1==gender2:        #gender1是外界设定的，gender2是读取到的
                        z.sleep(1)
                    else:
                        d(textContains='返回').click()
                        i = i+1
                        continue
            else:
                if change ==0:        #第一次滑动，开始ｉｎｄｅｘ不是通讯录里的人的时候，当点击开始发消息时将该值变为１
                    i = i + 1
                    if i>13:     #已绑定通讯录但通讯录一个人都没有时的结束条件
                        return
                    continue
                else:
                    obj = d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i).child(
                        className='android.widget.CheckBox')
                    if obj.exists:
                        return

                    d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                    z.sleep(2)
                    i = 2
                    continue
            z.heartbeat()
            d(text='发消息').click()
            z.sleep(1)
            d(className='android.widget.RelativeLayout').child(className='android.widget.LinearLayout',index=5).child(className='android.widget.ImageView',index=1).click()
            picnum = int(args['picnum'])
            countpic = 0
            ff = 0
            mm = 0
            while countpic < picnum:
                picclick = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=ff).child(className='android.widget.CheckBox')
                if picclick.exists:
                    if d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=ff).child(className='android.widget.CheckBox', checked='true').exists:
                        ff = ff + 1
                        continue
                    mm = 1
                    picclick.click()
                    countpic = countpic + 1
                    ff = ff + 1

                else:
                    if mm == 0:
                        z.sleep(2)
                        break

                    clickCondition = d(className='android.widget.RelativeLayout', index=1).child(className='android.widget.AbsListView', index=0).info['visibleBounds']
                    top = int(clickCondition['top'])
                    bottom = int(clickCondition['bottom'])
                    y = int((bottom - top) / 2)
                    y = y + top
                    x = int(clickCondition['right']) - 1
                    d.swipe(x, y, 0, y)
                    mm = 0
                    ff = 0

            z.heartbeat()
            z.sleep(1)
            d(resourceId='com.tencent.mobileqq:id/send_btn').click()
            while d(textContains='正在处理').exists:
                z.sleep(2)
            z.sleep(2)
            saveid = args['repo_cate_id']
            self.repo.uploadPhoneNumber(phone,saveid)
            i = i + 1
            t = t + 1
            d(resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft', description='返回消息界面').click()

            d(className='android.widget.TabWidget', resourceId='android:id/tabs').child(
                className='android.widget.FrameLayout').child(
                className='android.widget.RelativeLayout').click()  # 发完消息后点击到联系人
            z.heartbeat()
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqAddressList2

if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("3018768")
    z = ZDevice("3018768")
    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").communicate()

    args = {"picnum":"2","repo_cate_id":"144",'gender':"不限",'EndIndex':'20',"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)
