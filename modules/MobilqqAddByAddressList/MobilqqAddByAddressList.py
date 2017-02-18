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

class MobilqqAddByAddressList:
    def __init__(self):
        self.repo = Repo()
        self.xuma = XunMa()

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






    def Bind(self,d):
        newStart = 1
        while newStart == 1:
            GetBindNumber = self.xuma.GetPhoneNumber('2113')
            print(GetBindNumber)
            time.sleep(2)
            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(GetBindNumber)  #GetBindNumber

            time.sleep(1)
            d(text='下一步').click()
            time.sleep(3)
            if d(text='下一步',resourceId='com.tencent.mobileqq:id/name',index=2).exists:       #操作过于频繁的情况
                return 'false'

            if d(text='确定', resourceId='com.tencent.mobileqq:id/name', index='2').exists:     #提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d(text='确定', resourceId='com.tencent.mobileqq:id/name', index='2').click()

            code = self.xuma.GetVertifyCode(GetBindNumber, '2113','4')

            newStart = 0



            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(code)
            d(text='完成', resourceId='com.tencent.mobileqq:id/name').click()

        return 'true'



    def action(self, d,z, args):
        gender1 = args['gender']

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(6)
        if d(text='消息',resourceId='com.tencent.mobileqq:id/name').exists:                    #到了通讯录这步后看号有没有被冻结
            print
        else:
            return 2
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
            d(text='关闭').click()
            time.sleep(1)

        d(className='android.widget.TabWidget',resourceId='android:id/tabs').child(className='android.widget.FrameLayout').child(className='android.widget.RelativeLayout').click()     #点击到联系人
        time.sleep(4)

        if d(text='主题装扮').exists:
            d(text='关闭').click()
        if d(text='马上绑定').exists:
            d(text='关闭').click()
        if d(text='通讯录').exists:
            d(text='关闭').click()



        if d(text='联系人',resourceId='com.tencent.mobileqq:id/ivTitleName').exists:       #如果已经到联系人界面
            print
        else:
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
            time.sleep(2)
            wait = 0

        time.sleep(1)
        wait1 = 1
        while wait1 == 1:
            obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.CheckBox',
                    checked='true')  # 防止有多列分组，滑动之后再看有没有展开的列表
            time.sleep(2)
            if obj.exists:
                obj.click()
                continue
            wait1 = 0

        for i in range(11, 1, -1):       #收起通讯录之后，再倒序确定通讯录的位置，点击展开并滑动，未绑定通讯录的,先绑定再发消息
            if d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i).exists:
                d(resourceId='com.tencent.mobileqq:id/elv_buddies', className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i - 1).click()    #点击通讯录
                time.sleep(2)
                if d(resourceId='com.tencent.mobileqq:id/name',className='android.widget.EditText',index=2).exists:       #检查到尚未 启用通讯录
                    if d(text=' +null',resourceId='com.tencent.mobileqq:id/name').exists:
                        d(text=' +null', resourceId='com.tencent.mobileqq:id/name').click()
                        d(text='中国',resourceId='com.tencent.mobileqq:id/name').click()
                    text = self.Bind(d)                                 #未开启通讯录的，现绑定通讯录
                    if text=='false':                          #操作过于频繁的情况
                        return
                    time.sleep(7)
                    if d(resourceId='com.tencent.mobileqq:id/nickname',className='android.widget.TextView').exists:      #通讯录展开后在另一个页面的情况
                        d(text='返回').click()
                    time.sleep(7)
                    d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i - 1).click()

                if d(text='匹配手机通讯录',resourceId='com.tencent.mobileqq:id/name').exists:
                    d(text='匹配手机通讯录', resourceId='com.tencent.mobileqq:id/name').click()
                    time.sleep(10)
                    d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i - 1).click()
                time.sleep(1)
                if d(text='启用').exists:
                    d(text='启用').click()
                    time.sleep(6)
                    d(text='返回').click()
                    obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.CheckBox',
                            # 刚进联系人界面看是否有展开的列表
                            checked='true')  # 看是否有展开的
                    if obj.exists:
                        obj.click()
                    d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i - 1).click()
                d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                time.sleep(2)
                break
            else:
                continue           #直到找到通讯录为止

        set1 = set()
        change = 0
        i = 1
        t = 1
        EndIndex = int(args['EndIndex'])
        while t < EndIndex+1:
            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)

            try:
                Material = Material[0]['content']  # 从素材库取出的要发的材料
                wait = 0
            except Exception:
                d.server.adb.cmd("shell","am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()

            time.sleep(1)

            obj = d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i).child(
                resourceId='com.tencent.mobileqq:id/text1', index=1)  # 点击第ｉ个人
            print(i)
            time.sleep(0.5)
            if obj.exists:
                change = 1
                obj.click()
                if d(descriptionContains='昵称:').exists:
                    print
                else:
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
                if gender1 != '不限':
                    gender2 = self.Gender(d)
                    if gender1==gender2:        #gender1是外界设定的，gender2是读取到的
                        time.sleep(1)
                    else:
                        d(textContains='返回').click()
                        i = i+1
                        continue
            else:
                if change ==0:        #第一次滑动，开始ｉｎｄｅｘ不是通讯录里的人的时候，当点击开始发消息时将该值变为１
                    i = i + 1
                    continue
                else:
                    obj = d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i).child(
                        className='android.widget.CheckBox')
                    if obj.exists:
                        return
                    d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                    time.sleep(3)
                    i = 2
                    continue

            if '[姓名]' in Material:
                obj1 = d(descriptionContains='QQ 昵称').child(className='android.widget.TextView', index=1).info
                obj1 = obj1['text']
                Material = Material.replace('[姓名]',obj1)  # -----------------------------------
                print(Material)

            d(text='加好友').click()
            if d(textContains='问题').exists:
                d(text='取消').click()
                d(text='返回').click()
                i = i+1
                continue
            obj = d(className='android.widget.EditText', index=1).info  # 将之前消息框的内容删除
            obj = obj['text']
            lenth = len(obj)
            delet = 0
            while delet < lenth:
                d.press.delete()
                delet = delet + 1
            z.input(Material)
            time.sleep(1)
            # d(text='发送').click()
            d(text='取消').click()
            i = i + 1
            t = t + 1
            d(text='返回').click()

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqAddByAddressList

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id":"100",'gender':"不限",'EndIndex':'50',"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)