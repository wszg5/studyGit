# coding:utf-8
import colorsys

from PIL import Image

from smsCode import smsCode
from uiautomator import Device
from Repo import *
import os, time, datetime, random
import util
from zservice import ZDevice


class QLFilterPraise:

    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def Praise(self, d, z):
        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        z.sleep(1)
        z.heartbeat()
        obj3 = d(descriptionContains='赞')
        if obj3.exists:
            z.heartbeat( )
            obj3 = obj3.info
            obj3 = obj3['bounds']  # 验证码处的信息
            left = obj3["left"]  # 验证码的位置信息
            top = obj3['top']
            right = obj3['right']
            bottom = obj3['bottom']

            d.screenshot( sourcePng )  #

            img = Image.open( sourcePng )
            box = (left, top, right, bottom)  # left top right bottom
            region = img.crop( box )  #
            # show(region)    #展示资料卡上的信息
            image = region.convert( 'RGBA' )
            # 生成缩略图，减少计算量，减小cpu压力
            image.thumbnail( (200, 200) )
            max_score = None
            dominant_color = None
            for count, (r, g, b, a) in image.getcolors( image.size[0] * image.size[1] ):
                # 跳过纯黑色
                if a == 0:
                    continue
                saturation = colorsys.rgb_to_hsv( r / 255.0, g / 255.0, b / 255.0 )[1]
                y = min( abs( r * 2104 + g * 4130 + b * 802 + 4096 + 131072 ) >> 13, 235 )
                y = (y - 16.0) / (235 - 16)
                # 忽略高亮色
                if y > 0.9:
                    continue
                z.heartbeat( )
                score = (saturation + 0.1) * count
                if score > max_score:
                    max_score = score
                    dominant_color = (r, g, b)
            # print("---------------------------------------------------------------------------")
            # print(dominant_color)
            z.heartbeat( )
            if None == dominant_color:
                return '不限'
            red = dominant_color[1]
            blue = dominant_color[2]

            if red > blue:
                # print('女')
                return "无"
            else:
                # print('男')
                return '有'
        else:  # 没有基本资料的情况
            return '跳过'

    def action(self, d, z,args):
        z.toast( "准备执行QQ轻聊版附近的人点赞" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ轻聊版附近的人点赞" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.qqlite" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
        z.heartbeat( )

        if d( text='消息' ).exists:  # 到了通讯录这步后看号有没有被冻结
            z.toast( "卡槽状态正常，继续执行" )
        else:
            z.toast( "卡槽状态异常，跳过此模块" )
            return

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        gender = args["gender"]
        count = int(args["count"])

        d(text="我",className="android.widget.TextView").click()
        if d(text="附近的人").exists:
            d(text="附近的人").click()
        else:
            d( text="我", className="android.widget.TextView" ).click()
            d(text="附近的人").click()
        z.sleep(2)
        d(index=0,resourceId="com.tencent.qqlite:id/ivTitleBtnRightImage").click()
        z.heartbeat()
        d(text="筛选附近的人").click()

        if gender != "全部":
            d(text=gender,resourceId="com.tencent.qqlite:id/0",className="android.widget.TextView").click()
        else:
            d(text="全部").click()
        z.sleep(1)
        z.heartbeat()
        d(text="完成").click()
        z.sleep(1)
        index=1
        num = 0
        while True:
           obj =  d(index=0,resourceId="com.tencent.qqlite:id/0",className="android.view.View").child(index=index,className="android.widget.RelativeLayout").child(
                index=0,className="android.widget.ImageView",resourceId="android:id/icon")
           if obj.exists:
                obj.click()
                z.sleep(1)
                obj2 = d( descriptionContains='赞' )
                
                text = self.Praise(d,z)
                if text=="无":
                    # for i in range(0,click_count):
                    obj2.click()
                    num = num + 1
                else:
                    pass
                obj2 = d( descriptionContains='赞')
                if obj2.exists:
                    obj2.click()
                    num = num + 1
                z.heartbeat()
                z.sleep(1)
                d(index=0,resourceId="com.tencent.qqlite:id/ivTitleBtnLeft",description="向上导航").click()
                index = index +1
           else:
               d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
               index= 2
           if num == count:
               z.toast("模块完成")
               break

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return QLFilterPraise

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # print(d.dump(compressed=False))
    args = {'gender':"男","count":"8","time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)