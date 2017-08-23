# coding:utf-8
from PIL.ImageShow import show
from uiautomator import Device
from Repo import *
import os, datetime, string, random
from zservice import ZDevice
import sys
from PIL import Image
import colorsys
from Inventory import *

class AlipayDepost:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def Gender(self,d,obj):

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

                score = (saturation + 0.1) * count
                if score > max_score:
                    max_score = score
                    dominant_color = (r, g, b)    #红绿蓝
            # print("---------------------------------------------------------------------------")
            # print(dominant_color)
            return dominant_color


    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.eg.android.AlipayGphone").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin").communicate()  # 拉起来
        z.sleep(10)

        accountStatus = "正常"

        d(description='通讯录').click()
        if d(text='转到银行卡').exists:
            d(description ='返回').click()
            d(description='通讯录').click()

        d(text='新的朋友').click()
        d(text='添加手机联系人').click()


        publicpath = d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=2) \
            .child(className='android.widget.LinearLayout', index=0).child(
            className='android.widget.LinearLayout', index=0)  # 为下面的点击做准备

        times = 3
        while d(textContains='没有联系人').exists:
            z.heartbeat()
            d(description='返回').click()
            z.sleep(int(args["contact_wait"]))
            d(text='添加手机联系人').click()
            times = times - 1
            if times < 0:
                z.toast("手机通讯录里没有联系人")
                return

        z.heartbeat()
        i = 0
        set1 = set()
        change = 0
        while True:
            judexist = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=i)\
                .child(className='android.widget.LinearLayout').child(className='android.widget.TextView',index=0)
            if judexist.exists:
                z.heartbeat()
                change = 1
                phoneNumber = judexist.info['text']#要保存的电话号码
                if phoneNumber in set1:
                    i = i+1
                    continue
                set1.add(phoneNumber)
                # print(phoneNumber)
                judexist.click()        #点击第i个人
                z.sleep(1.5)

                accountCount = "一对一"
                if d(textContains='该手机号对应多个支付宝账户，请核实后选择').exists:
                    d(resourceId='com.alipay.mobile.contactsapp:id/head_icon').click()
                    accountCount = '一对多'

                path = d(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=0).child(className='android.widget.ImageView',index=2)
                getinfo = self.Gender(d, path)
                if getinfo == None:
                    rank = '非会员'
                    # print('不是会员')
                elif getinfo[2] > 200:  # (68, 164, 238)蓝色大众会员  (140, 142, 185)黑色砖石会员  (255, 197, 30)黄金会员
                    rank = '大众会员'
                elif getinfo[0] > 200:
                    rank = '黄金会员'
                else:
                    rank = '钻石会员'
                # print('=====================================%s==================================================='%rank)
                if d(className='android.widget.ListView').child(className='android.widget.FrameLayout').child(className='android.widget.TextView',index=0).exists:
                    nickname = d(className='android.widget.ListView').child(className='android.widget.FrameLayout').child(className='android.widget.TextView',index=0).info['text']   #要保存的昵称
                else:
                    nickname = '空'
                # print('=============================%s=============================================================='%nickname)

                z.heartbeat()
                if d(text='支付宝账户').exists:
                    for t in range(0, 14):
                        if publicpath.child(className='android.widget.LinearLayout', index=t).child(text='支付宝账户').exists:
                            break
                    account = publicpath.child(className='android.widget.LinearLayout', index=t).child(className='android.widget.TextView',
                                                                                   index=1).info['text']
                else:
                    account = '空'
                z.heartbeat()

                # print('================================%s============================================================='%account)

                if d(text='真实姓名').exists:
                    path = publicpath.child(className='android.widget.LinearLayout', index=1).child(
                        className='android.widget.TextView', index='1')
                    getinfo = self.Gender(d,path)
                    if getinfo[0]>200:
                        gender = '女'           #要保存的性别和是否认证
                        identity = '已实名'
                    elif getinfo[2]>200:
                        gender = '男'
                        identity = '已实名'
                    else:
                        gender = '无'
                        identity = '未实名'
                # print('==========================%s==============%s======================================================'%(gender,identity))

                if identity=='已实名':
                    d(text='转账').click()
                    if d(textContains='对方账户存在异常').exists:
                        accountStatus = "异常"
                        d(text='确定').click()
                    else:
                        realnameStr = \
                            d( className='android.widget.ScrollView' ).child( className='android.widget.LinearLayout',
                                                                              index=0 ).child(
                                className='android.widget.RelativeLayout', index=1 ).child(
                                className='android.widget.TextView' ).info['text']

                        a = realnameStr.find( '（' )
                        b = realnameStr.find( '）' )
                        realname = realnameStr[a + 2:b]
                        # realname = d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout',index=0).child(className='android.widget.RelativeLayout',index=1).child(className='android.widget.TextView').info['text']
                        if d(textContains='对方长时间未使用支付宝').exists:
                            accountStatus = "非常用"
                        else:
                            accountStatus = "常用"

                        d(description='返回').click()
                else:
                    realname = '无'
                # print('=========================%s====================================================================='%realname)


                if d(text='显示更多').exists:
                    d(text='显示更多').click()
                    z.sleep(1)
                    if not d(text='收起').exists:
                        d.swipe(width / 2, height * 3 / 4, width / 2, height / 3)

                z.heartbeat()
                if d(text='地区').exists:
                    area = publicpath.child(className='android.widget.LinearLayout',index=2).child(className='android.widget.TextView',index='1').info['text']
                else:
                    area = '空'
                # print('=========================%s====================================================================='%area)

                if d(text='星座').exists:    #星座
                    zodiac = d(textContains='座',index=1).info['text']
                else:
                    zodiac = '空'

                # print('=============================%s================================================================='%zodiac)


                if d(text='年龄').exists:
                    for t in range(1, 14):
                        if publicpath.child(className='android.widget.LinearLayout', index=t).child(text='年龄').exists:
                            break
                    age = publicpath.child(className='android.widget.LinearLayout', index=t).child(className='android.widget.TextView',
                                                                                   index=1).info['text']
                else:
                    age = '空'
                # print('=================================%s============================================================='%age)

                if d(text='身高').exists:
                    for t in range(1, 14):
                        if publicpath.child(className='android.widget.LinearLayout', index=t).child(text='身高').exists:
                            break
                    tall = publicpath.child(className='android.widget.LinearLayout', index=t).child(className='android.widget.TextView',
                                                                                   index=1).info['text']
                else:
                    tall = '空'
                # print('==========================%s===================================================================='%tall)

                if d(text='体重').exists:
                    for t in range(1, 14):
                        if publicpath.child(className='android.widget.LinearLayout', index=t).child(text='体重').exists:
                            break
                    weight = publicpath.child(className='android.widget.LinearLayout', index=t).child(className='android.widget.TextView',
                                                                                   index=1).info['text']
                else:
                    weight = '空'
                # print('=============================%s================================================================='%weight)
                z.heartbeat()
                if d(text='职业').exists:
                    for t in range(1, 14):
                        if publicpath.child(className='android.widget.LinearLayout', index=t).child(text='职业').exists:
                            break
                    carrer = publicpath.child(className='android.widget.LinearLayout', index=t).child(className='android.widget.TextView',
                                                                                   index=1).info['text']
                else:
                    carrer = '空'
                # print('=============================%s================================================================='%carrer)
                z.heartbeat()
                if d(text='收入').exists:
                    for t in range(1, 14):
                        if publicpath.child(className='android.widget.LinearLayout', index=t).child(text='收入').exists:
                            break
                    income = publicpath.child(className='android.widget.LinearLayout', index=t).child(className='android.widget.TextView',
                                                                                   index=1).info['text']
                else:
                    income = '空'
                # print('===============================%s==============================================================='%income)

                if d(text='兴趣爱好').exists:
                    for t in range(1, 14):
                        if publicpath.child(className='android.widget.LinearLayout', index=t).child(text='兴趣爱好').exists:
                            break
                    idexx = 0
                    taste = []    #将所有兴趣保存到集合里
                    z.heartbeat()
                    while True:
                        interest = publicpath.child(className='android.widget.LinearLayout', index=t).child(className='android.view.View').child(className='android.widget.TextView',
                                                                           index=idexx)
                        if interest.exists:
                            hobby = interest.info['text']
                            taste.append(hobby)
                            idexx = idexx+1
                        else:
                            break
                else:
                    taste = []
                # print(taste)
                z.heartbeat()
                para = {"phoneNumber":phoneNumber,
                        "x_11":nickname,
                        "x_12":realname,"x_13":gender,
                        "x_14":area,"x_15":age,
                        "x_16":accountStatus,
                        "x_17":accountCount,
                        "x_01":"AliPay","x_02":rank,
                        "x_03":account,"x_04":zodiac,
                        "x_05":identity,"x_06":tall,
                        "x_07":weight,"x_08":carrer,
                        "x_09":income,"x_10":taste}
                self.repo.PostInformation(args["repo_cate_id"], para)
                z.toast("%s入库完成" % phoneNumber)

                i = i+1
                d(description = '返回').click()


            else:
                if change==0:
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"通讯录内没有好友\"" ).communicate()
                    z.sleep(10)
                    return
                clickCondition = d(className='android.widget.ListView')
                obj = clickCondition.info
                obj = obj['visibleBounds']
                top = int(obj['top'])
                bottom = int(obj['bottom'])
                y = bottom - top
                d.swipe(width / 2, y, width / 2, 0)
                zz = i+2
                for k in range(1,10):
                    obj2 = d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=zz) \
                        .child(className='android.widget.LinearLayout').child(className='android.widget.TextView', index=0)       #结束判断条件
                    if obj2.exists:
                        phone = obj2.info['text']
                        if phone in set1:            #结束条件，如果
                            if (args["time_delay"]):
                                z.sleep(int(args["time_delay"]))
                            return
                        else:
                            break
                    else:
                        zz = zz-1
                        continue

                obj1 =d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=0) \
                    .child(className='android.widget.LinearLayout').child(className='android.widget.TextView', index=0)
                if obj1.exists:      #实现精准滑动后有的能显示第０列的电话号码，有的显示不出来
                    i = 0
                    continue
                else:
                    i = 1
                    continue


def getPluginClass():
    return AlipayDepost



if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

    clazz = getPluginClass()
    o = clazz()
    d = Device("cda0ae8d")
    z = ZDevice("cda0ae8d")

    # z.toast("开始重装支付宝APP")
    # z.cmd("shell", "pm uninstall com.eg.android.AlipayGphone")
    # z.cmd("shell", "su -c 'rm -rf /data/data/com.eg.android.AlipayGphone'")
    # z.cmd("install", "/home/zunyun/alipay.apk")



    #z.server.install();
    # d.server.adb.cmd("shell", "pm clear com.eg.android.AlipayGphone").communicate()  # 清除缓存
    # if d(textContains='今天操作太频繁了').exists:  # 操作频繁，清空账号信息，重新注册
    #     # z.cmd("shell", "pm clear com.eg.android.AlipayGphone")  # 清除缓存
    #     z.generateSerial()
    # d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()

    args = {"repo_number_id":44,"repo_cate_id":219};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

























