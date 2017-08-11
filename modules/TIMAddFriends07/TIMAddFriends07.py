# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
from PIL import Image
import colorsys
# from RClient import *


class TIMAddFriends07:
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

            if None == dominant_color:
                return '不限'
            red = dominant_color[0]
            blue = dominant_color[2]

            if red > blue:
                return '女'
            else:
                return '男'
        else:                          #没有基本资料的情况
            return '不限'

    def action(self, d, z, args):

        gender = args['gender']
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(5)
        d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=1).child(
            className='android.widget.FrameLayout', index=1).click()  # 点击到联系人
        # time.sleep(3)
        # if d(text='联系人', resourceId='com.tencent.tim:id/ivTitleName').exists:  # 如果已经到联系人界面
        #     # obj = d(className='android.widget.AbsListView', index=1).child(index=8,resourceId='com.tencent.tim:id/group_item_layout').child(
        #     #     checked='false', resourceId='com.tencent.tim:id/name')
        #     # d(text="添加",resourceId="com.tencent.tim:id/ivTitleBtnRightText").click()
        #
        #     # if obj.exists:
        #     #     time.sleep(2)
        #     #     d(resourceId='com.tencent.tim:id/group_item_layout', index=8).click()  # 未展开的情况，先点击展开
        #     #     time.sleep(1)
        #     #     d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
        #     # else:
        #     #     d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
        # else:  # 没有在联系人界面的话
        #     d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=1).child(
        #         className='android.widget.FrameLayout', index=1).click()  # 点击到联系人
        #     obj = d(className='android.widget.AbsListView', index=1).child(index=8,resourceId='com.tencent.tim:id/group_item_layout').child(
        #         checked='false', resourceId='com.tencent.tim:id/name')
        #     if obj.exists:
        #         d(resourceId='com.tencent.tim:id/group_item_layout', index=8).click()  # 未展开的情况，先点击展开
        #         d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
        #     else:
        #         d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
        while True:                          #由于网速慢或手机卡可能误点
            if d( index=1, className='android.widget.ImageView' ).exists:
                z.heartbeat( )
                d( index=1, className="android.widget.FrameLayout" ).child( index=0,className="android.widget.RelativeLayout" ).click( )
            if d(text="加好友").exists:    #由于网速慢或手机卡可能误点
                d(text="加好友").click()
                d(text="返回",className="android.widget.TextView").click()
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,className="android.widget.RelativeLayout" ).click( )
            z.sleep( 2 )
            # if  d(textContains="通讯录").exists:
            if d(text="添加",resourceId="com.tencent.tim:id/ivTitleBtnRightText").exists:
                z.heartbeat( )
                d( text="添加", resourceId="com.tencent.tim:id/ivTitleBtnRightText" ).click( )
                break
        i = 2
        t = 1
        d(index=0,text="添加手机联系人").click()
        EndIndex = int(args['EndIndex'])
        while t < EndIndex + 1:
            cate_id = args["repo_material_id"]
            time.sleep(2)

            obj = d(index=0,resourceId='com.tencent.tim:id/name', className='android.widget.AbsListView').child(
                className="android.widget.LinearLayout", index=i).child(text="添加",index=2)
            if obj.exists:
                obj.click()
                time.sleep(2)
            else:
                i = i + 1
                continue

            if gender != '不限':
                gender2 = self.Gender(d)
                if gender == gender2:               # gender是外界设定的，gender2是读取到的
                    time.sleep(1)
                else:
                    d(textContains='返回').click()
                    i = i + 1
                    continue
            if obj.exists:
                return
            if d(text='加好友',className='android.widget.Button').exists:
                d(text='加好友',className='android.widget.Button').click()
            time.sleep(2)
            material = self.repo.GetMaterial(cate_id, 0, 1)
            material = material[0]['content']  # 从素材库取出的要发的材料
            z.sleep( 2 )
            z.heartbeat( )
            if d( text='加好友', className="android.widget.Button" ).exists:  # 拒绝被添加的轻况
                continue
            if d( text='必填', resourceId='com.tencent.tim:id/name' ).exists:  # 要回答问题的情况
                z.heartbeat( )
                continue
            d.dump( compressed=False )
            if d( text="风险提示" ).exists:  # 风险提示
                z.heartbeat( )
                continue
            obj = d( text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText' )  # 不需要验证可直接添加为好友的情况
            if obj.exists:
                z.sleep( 2 )
                obj.click( )
                if d( text='添加失败，请勿频繁操作', resourceId='com.tencent.tim:id/name' ).exists:
                    z.heartbeat( )
                    z.toast( "频繁操作,跳出模块" )
                    return
                else:
                    print(  "请求发送成功" )
                continue
            d.dump( compressed=False )
            obj = d( index=3, className='android.widget.EditText',
                     resourceId='com.tencent.tim:id/name' ).info  # 将之前消息框的内容删除        需要发送验证信息
            obj = obj['text']
            lenth = len( obj )
            t = 0
            while t < lenth:
                d.press.delete( )
                t = t + 1
            time.sleep( 2 )
            z.input( material )
            # d(index=2,className="android.widget.CompoundButton",resourceId="com.tencent.tim:id/name").click()
            # if "是" in switch_card:
            #     if d( index=2, className="android.widget.CompoundButton", resourceId="com.tencent.tim:id/name" ).exists:
            #         d( index=2, className="android.widget.CompoundButton",
            #            resourceId="com.tencent.tim:id/name" ).click( )
            d( text='下一步', resourceId='com.tencent.tim:id/ivTitleBtnRightText' ).click( )
            z.sleep( 1 )
            d( text='发送' ).click( )
            if d( resourceId='com.tencent.tim:id/name', text='添加失败，请勿频繁操作' ).exists:  # 操作过于频繁的情况
                z.toast( "频繁操作,跳出模块" )
                return
            # print( QQnumber + "请求发送成功" )
            z.heartbeat( )
            # count = count + 1
            # if count == add_count:
            #     break

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMAddFriends07


if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id": "40", 'gender':"不限", "time_delay": "3", "EndIndex": "8"};  # cate_id是仓库号，length是数量
    o.action(d, z, args)