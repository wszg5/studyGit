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

class AlipayDepostII:
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

        # d(description='通讯录').click()
        # if d(text='转到银行卡').exists:
        #     d(description ='返回').click()
            # d(description='通讯录').click()

        d(text='转账').click()
        d(text='转到支付宝账户').click()
        # d(text='新的朋友').click()
        # d(text='添加手机联系人').click()


        publicpath = d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=2) \
            .child(className='android.widget.LinearLayout', index=0).child(
            className='android.widget.LinearLayout', index=0)  # 为下面的点击做准备


        # times = 3
        # while d(textContains='没有联系人').exists:
        #     z.heartbeat()
        #     d(description='返回').click()
        #     z.sleep(int(args["contact_wait"]))
        #     d(text='添加手机联系人').click()
        #     times = times - 1
        #     if times < 0:
        #         # z.toast("开始重装支付宝APP")
        #         # z.cmd("shell", "pm uninstall com.eg.android.AlipayGphone")
        #         # z.cmd("shell", "su -c 'rm -rf /data/data/com.eg.android.AlipayGphone'")
        #         # z.cmd("install", "/apps/alipay.apk")
        #         return



        z.heartbeat()
        while True:
            cate_id = int( args["repo_number_id"] )  # 得到取号码的仓库号
            number_count = 1  # 每次取一个号码
            while True:
                exist_numbers = self.repo.GetNumber( cate_id, 0, number_count, 'exist' )
                print( exist_numbers )
                remain = number_count - len( exist_numbers )
                normal_numbers = self.repo.GetNumber( cate_id, 0, remain, 'normal' )
                numbers = exist_numbers + normal_numbers
                if len( numbers ) > 0:
                    break
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空，等待中\"" % cate_id ).communicate( )
                z.sleep( 30 )
            phoneNumber = numbers[0]['number']
            if d( description='清空', resourceId='com.alipay.mobile.ui:id/clearButton',
               className='android.widget.ImageButton', index=0 ).exists:
                d( description='清空', resourceId='com.alipay.mobile.ui:id/clearButton',
                    className='android.widget.ImageButton', index=0 ).click( )
            z.input(phoneNumber)
            d(text='下一步').click()

            z.sleep( 1.5 )
            if d(textContains='账号不存在').exists:
                d(text='确定').click()
                d(description='清空',resourceId='com.alipay.mobile.ui:id/clearButton',className='android.widget.ImageButton',index=0).click()
                self.repo.uploadPhoneNumber(phoneNumber, int(args["repo_not_exist_id"]))
                z.toast("不存在号码，入库成功")
                continue

            if d( textContains='频繁' ).exists:
                d( text='确定' ).click( )
                d( description='清空', resourceId='com.alipay.mobile.ui:id/clearButton',
                   className='android.widget.ImageButton', index=0 ).click( )
                break

            if d( textContains='该手机号对应多个支付宝账户，请核实后选择' ).exists:
                d(className='android.widget.RelativeLayout' ,index=0).click()

            # if d( textContains='今天操作太频繁了' ).exists or d(
            #         textContains='该功能暂未对您开放' ).exists:  # 操作频繁 / 该功能暂未对您开放 ，清空账号信息，重启手机
            #     z.toast( "开始重装支付宝APP" )
            #     z.cmd( "shell", "pm uninstall com.eg.android.AlipayGphone" )
            #     z.cmd( "shell", "su -c 'rm -rf /data/data/com.eg.android.AlipayGphone'" )
            #     z.cmd( "install", "/apps/alipay.apk" )
            #     return

            z.sleep( 3 )
            if d(text='添加备注(50字以内)') and d(text="转账金额").exists:
                realnameStr = \
                    d( className='android.widget.ScrollView' ).child( className='android.widget.LinearLayout',
                                                                      index=0 ).child(
                        className='android.widget.RelativeLayout', index=1 ).child(
                        className='android.widget.TextView' ).info['text']

                a = realnameStr.find('（')
                b = realnameStr.find('）')
                realname = realnameStr[a+2:b]

                if d( textContains='对方长时间未使用支付宝' ).exists:
                    accountStatus = "非常用"
                else:
                    accountStatus = "常用"
            else:
                realname = '无'


            d(resourceId='com.alipay.mobile.transferapp:id/tf_receiverHeadImg',description='头像',className='android.widget.ImageView').click()
            z.sleep( 3 )


            # print('=========================%s====================================================================='%realname)

            path = d( className='android.widget.ListView' ).child( className='android.widget.FrameLayout',
                                                                   index=0 ).child(
                className='android.widget.ImageView', index=2 )
            getinfo = self.Gender( d, path )
            print(getinfo)
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
            if d( className='android.widget.ListView' ).child( className='android.widget.FrameLayout' ).child(
                    className='android.widget.TextView', index=0 ).exists:
                nickname = \
                d( className='android.widget.ListView' ).child( className='android.widget.FrameLayout' ).child(
                    className='android.widget.TextView', index=0 ).info['text']  # 要保存的昵称
            else:
                nickname = '空'
            # print('=============================%s=============================================================='%nickname)

            z.heartbeat( )
            if d( text='支付宝账户' ).exists:
                for t in range( 0, 14 ):
                    if publicpath.child( className='android.widget.LinearLayout', index=t ).child(
                            text='支付宝账户' ).exists:
                        break
                account = publicpath.child( className='android.widget.LinearLayout', index=t ).child(
                    className='android.widget.TextView',
                    index=1 ).info['text']
            else:
                account = '空'
            z.heartbeat( )

            # print('================================%s============================================================='%account)

            if d( text='真实姓名' ).exists:
                path = publicpath.child( className='android.widget.LinearLayout', index=1 ).child(
                    className='android.widget.TextView', index='1' )
                getinfo = self.Gender( d, path )
                if getinfo[0] > 200:
                    gender = '女'  # 要保存的性别和是否认证
                    identity = '已实名'
                elif getinfo[2] > 200:
                    gender = '男'
                    identity = '已实名'
                else:
                    gender = '无'
                    identity = '未实名'
            # print('==========================%s==============%s======================================================'%(gender,identity))


            if d( text='显示更多' ).exists:
                d( text='显示更多' ).click( )
                z.sleep( 1 )
                if not d( text='收起' ).exists:
                    d.swipe( width / 2, height * 3 / 4, width / 2, height / 3 )

            z.heartbeat( )
            if d( text='地区' ).exists:
                area = publicpath.child( className='android.widget.LinearLayout', index=2 ).child(
                    className='android.widget.TextView', index='1' ).info['text']
            else:
                area = '空'
            # print('=========================%s====================================================================='%area)

            if d( text='星座' ).exists:  # 星座
                zodiac = d( textContains='座', index=1 ).info['text']
            else:
                zodiac = '空'

            # print('=============================%s================================================================='%zodiac)


            if d( text='年龄' ).exists:
                for t in range( 1, 14 ):
                    if publicpath.child( className='android.widget.LinearLayout', index=t ).child( text='年龄' ).exists:
                        break
                age = publicpath.child( className='android.widget.LinearLayout', index=t ).child(
                    className='android.widget.TextView',
                    index=1 ).info['text']
            else:
                age = '空'
            # print('=================================%s============================================================='%age)

            if d( text='身高' ).exists:
                for t in range( 1, 14 ):
                    if publicpath.child( className='android.widget.LinearLayout', index=t ).child( text='身高' ).exists:
                        break
                tall = publicpath.child( className='android.widget.LinearLayout', index=t ).child(
                    className='android.widget.TextView',
                    index=1 ).info['text']
            else:
                tall = '空'
            # print('==========================%s===================================================================='%tall)

            if d( text='体重' ).exists:
                for t in range( 1, 14 ):
                    if publicpath.child( className='android.widget.LinearLayout', index=t ).child( text='体重' ).exists:
                        break
                weight = publicpath.child( className='android.widget.LinearLayout', index=t ).child(
                    className='android.widget.TextView',
                    index=1 ).info['text']
            else:
                weight = '空'
            # print('=============================%s================================================================='%weight)
            z.heartbeat( )
            if d( text='职业' ).exists:
                for t in range( 1, 14 ):
                    if publicpath.child( className='android.widget.LinearLayout', index=t ).child( text='职业' ).exists:
                        break
                carrer = publicpath.child( className='android.widget.LinearLayout', index=t ).child(
                    className='android.widget.TextView',
                    index=1 ).info['text']
            else:
                carrer = '空'
            # print('=============================%s================================================================='%carrer)
            z.heartbeat( )
            if d( text='收入' ).exists:
                for t in range( 1, 14 ):
                    if publicpath.child( className='android.widget.LinearLayout', index=t ).child( text='收入' ).exists:
                        break
                income = publicpath.child( className='android.widget.LinearLayout', index=t ).child(
                    className='android.widget.TextView',
                    index=1 ).info['text']
            else:
                income = '空'
            # print('===============================%s==============================================================='%income)

            if d( text='兴趣爱好' ).exists:
                for t in range( 1, 14 ):
                    if publicpath.child( className='android.widget.LinearLayout', index=t ).child( text='兴趣爱好' ).exists:
                        break
                idexx = 0
                taste = []  # 将所有兴趣保存到集合里
                z.heartbeat( )
                while True:
                    interest = publicpath.child( className='android.widget.LinearLayout', index=t ).child(
                        className='android.view.View' ).child( className='android.widget.TextView',
                                                               index=idexx )
                    if interest.exists:
                        hobby = interest.info['text']
                        taste.append( hobby )
                        idexx = idexx + 1
                    else:
                        break
            else:
                taste = []
            # print(taste)
            z.heartbeat( )
            para = {"phoneNumber": phoneNumber,
                    "x_11": nickname,
                    "x_12": realname, "x_13": gender,
                    "x_14": area, "x_15": age,
                    "x_16": accountStatus,
                    "x_01": "AliPay", "x_02": rank,
                    "x_03": account, "x_04": zodiac,
                    "x_05": identity, "x_06": tall,
                    "x_07": weight, "x_08": carrer,
                    "x_09": income, "x_10": taste}
            self.repo.PostInformation( args["repo_cate_id"], para )
            z.toast( "%s入库完成" % phoneNumber )

            d(resourceId='com.alipay.mobile.ui:id/title_bar_back_button',className='android.widget.ImageButton',description='返回').click()
            d(resourceId='com.alipay.mobile.ui:id/title_bar_back_button',className='android.widget.ImageButton',description='返回').click()
            continue

            # judexist = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=i)\
            #     .child(className='android.widget.LinearLayout').child(className='android.widget.TextView',index=0)
            # if judexist.exists:
            #     z.heartbeat()
            #     change = 1
            #     phoneNumber = judexist.info['text']#要保存的电话号码
            #     if phoneNumber in set1:
            #         i = i+1
            #         continue
            #     set1.add(phoneNumber)
            #     # print(phoneNumber)
            #     judexist.click()        #点击第i个人
            #     z.sleep(1.5)

            #
            # else:
            #     if change==0:
            #         d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"通讯录内没有好友\"" ).communicate()
            #         z.sleep(10)
            #         return
            #     clickCondition = d(className='android.widget.ListView')
            #     obj = clickCondition.info
            #     obj = obj['visibleBounds']
            #     top = int(obj['top'])
            #     bottom = int(obj['bottom'])
            #     y = bottom - top
            #     d.swipe(width / 2, y, width / 2, 0)
            #     zz = i+2
            #     for k in range(1,10):
            #         obj2 = d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=zz) \
            #             .child(className='android.widget.LinearLayout').child(className='android.widget.TextView', index=0)       #结束判断条件
            #         if obj2.exists:
            #             phone = obj2.info['text']
            #             if phone in set1:            #结束条件，如果
            #                 if (args["time_delay"]):
            #                     z.sleep(int(args["time_delay"]))
            #                 return
            #             else:
            #                 break
            #         else:
            #             zz = zz-1
            #             continue
            #
            #     obj1 =d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=0) \
            #         .child(className='android.widget.LinearLayout').child(className='android.widget.TextView', index=0)
            #     if obj1.exists:      #实现精准滑动后有的能显示第０列的电话号码，有的显示不出来
            #         i = 0
            #         continue
            #     else:
            #         i = 1
            #         continue


def getPluginClass():
    return AlipayDepostII



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
    # z.generateSerial()
    # d.server.adb.cmd("shell", "pm clear com.eg.android.AlipayGphone").communicate()  # 清除缓存
    # if d(textContains='今天操作太频繁了').exists:  # 操作频繁，清空账号信息，重新注册
    #     z.cmd("shell", "pm clear com.eg.android.AlipayGphone")  # 清除缓存
    #     z.generateSerial()
    # d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()

    args = {"repo_number_id": "123", "repo_cate_id": "219", "repo_not_exist_id": "226", "repo_exception_id":"227"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

























