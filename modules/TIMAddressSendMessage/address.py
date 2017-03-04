# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
from PIL import Image
import colorsys
from RClient import *
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class TIMAddressAddFriends:
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

class TIMAddressSendMessage:

    def __init__(self):
        self.repo = Repo()

    def action(self, d, z,args):
        gender = args['gender']
        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来

        while 1:
            if d(text='消息',className='android.widget.TextView').exists:
                d(className='android.widget.TabWidget', index=1).child(className='android.widget.FrameLayout',index=1).click()  # 点击到联系人
                time.sleep(1)
                break
            else:
                time.sleep(1)

        info = d(index=1, className='android.widget.AbsListView').info
        bHeight = info["visibleBounds"]["bottom"] - info["visibleBounds"]["top"]
        # bWidth = info["visibleBounds"]["right"] - info["visibleBounds"]["left"]
        bTop = info["visibleBounds"]["top"]
        count = d(index=1, className='android.widget.AbsListView').info['childCount']
        bHeight = bHeight*(count-1)/count

        obj =d(className='android.widget.AbsListView', index=1).child(index=8,resourceId='com.tencent.tim:id/group_item_layout').child(checked='false',resourceId='com.tencent.tim:id/name')
        tInfo = d(index=8,resourceId='com.tencent.tim:id/group_item_layout').info
        tHeight = tInfo["visibleBounds"]["top"]
        tHeight = tHeight-bTop

        if obj.exists:
            time.sleep(2)
            d(resourceId='com.tencent.tim:id/group_item_layout', index=8).click()  # 未展开的情况，先点击展开
            time.sleep(1)
            d.swipe(0, tHeight+25, 0, 0)                         #30像素是表(tableView)中组(goup)与组的间隔,可以优化
        else:
            d.swipe(0, tHeight+25, 0, 0)
            print '通讯录已经被点'

        numberArr = []
        judge = True
        r = 0
        while judge==True:

            if judge == False:
                break
            for i in range(1, count-1):
                d(index=1, className='android.widget.AbsListView').child(index=1,
                                                                         className='android.widget.RelativeLayout').click()
                d(text='返回', className='android.widget.TextView').click()
                d.swipe(0, 86 * 7, 0, 0)
                r = r + 1
                print r
                # obj = d(index=1, className='android.widget.AbsListView').child(index=i,className='android.widget.RelativeLayout')
                # if obj.exists:
                #     obj.click()
                #
                #     number = d(index=0, className='android.widget.TextView', descriptionContains='昵称').info["text"]
                #     d(text='返回', className='android.widget.TextView').click()
                #     if number.isdigit():
                #         if number not in numberArr:
                #             numberArr.append(number)
                #     else:
                #         judge = False
                #         break
                #
                #     if count == i + 2:
                #         d.swipe(0, 86*7, 0, 0)
                #         r = r+1
                #         print r



        print numberArr
        ok='ok'
                #     if obj in numberArr:
                #         ok='ok'
                #     else:
                #         if obj.isdigit():
                #             numberArr.append(obj)
                #
                #     if count == i + 1:
                #         d.swipe(bWidth / 2, bHeight, bWidth / 2, 0)
                #         nstr = d(index=0, className='android.widget.AbsListView').child(index=i,className='android.widget.LinearLayout').info["contentDescription"]
                #         if nstr == numberArr[-1]:
                #             judge = 'False'
                #             break
                #
                # else:
                #     if i==0:
                #         continue
                #     else:
                #         judge = 'False'
                #         break


        i = 1
        t = 1
        EndIndex = int(args['EndIndex'])

        while t < EndIndex+1:
            cate_id = args["repo_material_id"]
            message = self.repo.GetMaterial(cate_id, 0, 1)
            message = message[0]['content']  # 从素材库取出的要发的材料
            if len(message)==0:
                return
            time.sleep(1)
            obj = d(resourceId='com.tencent.tim:id/elv_buddies', className='android.widget.AbsListView').child(resourceId='com.tencent.tim:id/group_item_layout',index=10)
            if obj.exists and i ==10:      #通讯录好友已经到底的情况
                return
            if i > 11:
                return
            obj = d(resourceId='com.tencent.tim:id/elv_buddies', className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=i).child(resourceId='com.tencent.tim:id/text1',index=1)  # 点击第ｉ个人
            if obj.exists:
                obj.click()
                time.sleep(1)
            else:
                i = i+1
                continue

            if gender != '不限':
                gender2 = self.Gender(d)
                if gender == gender2:  # gender是外界设定的，gender2是读取到的
                    time.sleep(1)
                else:
                    d(textContains='返回').click()
                    i = i + 1
                    continue
            d(resourceId='com.tencent.tim:id/txt', text='发消息').click()
            time.sleep(2)
            d(resourceId='com.tencent.tim:id/input', className='android.widget.EditText').click()  # Material
            z.input(message)
            time.sleep(1)
            d(resourceId='com.tencent.tim:id/fun_btn', text='发送').click()
            i = i+1
            t = t+1
            d(resourceId='com.tencent.tim:id/ivTitleBtnLeft', description='返回消息界面').click()
            d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=1).child(className='android.widget.FrameLayout', index=1).click()  # 点击到联系人
            continue
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMAddressSendMessage

if __name__ == "__main__":

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT52DSK00474")
    z = ZDevice("HT52DSK00474")

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id":"39", 'gender':"不限","time_delay":"3","EndIndex":"50"};    #cate_id是仓库号，length是数量
    o.action(d,z,args)
